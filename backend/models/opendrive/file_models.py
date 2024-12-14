from pydantic import BaseModel
from typing import Optional, List

class CheckFileExistsRequest(BaseModel):
    folder_id: str
    session_id: str
    name: List[str]

class CheckFileExistsResponse(BaseModel):
    result: List[str]

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