from fastapi import APIRouter, HTTPException
from typing import Optional
from api.voices.azure.tts import another_function
from api.util.azure import token_manager, voice_manager

router = APIRouter()

@router.get("/voices")
async def get_available_voices(locale: Optional[str] = None):
    token = await token_manager.get_token()
    voices = await voice_manager.get_voices(token)
    if locale:
        voices = [voice for voice in voices if voice['locale'] == locale]
    if not voices:
        raise HTTPException(status_code=404, detail="No voices found for the specified locale.")
    return voices
