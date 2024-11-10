from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import requests
import base64
import json
import os
from datetime import datetime, timedelta
import aiofiles
import uuid
from typing import List, Dict, Optional
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuration
SUBSCRIPTION_KEY = "7fEVd26MSr5EJ2bPzDX3XDZ8YC7pLhyo5anue6mYJv805kteGaGBJQQJ99AKACYeBjFXJ3w3AAAYACOGP5eQ"
REGION = "eastus"  # Replace with your Azure region
TOKEN_URL = f"https://{REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
TTS_URL = f"https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
VOICES_URL = f"https://{REGION}.tts.speech.microsoft.com/cognitiveservices/voices/list"


class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-JennyNeural"  # Default voice
    style: str = "neutral"  # Default style
    rate: str = "+0%"  # Default rate
    pitch: str = "+0Hz"  # Default pitch


class VoiceManager:
    def __init__(self):
        self.voices = None
        self.last_updated = None
        self.update_interval = timedelta(hours=24)  # Update voices list daily

    async def get_voices(self, token: str) -> List[Dict]:
        # Return cached voices if they're still valid
        if (
            self.voices
            and self.last_updated
            and datetime.now() - self.last_updated < self.update_interval
        ):
            return self.voices

        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(VOICES_URL, headers=headers)
        if response.status_code == 200:
            # Process and organize voices by locale
            voices = response.json()
            self.voices = voices
            self.last_updated = datetime.now()
            return voices
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to fetch voices: {response.text}",
        )


class TokenManager:
    def __init__(self):
        self.token = None
        self.expiry_time = None

    async def get_token(self):
        if self.token and self.expiry_time and datetime.now() < self.expiry_time:
            return self.token

        headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}

        response = requests.post(TOKEN_URL, headers=headers)
        if response.status_code == 200:
            self.token = response.text
            self.expiry_time = datetime.now() + timedelta(minutes=9)
            return self.token
        raise HTTPException(status_code=401, detail="Failed to get Azure token")


token_manager = TokenManager()
voice_manager = VoiceManager()


async def save_audio(audio_content: bytes, file_path: str):
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(audio_content)


@app.get("/voices")
async def get_available_voices(
    locale: Optional[str] = None,
    gender: Optional[str] = None,
    neural: Optional[bool] = None,
):
    """
    Get available voices with optional filters:
    - locale: e.g., "en-US", "es-ES"
    - gender: "Male" or "Female"
    - neural: true for neural voices only
    """
    try:
        token = await token_manager.get_token()
        voices = await voice_manager.get_voices(token)

        # Apply filters if provided
        filtered_voices = voices
        if locale:
            filtered_voices = [
                v
                for v in filtered_voices
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
            locale = voice["Locale"]
            if locale not in organized_voices:
                organized_voices[locale] = []

            # Simplify the voice data
            simplified_voice = {
                "name": voice["ShortName"],
                "gender": voice["Gender"],
                "type": voice["VoiceType"],
                "sample_rate": voice["SampleRateHertz"],
                "styles": voice.get("StyleList", []),  # Some voices support styles
                "roles": voice.get("RolePlayList", []),  # Some voices support roles
            }
            organized_voices[locale].append(simplified_voice)

        return JSONResponse(
            content={
                "total_voices": len(filtered_voices),
                "voices_by_locale": organized_voices,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tts")
async def text_to_speech(request: TTSRequest, background_tasks: BackgroundTasks):
    try:
        # Get access token
        token = await token_manager.get_token()

        # Prepare SSML
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='{request.voice}'>
                <prosody rate='{request.rate}' pitch='{request.pitch}'>
                    <mstts:express-as style='{request.style}' xmlns:mstts='http://www.w3.org/2001/mstts'>
                        {request.text}
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

        response = requests.post(TTS_URL, headers=headers, data=ssml.encode("utf-8"))

        if response.status_code == 200:
            filename = f"audio_{uuid.uuid4()}.mp3"
            file_path = f"audio_files/{filename}"

            os.makedirs("audio_files", exist_ok=True)

            background_tasks.add_task(save_audio, response.content, file_path)

            return {
                "status": "success",
                "file_path": file_path,
                "audio_base64": base64.b64encode(response.content).decode("utf-8"),
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Azure TTS API error: {response.text}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
