# routes/convert.py
from fastapi import APIRouter, HTTPException
import aiofiles
import uuid
import os
import os
from tts_providers.azure_tts import AzureTTSProvider
from tts_providers.google_tts import GoogleTTSProvider

router = APIRouter()

AUDIO_DIR = "audio"


@router.post("/convert_to_speech/")
async def convert_to_speech(file_path: str, engine: str = "azure", voice: str = None):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # Read the content of the eBook
    async with aiofiles.open(file_path, "r") as ebook_file:
        text = await ebook_file.read()

    # Choose the TTS engine
    audio_filename = f"{uuid.uuid4()}_output.wav"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    if engine == "azure":
        tts_provider = AzureTTSProvider()
    elif engine == "google":
        tts_provider = GoogleTTSProvider()
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported TTS engine. Supported engines are: azure, google.",
        )

    # Generate speech from text
    result = tts_provider.synthesize(text, audio_path, voice)

    if not result:
        raise HTTPException(status_code=500, detail="Error synthesizing audio.")

    return {"message": "Audio generated successfully", "audio_path": audio_path}
