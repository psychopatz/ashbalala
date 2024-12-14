from backend.utils.http_client import HTTPClient
from backend.models.opendrive.folder_models import (
    ListFolderResponse, RemoveFolderResponse
)
from backend.core.config import OPENDRIVE_BASE_URL
from backend.core.opendrive_interface import IFolderService

class FolderService(IFolderService):
    def __init__(self):
        self.base_url = OPENDRIVE_BASE_URL
        self.http = HTTPClient(base_url=self.base_url)
        self.session_id = None

    async def create_new_folder(
        self,
        folder_name: str,
        folder_sub_parent: str,
        folder_is_public: int,
        folder_public_upl: int,
        folder_public_display: int,
        folder_public_dnl: int,
        folder_description: str = ""
    ) -> dict:
        from backend.services.opendrive.auth_service import AuthService
        auth_service = AuthService()
        await auth_service.ensure_session()
        json_data = {
            "session_id": auth_service.session_id,
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

    async def list_folder(self, folder_id: str) -> ListFolderResponse:
        from backend.services.opendrive.auth_service import AuthService
        auth_service = AuthService()
        await auth_service.ensure_session()
        url = f"/folder/list.json/{auth_service.session_id}/{folder_id}"
        response = await self.http.get(url)
        response.raise_for_status()
        print("list_folder response:", response.json())
        
        # Parse the response using model_validate
        data = response.json()
        return ListFolderResponse.model_validate(data)
    
    async def remove_folder(self, folder_id: str) -> RemoveFolderResponse:
        from backend.services.opendrive.auth_service import AuthService
        auth_service = AuthService()
        await auth_service.ensure_session()
        request_data = {
            "folder_id":folder_id,
            "session_id": auth_service.session_id
            }
        response = await self.http.post("/folder/remove.json", json=request_data)
        response.raise_for_status()
        print("remove_folder response:", response.json())
        return RemoveFolderResponse(**response.json())