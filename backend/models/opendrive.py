from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    SessionID: str = Field(..., alias='SessionID')

class UploadResponse(BaseModel):
    FileId: str = Field(..., alias='FileId')

class DownloadLinkResponse(BaseModel):
    DownloadLink: str = Field(..., alias='DownloadLink')
