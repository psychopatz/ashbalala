from pydantic import BaseModel
from typing import Optional, List
from models.opendrive.common_models import FolderInfo


class CreateFolderRequest(BaseModel):
    session_id: str
    folder_name: str
    folder_sub_parent: str
    folder_is_public: int
    folder_public_upl: int
    folder_public_display: int
    folder_public_dnl: int
    folder_description: str = ""


class ListFolderRequest(BaseModel):
    session_id: str
    folder_id: str


class ListFolderResponse(BaseModel):
    DirUpdateTime: str
    Name: str
    ParentFolderID: str
    DirectFolderLink: str
    ResponseType: int
    Folders: Optional[List[FolderInfo]] = []
    Files: Optional[List[dict]] = []


class RemoveFolderRequest(BaseModel):
    session_id: str
    folder_id: str


class RemoveFolderResponse(BaseModel):
    DirUpdateTime: int


class RenameFolderRequest(BaseModel):
    session_id: str
    folder_id: str
    folder_name: str


class RenameFolderResponse(BaseModel):
    DirUpdateTime: int
