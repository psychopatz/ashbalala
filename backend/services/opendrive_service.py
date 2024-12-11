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

    async def upload_file(self, folder_id: str, file_path: str):
        await self.ensure_session()
        file_name = os.path.basename(file_path)

        async with aiofiles.open(file_path, 'rb') as f:
            files = {
                "file": (file_name, await f.read(), "application/octet-stream")
            }

        data = {
            "session_id": self.session_id,
            "folder_id": folder_id,
            "overwrite": "true"
        }

        # Upload endpoint: /upload.json
        response = await self.http.client.post(
            f"{self.base_url}/upload.json", 
            data=data, 
            files=files
        )
        response.raise_for_status()
        upload_data = UploadResponse(**response.json())
        return upload_data.FileId

    async def get_download_link(self, file_id: str):
        await self.ensure_session()
        params = {
            "session_id": self.session_id,
            "file_id": file_id
        }
        response = await self.http.get("/file/download_link.json", params=params)
        download_data = DownloadLinkResponse(**response.json())
        return download_data.DownloadLink

    async def download_file(self, file_id: str, dest_path: str):
        link = await self.get_download_link(file_id)

        async with self.http.client as client:
            r = await client.get(link)
            r.raise_for_status()
            async with aiofiles.open(dest_path, 'wb') as f:
                await f.write(r.content)

        return dest_path

    async def create_folder(self, parent_id: str, folder_name: str):
        await self.ensure_session()
        json_data = {
            "session_id": self.session_id,
            "folder_name": folder_name,
            "parent_id": parent_id
        }
        response = await self.http.post("/folder.json", json=json_data)
        return response.json()

    async def get_folder_content(self, folder_id: str):
        await self.ensure_session()
        params = {
            "session_id": self.session_id,
            "folder_id": folder_id
        }
        response = await self.http.get("/folder/list.json", params=params)
        return response.json()
