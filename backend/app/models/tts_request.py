from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-JennyNeural"
    style: str = "neutral"
    rate: str = "+0%"
    pitch: str = "+0Hz"
