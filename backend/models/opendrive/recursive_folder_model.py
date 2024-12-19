# /backend/models/opendrive/recursive_folder_model.py

from typing import List, Optional
from pydantic import BaseModel


class RecursiveFolderItem(BaseModel):
    FolderID: str
    ParentID: Optional[str]
    Name: str
    Description: Optional[str]
    IsPublic: Optional[int]
    PublicUpl: Optional[int]
    PublicDisplay: Optional[int]
    PublicDnl: Optional[int]
    DateCreated: int
    DateModified: int
    DateAccessed: Optional[int]
    OwnerSuspended: Optional[int]
    FilesCount: Optional[int]
    FoldersCount: Optional[int]
    IsArchive: Optional[int]
    Category: Optional[int]
    OwnerName: Optional[str]
    OwnerID: Optional[str]
    AccessUser: Optional[str]
    DirUpdateTime: int
    AccessDisabled: Optional[int]
    SharingID: Optional[str]
    OwnerLevel: Optional[int]
    HasSubFolders: Optional[int]
    Access: int
    Shared: str
    ChildFolders: int
    Link: str
    Encrypted: str
    Folders: Optional[List["RecursiveFolderItem"]] = None
    Files: Optional[List[dict]] = None


class RecursiveFolderResponse(BaseModel):
    DirUpdateTime: str
    Name: str
    ParentFolderID: str
    DirectFolderLink: str
    ResponseType: int
    Folders: Optional[List[RecursiveFolderItem]] = None
    Files: Optional[List[dict]] = None
