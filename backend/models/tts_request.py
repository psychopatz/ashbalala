from pydantic import BaseModel
from backend.core.config import DEFAULT_VOICE, DEFAULT_STYLE, DEFAULT_RATE, DEFAULT_PITCH

class TTSRequest(BaseModel):
    text: str
    voice: str = DEFAULT_VOICE
    style: str = DEFAULT_STYLE
    rate: str = DEFAULT_RATE
    pitch: str = DEFAULT_PITCH
