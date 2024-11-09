from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get("/download_audio/")
async def download_audio(audio_path: str):
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    return FileResponse(
        audio_path, media_type="audio/wav", filename=os.path.basename(audio_path)
    )
