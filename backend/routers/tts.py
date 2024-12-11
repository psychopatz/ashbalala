from fastapi import APIRouter, BackgroundTasks, HTTPException
from backend.models.tts_request import TTSRequest
from backend.services.azure_service import AzureTTSService
from backend.utils.file_io import save_audio_file
import base64
import uuid
from backend.core.config import AUDIO_FILES_DIR

router = APIRouter()
tts_service = AzureTTSService()

@router.post("/")
async def text_to_speech(request: TTSRequest, background_tasks: BackgroundTasks):
    try:
        audio_content = await tts_service.synthesize_speech(
            text=request.text,
            voice=request.voice,
            style=request.style,
            rate=request.rate,
            pitch=request.pitch,
        )

        filename = f"audio_{uuid.uuid4()}.mp3"
        file_path = f"{AUDIO_FILES_DIR}/{filename}"

        # Save the audio in the background
        background_tasks.add_task(save_audio_file, audio_content, file_path)

        return {
            "status": "success",
            "file_path": file_path,
            "audio_base64": base64.b64encode(audio_content).decode("utf-8"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
