# /backend/services/opendrive/recursive_folder_service.py

from typing import List
from core.opendrive_interface import IFolderService
from models.opendrive.recursive_folder_model import (
    RecursiveFolderResponse,
    RecursiveFolderItem,
)


class RecursiveFolderService:
    def __init__(self, folder_service: IFolderService):
        self.folder_service = folder_service

    async def _get_recursive_folder(
        self, session_id: str, folder_id: str
    ) -> RecursiveFolderItem:
        list_folder_response = await self.folder_service.list_folder(
            session_id, folder_id
        )

        folder_item = RecursiveFolderItem(
            FolderID=folder_id,
            ParentID=list_folder_response.ParentFolderID,
            Name=list_folder_response.Name,
            Description=None,
            IsPublic=None,
            PublicUpl=None,
            PublicDisplay=None,
            PublicDnl=None,
            DateCreated=0,
            DateModified=0,
            DateAccessed=None,
            OwnerSuspended=None,
            FilesCount=None,
            FoldersCount=None,
            IsArchive=None,
            Category=None,
            OwnerName=None,
            OwnerID=None,
            AccessUser=None,
            DirUpdateTime=(
                int(list_folder_response.DirUpdateTime)
                if list_folder_response.DirUpdateTime
                else 0
            ),
            AccessDisabled=None,
            SharingID=None,
            OwnerLevel=None,
            HasSubFolders=None,
            Access=0,
            Shared="False",
            ChildFolders=0,
            Link=list_folder_response.DirectFolderLink,
            Encrypted="0",
            Files=list_folder_response.Files,
        )

        if list_folder_response.Folders:
            folder_item.Folders = []
            for folder in list_folder_response.Folders:
                folder_item.Folders.append(
                    await self._get_recursive_folder(session_id, folder.FolderID)
                )
        return folder_item

    async def get_recursive_folder(
        self, session_id: str, folder_id: str
    ) -> RecursiveFolderResponse:

        list_folder_response = await self.folder_service.list_folder(
            session_id, folder_id
        )

        recursive_folder_data = RecursiveFolderResponse(
            DirUpdateTime=list_folder_response.DirUpdateTime,
            Name=list_folder_response.Name,
            ParentFolderID=list_folder_response.ParentFolderID,
            DirectFolderLink=list_folder_response.DirectFolderLink,
            ResponseType=list_folder_response.ResponseType,
        )

        if list_folder_response.Folders:
            recursive_folder_data.Folders = []
            for folder in list_folder_response.Folders:
                recursive_folder_data.Folders.append(
                    await self._get_recursive_folder(session_id, folder.FolderID)
                )

        recursive_folder_data.Files = (
            list_folder_response.Files if list_folder_response.Files else []
        )

        return recursive_folder_data
