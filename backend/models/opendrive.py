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

class UploadResponse(BaseModel):
    FileId: str = Field(..., alias='FileId')

class DownloadLinkResponse(BaseModel):
    DownloadLink: str = Field(..., alias='DownloadLink')

class SessionCheckRequest(BaseModel):
    session_id: str

class SessionCheckResponse(BaseModel):
    result: bool

# Check file exists models
class CheckFileExistsRequest(BaseModel):
    folder_id: str
    session_id: str
    name: List[str]

class CheckFileExistsResponse(BaseModel):
    result: List[str]

# Create file models
class CreateFileRequest(BaseModel):
    session_id: str
    folder_id: str
    file_name: str
    file_description: Optional[str] = None
    access_folder_id: Optional[str] = None
    file_size: Optional[int] = None
    file_hash: Optional[str] = None
    sharing_id: Optional[str] = None
    open_if_exists: Optional[int] = None

class CreateFileResponse(BaseModel):
    FileId: Optional[str] = None
    Name: Optional[str] = None
    GroupID: Optional[Union[str, int]] = None  # Accepts both str and int
    Extension: Optional[str] = None
    Size: Optional[str] = None
    Views: Optional[str] = None
    Version: Optional[str] = None
    Downloads: Optional[str] = None
    Access: Optional[str] = None
    Link: Optional[str] = None
    DownloadLink: Optional[str] = None
    StreamingLink: Optional[str] = None
    DirUpdateTime: Optional[int] = None
    TempLocation: Optional[str] = None
    SpeedLimit: Optional[int] = None
    RequireCompression: Optional[int] = None
    RequireHash: Optional[int] = None
    RequireHashOnly: Optional[int] = None

    class Config:
        extra = "allow"  # Allows ignoring unexpected fields