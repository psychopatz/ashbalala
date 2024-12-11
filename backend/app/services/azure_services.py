# Azure-related service functions

import requests
from datetime import datetime, timedelta
from fastapi import HTTPException
import aiofiles

# Configuration
SUBSCRIPTION_KEY = "7fEVd26MSr5EJ2bPzDX3XDZ8YC7pLhyo5anue6mYJv805kteGaGBJQQJ99AKACYeBjFXJ3w3AAAYACOGP5eQ"
REGION = "eastus"
TOKEN_URL = f"https://{REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
TTS_URL = f"https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
VOICES_URL = f"https://{REGION}.tts.speech.microsoft.com/cognitiveservices/voices/list"

def save_audio(audio_content: bytes, file_path: str):
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(audio_content)

class VoiceManager:
    def __init__(self):
        self.voices = None
        self.last_updated = None
        self.update_interval = timedelta(hours=24)

    async def get_voices(self, token: str):
        if self.voices and self.last_updated and datetime.now() - self.last_updated < self.update_interval:
            return self.voices

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(VOICES_URL, headers=headers)
        if response.status_code == 200:
            voices = response.json()
            self.voices = voices
            self.last_updated = datetime.now()
            return voices
        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch voices: {response.text}")

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
