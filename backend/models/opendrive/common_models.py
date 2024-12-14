from pydantic import BaseModel
from typing import Optional
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
    TempStreamingLink: Optional[str] = None
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