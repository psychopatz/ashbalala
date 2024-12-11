from fastapi import APIRouter, HTTPException
from typing import Optional
from backend.services.azure_service import AzureTTSService

router = APIRouter()
tts_service = AzureTTSService()

@router.get("/")
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
        voices_info = await tts_service.get_voices(locale=locale, gender=gender, neural=neural)
        return voices_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
