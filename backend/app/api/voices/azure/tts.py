from api.voices.azure.get_voices import some_function
from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.models import TTSRequest
from api.util.azure import token_manager, save_audio
import requests
import os
import uuid

router = APIRouter()

@router.post("/text-to-speech")
async def text_to_speech(request: TTSRequest, background_tasks: BackgroundTasks):
    token = await token_manager.get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-32kbitrate-mono-mp3",
    }
    ssml = f"""
    <speak version='1.0' xml:lang='en-US'>
        <voice xml:lang='en-US' xml:gender='Female' name='{request.voice}'>
            <prosody rate='{request.rate}' pitch='{request.pitch}'>
                {request.text}
            </prosody>
        </voice>
    </speak>
    """
    response = requests.post(TTS_URL, headers=headers, data=ssml.encode('utf-8'))
    if response.status_code == 200:
        audio_content = response.content
        file_name = f"audio_{uuid.uuid4()}.mp3"
        file_path = os.path.join("audio_files", file_name)
        background_tasks.add_task(save_audio, audio_content, file_path)
        return {"file_path": file_path}
    raise HTTPException(status_code=response.status_code, detail="Failed to convert text to speech.")
