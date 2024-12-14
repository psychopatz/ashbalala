# models/opendrive.py
from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    session_id: Optional[str] = None # Optional session_id field


class LoginResponse(BaseModel):
    SessionID: str
    UserName: str
    UserFirstName: str
    UserLastName: str
    AccType: str
    UserLang: str
    Enable2FA: str
    Active2FA: str
    UserID: str
    IsAccountUser: int
    DriveName: str
    UserLevel: str
    UserPlan: str
    FVersioning: str
    UserDomain: str
    PartnerUsersDomain: str
    UploadSpeedLimit: int
    DownloadSpeedLimit: int
    UploadsPerSecond: int
    DownloadsPerSecond: int

class UploadResponse(BaseModel):
    FileId: str = Field(..., alias='FileId')

class DownloadLinkResponse(BaseModel):
    DownloadLink: str = Field(..., alias='DownloadLink')


class SessionCheckRequest(BaseModel):
    session_id: str

class SessionCheckResponse(BaseModel):
  result: bool