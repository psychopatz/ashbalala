# /backend/models/opendrive/file_models.py
from pydantic import BaseModel
from typing import Optional, List


class CheckFileExistsRequest(BaseModel):
    folder_id: str
    session_id: str
    name: List[str]


class CheckFileExistsResponse(BaseModel):
    result: List[str]


class CreateFileResponse(BaseModel):
    FileId: str
    DirUpdateTime: Optional[int]


class OpenFileUploadResponse(BaseModel):
    TempLocation: str


class UploadFileChunkResponse(BaseModel):
    TotalWritten: int


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


class RetrieveThumbResponse(BaseModel):
    content: bytes
    content_type: str


class RemoveDeleteResponse(BaseModel):
    success: bool


# Add for rename file
class RenameFileRequest(BaseModel):
    session_id: str
    new_file_name: str
    file_id: str
    access_folder_id: str = ""


class RenameFileResponse(BaseModel):
    success: bool
    message: str


class ExpiringLinkResponse(BaseModel):
    DownloadLink: str
    StreamingLink: str
