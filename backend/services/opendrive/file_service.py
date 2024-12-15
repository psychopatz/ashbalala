# /backend/services/opendrive/file_service.py
from backend.utils.http_client import HTTPClient
from backend.models.opendrive.file_models import (
    CreateFileResponse,
    OpenFileUploadResponse,
    UploadFileChunkResponse,
    CloseFileUploadResponse,
    RetrieveThumbResponse,
    RemoveDeleteResponse,
    RenameFileResponse,
)
from backend.core.config import OPENDRIVE_BASE_URL
from backend.core.opendrive_interface import IFileService
import os


class FileService(IFileService):
    def __init__(self):
        self.base_url = OPENDRIVE_BASE_URL
        self.http = HTTPClient(base_url=self.base_url)
        self.session_id = None

    async def check_file_exists(
        self, folder_id: str, session_id: str, names: list
    ) -> dict:
        endpoint = f"/upload/checkfileexistsbyname.json/{folder_id}"
        json_data = {"session_id": session_id, "name": names}
        response = await self.http.post(endpoint, json=json_data)
        return response.json()

    async def create_file(
        self, session_id: str, folder_id: str, file_name: str, file_size: int
    ) -> CreateFileResponse:
        request_data = {
            "session_id": session_id,
            "folder_id": folder_id,
            "file_name": file_name,
            "file_size": file_size,
            "open_if_exists": 1,
        }
        response = await self.http.post("/upload/create_file.json", json=request_data)
        response.raise_for_status()
        print("create_file response:", response.json())
        return CreateFileResponse(**response.json())

    async def open_file_upload(
        self, session_id: str, file_id: str, file_size: int
    ) -> OpenFileUploadResponse:
        request_data = {
            "session_id": session_id,
            "file_id": file_id,
            "file_size": file_size,
        }
        response = await self.http.post(
            "/upload/open_file_upload.json", json=request_data
        )
        response.raise_for_status()
        print("open_file_upload response:", response.json())
        return OpenFileUploadResponse(**response.json())

    async def upload_file_chunk(
        self,
        session_id: str,
        file_id: str,
        temp_location: str,
        chunk_offset: int,
        chunk_size: int,
        file_path: str,
    ) -> UploadFileChunkResponse:
        with open(file_path, "rb") as file:
            files = {"file_data": file}
            data = {
                "session_id": session_id,
                "file_id": file_id,
                "temp_location": temp_location,
                "chunk_offset": chunk_offset,
                "chunk_size": chunk_size,
            }
            response = await self.http.post(
                "/upload/upload_file_chunk.json", data=data, files=files
            )
        response.raise_for_status()
        print("upload_file_chunk response:", response.json())
        return UploadFileChunkResponse(**response.json())

    async def close_file_upload(
        self,
        session_id: str,
        file_id: str,
        file_size: int,
        temp_location: str,
        file_time: int,
    ) -> CloseFileUploadResponse:
        request_data = {
            "session_id": session_id,
            "file_id": file_id,
            "file_size": file_size,
            "temp_location": temp_location,
            "file_time": file_time,
            "access_folder_id": "0",
            "file_compressed": 0,
            "file_hash": "",
            "sharing_id": "",
        }
        response = await self.http.post(
            "/upload/close_file_upload.json", json=request_data
        )
        response.raise_for_status()
        print("close_file_upload response:", response.json())
        return response.json()

    async def retrieve_thumb(
        self, session_id: str, file_id: str
    ) -> RetrieveThumbResponse:
        endpoint = f"/file/thumb.json/{file_id}"
        params = {"session_id": session_id}
        response = await self.http.get(endpoint, params=params)

        return RetrieveThumbResponse(
            content=response.content, content_type=response.headers.get("content-type")
        )

    async def remove_delete(
        self, session_id: str, file_id: str, access_folder_id: str = ""
    ) -> RemoveDeleteResponse:
        url = f"/file.json/{session_id}/{file_id}"
        params = {}
        if access_folder_id:
            params["access_folder_id"] = access_folder_id

        response = await self.http.delete(url, params=params)
        response.raise_for_status()
        return RemoveDeleteResponse(success=True)

    async def rename_file(
        self,
        session_id: str,
        new_file_name: str,
        file_id: str,
        access_folder_id: str = "",
    ) -> RenameFileResponse:
        url = "/file/rename.json"
        request_data = {
            "session_id": session_id,
            "new_file_name": new_file_name,
            "file_id": file_id,
            "access_folder_id": access_folder_id,
        }
        response = await self.http.post(url, json=request_data)
        response.raise_for_status()
        return RenameFileResponse(success=True, message="File renamed successfully")
