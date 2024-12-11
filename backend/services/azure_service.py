import requests
import uuid
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from fastapi import HTTPException
from backend.core.interfaces import ITTSService
from backend.core.config import (
    AZURE_SUBSCRIPTION_KEY, AZURE_TOKEN_URL, AZURE_TTS_URL, AZURE_VOICES_URL,
    TOKEN_EXPIRY_MINUTES, VOICES_UPDATE_INTERVAL
)

class AzureTokenManager:
    def __init__(self):
        self.token = None
        self.expiry_time = None

    async def get_token(self) -> str:
        if self.token and self.expiry_time and datetime.now() < self.expiry_time:
            return self.token

        headers = {"Ocp-Apim-Subscription-Key": AZURE_SUBSCRIPTION_KEY}
        response = requests.post(AZURE_TOKEN_URL, headers=headers)
        if response.status_code == 200:
            self.token = response.text
            self.expiry_time = datetime.now() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
            return self.token
        raise HTTPException(status_code=401, detail="Failed to get Azure token")

class AzureVoiceManager:
    def __init__(self):
        self.voices = None
        self.last_updated = None

    async def get_voices(self, token: str) -> List[Dict]:
        # Return cached voices if they're still valid
        if (
            self.voices
            and self.last_updated
            and datetime.now() - self.last_updated < VOICES_UPDATE_INTERVAL
        ):
            return self.voices

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(AZURE_VOICES_URL, headers=headers)
        if response.status_code == 200:
            self.voices = response.json()
            self.last_updated = datetime.now()
            return self.voices
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to fetch voices: {response.text}",
        )

class AzureTTSService(ITTSService):
    def __init__(self):
        self.token_manager = AzureTokenManager()
        self.voice_manager = AzureVoiceManager()

    async def get_token(self) -> str:
        return await self.token_manager.get_token()

    async def get_voices(
        self, 
        locale: Optional[str] = None, 
        gender: Optional[str] = None, 
        neural: Optional[bool] = None
    ) -> Dict:
        token = await self.get_token()
        voices = await self.voice_manager.get_voices(token)

        # Apply filters if provided
        filtered_voices = voices
        if locale:
            filtered_voices = [
                v for v in filtered_voices
                if v["Locale"].lower().startswith(locale.lower())
            ]
        if gender:
            filtered_voices = [
                v for v in filtered_voices if v["Gender"].lower() == gender.lower()
            ]
        if neural is not None:
            filtered_voices = [
                v for v in filtered_voices if ("Neural" in v["VoiceType"]) == neural
            ]

        # Organize voices by locale
        organized_voices = {}
        for voice in filtered_voices:
            voice_locale = voice["Locale"]
            if voice_locale not in organized_voices:
                organized_voices[voice_locale] = []

            simplified_voice = {
                "name": voice["ShortName"],
                "gender": voice["Gender"],
                "type": voice["VoiceType"],
                "sample_rate": voice["SampleRateHertz"],
                "styles": voice.get("StyleList", []),
                "roles": voice.get("RolePlayList", []),
            }
            organized_voices[voice_locale].append(simplified_voice)

        return {
            "total_voices": len(filtered_voices),
            "voices_by_locale": organized_voices,
        }

    async def synthesize_speech(self, text: str, voice: str, style: str, rate: str, pitch: str) -> bytes:
        token = await self.get_token()
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='{voice}'>
                <prosody rate='{rate}' pitch='{pitch}'>
                    <mstts:express-as style='{style}' xmlns:mstts='http://www.w3.org/2001/mstts'>
                        {text}
                    </mstts:express-as>
                </prosody>
            </voice>
        </speak>
        """

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "FastAPI_TTS",
        }

        response = requests.post(AZURE_TTS_URL, headers=headers, data=ssml.encode("utf-8"))

        if response.status_code == 200:
            return response.content
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Azure TTS API error: {response.text}",
            )
