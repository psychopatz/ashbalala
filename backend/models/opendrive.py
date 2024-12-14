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

# File upload models
class CreateFileRequest(BaseModel):
    session_id: str
    folder_id: str
    file_name: str
    file_size: int
    open_if_exists: int = 1
    
class CreateFileResponse(BaseModel):
    FileId: str
    DirUpdateTime: Optional[int]

class OpenFileUploadRequest(BaseModel):
    session_id: str
    file_id: str
    file_size: int

class OpenFileUploadResponse(BaseModel):
    TempLocation: str

class UploadFileChunkRequest(BaseModel):
    session_id: str
    file_id: str
    temp_location: str
    chunk_offset: int
    chunk_size: int

class UploadFileChunkResponse(BaseModel):
    TotalWritten: int

class CloseFileUploadRequest(BaseModel):
    session_id: str
    file_id: str
    file_size: int
    temp_location: str
    file_time: int
    access_folder_id: str = "0"
    file_compressed: int = 0
    file_hash: str = ""
    sharing_id: str = ""

class CloseFileUploadResponse(BaseModel):
    FileId: str
    Name: str
    GroupID: str
    Extension: str
    Size: str
    Views: str
    Version: str
    Downloads: str
    DateTrashed: str
    DateModified: str
    OwnerSuspended: bool
    AccType: str
    FileHash: str
    Link: str
    DownloadLink: str
    StreamingLink: str
    OwnerName: str
    upload_speed_limit: int
    download_speed_limit: int
    BWExceeded: int
    ThumbLink: str
    Encrypted: str
    Password: str
    OwnerLevel: str
    EditOnline: int
    ID: str
    FolderID: str
    Description: str
    IsArchive: str
    Category: str
    Date: str
    DateUploaded: int
    DateAccessed: str
    DirectLinkPublick: str
    EmbedLink: str
    AccessDisabled: int
    Type: str
    DestURL: str
    Owner: str
    AccessUser: str
    DirUpdateTime: int
    FileName: str
    FileDate: str

# List Folder request/response
class ListFolderRequest(BaseModel):
    folder_id: str

class FileInfo(BaseModel):
    FileId: str
    Name: str
    GroupID: int
    Extension: str
    Size: str
    Views: str
    Version: str
    Downloads: str
    DateModified: str
    Access: str
    FileHash: str
    Link: str
    DownloadLink: str
    StreamingLink: str
    TempStreamingLink: str
    EditLink: Optional[str] = None
    ThumbLink: str
    Encrypted: int
    Password: str
    EditOnline: int

class FolderInfo(BaseModel):
    FolderID: str
    ParentID: str
    Name: str
    Description: str
    IsPublic: str
    PublicUpl: str
    PublicDisplay: str
    PublicDnl: str
    DateCreated: str
    DateModified: str
    DateAccessed: str
    OwnerSuspended: bool
    FilesCount: int
    FoldersCount: int
    IsArchive: str
    Category: str
    OwnerName: str
    OwnerID: str
    AccessUser: str
    DirUpdateTime: int
    AccessDisabled: int
    SharingID: str
    OwnerLevel: str
    HasSubFolders: int


class ListFolderResponse(BaseModel):
    DirUpdateTime: str
    Name: str
    ParentFolderID: str
    DirectFolderLink: str
    ResponseType: int
    Folders: Optional[List[FolderInfo]] = []
    Files: Optional[List[FileInfo]] = []