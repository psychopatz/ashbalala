import os
import aiofiles
from backend.utils.http_client import HTTPClient
from backend.models.opendrive import LoginResponse, UploadResponse, DownloadLinkResponse
from backend.core.config import OPENDRIVE_BASE_URL, OPENDRIVE_USERNAME, OPENDRIVE_PASSWORD

class OpenDriveService:
    def __init__(self):
        self.base_url = OPENDRIVE_BASE_URL
        self.username = OPENDRIVE_USERNAME
        self.password = OPENDRIVE_PASSWORD
        self.http = HTTPClient(base_url=self.base_url)
        self.session_id = None

    async def login(self):
        data = {
            "username": self.username,
            "passwd": self.password
        }
        response = await self.http.post("/session/login.json", json=data)
        response.raise_for_status()
        login_data = LoginResponse(**response.json())
        self.session_id = login_data.SessionID
        return login_data


    async def ensure_session(self):
        if not self.session_id:
            await self.login()


    async def create_new_folder(
        self,
        folder_name: str,
        folder_sub_parent: str,
        folder_is_public: int,
        folder_public_upl: int,
        folder_public_display: int,
        folder_public_dnl: int,
        folder_description: str = "",
        ):
        """
        Creates a new folder with advanced options.
        """
        await self.ensure_session()
        json_data = {
            "session_id": self.session_id,
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
    
    