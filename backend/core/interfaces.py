from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class ITTSService(ABC):
    @abstractmethod
    async def get_token(self) -> str:
        pass

    @abstractmethod
    async def get_voices(
        self, 
        locale: Optional[str] = None, 
        gender: Optional[str] = None, 
        neural: Optional[bool] = None
    ) -> Dict:
        pass

    @abstractmethod
    async def synthesize_speech(self, text: str, voice: str, style: str, rate: str, pitch: str) -> bytes:
        pass
