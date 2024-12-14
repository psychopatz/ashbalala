from pydantic import BaseModel, Field
from typing import Optional, List, Union

# Login request/response
class LoginRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    session_id: Optional[str] = None

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

# Session check request/response
class SessionCheckRequest(BaseModel):
    session_id: str

class SessionCheckResponse(BaseModel):
    result: bool

# Check file exists request/response
class CheckFileExistsRequest(BaseModel):
    folder_id: str
    session_id: str
    name: List[str]

class CheckFileExistsResponse(BaseModel):
    result: List[str]
