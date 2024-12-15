from pydantic import BaseModel
from typing import Optional, Union


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
    ParentID: Optional[str] = None
    Name: str
    Description: Optional[str] = None
    IsPublic: Optional[Union[int, str]] = None
    PublicUpl: Optional[Union[int, str]] = None
    PublicDisplay: Optional[Union[int, str]] = None
    PublicDnl: Optional[Union[int, str]] = None
    DateCreated: Optional[Union[int, str]] = None
    DateModified: Optional[Union[int, str]] = None
    DateAccessed: Optional[str] = None
    OwnerSuspended: Optional[bool] = None
    FilesCount: Optional[int] = None
    FoldersCount: Optional[int] = None
    IsArchive: Optional[str] = None
    Category: Optional[str] = None
    OwnerName: Optional[str] = None
    OwnerID: Optional[str] = None
    AccessUser: Optional[str] = None
    DirUpdateTime: Optional[int] = None
    AccessDisabled: Optional[int] = None
    SharingID: Optional[str] = None
    OwnerLevel: Optional[str] = None
    HasSubFolders: Optional[int] = None
    Access: Optional[int] = None
    Shared: Optional[str] = None
    ChildFolders: Optional[int] = None
    Link: Optional[str] = None
    Encrypted: Optional[str] = None
