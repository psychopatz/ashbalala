from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from backend.services.tts.azure_service import AzureTTSService
from backend.core.tts_interface import ITTSService

router = APIRouter()

def get_tts_service() -> ITTSService:
    return AzureTTSService()

@router.get("/")
async def get_available_voices(
    locale: Optional[str] = None,
    gender: Optional[str] = None,
    neural: Optional[bool] = None,
    tts_service: ITTSService = Depends(get_tts_service)
):
    """
    Get available voices with optional filters:
    - locale: e.g., "en-US", "es-ES"
    - gender: "Male" or "Female"
    - neural: true for neural voices only
    """
    try:
        voices_info = await tts_service.get_voices(locale=locale, gender=gender, neural=neural)
        return voices_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))