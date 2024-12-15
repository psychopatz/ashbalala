from backend.utils.http_client import HTTPClient
from backend.models.opendrive.folder_models import (
    ListFolderResponse,
    RemoveFolderResponse,
    RenameFolderResponse,
)
from backend.models.opendrive.common_models import FolderInfo
from backend.core.config import OPENDRIVE_BASE_URL
from backend.core.opendrive_interface import IFolderService


class FolderService(IFolderService):
    def __init__(self):
        self.base_url = OPENDRIVE_BASE_URL
        self.http = HTTPClient(base_url=self.base_url)

    async def create_new_folder(
        self,
        session_id: str,
        folder_name: str,
        folder_sub_parent: str,
        folder_is_public: int,
        folder_public_upl: int,
        folder_public_display: int,
        folder_public_dnl: int,
        folder_description: str = "",
    ) -> dict:
        json_data = {
            "session_id": session_id,
            "folder_name": folder_name,
            "folder_sub_parent": folder_sub_parent,
            "folder_is_public": folder_is_public,
            "folder_public_upl": folder_public_upl,
            "folder_public_display": folder_public_display,
            "folder_public_dnl": folder_public_dnl,
            "folder_description": folder_description,
        }
        response = await self.http.post("/folder.json", json=json_data)
        return response.json()

    async def list_folder(self, session_id: str, folder_id: str) -> ListFolderResponse:
        url = f"/folder/list.json/{session_id}/{folder_id}"
        response = await self.http.get(url)
        response.raise_for_status()
        print("list_folder response:", response.json())
        data = response.json()

        # Parse the folders data using the folderInfo model.
        if "Folders" in data and data["Folders"]:
            parsed_folders = [FolderInfo(**folder) for folder in data["Folders"]]
            data["Folders"] = parsed_folders

        return ListFolderResponse.model_validate(data)

    async def remove_folder(
        self, session_id: str, folder_id: str
    ) -> RemoveFolderResponse:
        request_data = {
            "folder_id": folder_id,
            "session_id": session_id,
        }
        response = await self.http.post("/folder/remove.json", json=request_data)
        response.raise_for_status()
        print("remove_folder response:", response.json())
        return RemoveFolderResponse(**response.json())

    async def rename_folder(
        self, session_id: str, folder_id: str, folder_name: str
    ) -> RenameFolderResponse:
        request_data = {
            "session_id": session_id,
            "folder_id": folder_id,
            "folder_name": folder_name,
        }
        response = await self.http.post("/folder/rename.json", json=request_data)
        response.raise_for_status()
        print("rename_folder response:", response.json())
        return RenameFolderResponse(**response.json())
