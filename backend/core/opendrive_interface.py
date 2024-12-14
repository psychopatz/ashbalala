from typing import Protocol, List
from backend.models.opendrive.common_models import FileInfo, FolderInfo
from backend.models.opendrive.auth_models import LoginResponse
from backend.models.opendrive.folder_models import (
    ListFolderResponse,
    RemoveFolderResponse,
)
from backend.models.opendrive.file_models import (
    CreateFileResponse,
    OpenFileUploadResponse,
    UploadFileChunkResponse,
    CloseFileUploadResponse,
    RetrieveThumbResponse,
)


class IAuthService(Protocol):
    async def login(self) -> LoginResponse: ...
    async def check_session(self, session_id: str) -> dict: ...
    async def ensure_session(self) -> None: ...


class IFolderService(Protocol):
    async def create_new_folder(
        self,
        folder_name: str,
        folder_sub_parent: str,
        folder_is_public: int,
        folder_public_upl: int,
        folder_public_display: int,
        folder_public_dnl: int,
        folder_description: str = "",
    ) -> dict: ...
    async def list_folder(self, folder_id: str) -> ListFolderResponse: ...
    async def remove_folder(self, folder_id: str) -> RemoveFolderResponse: ...


class IFileService(Protocol):
    async def check_file_exists(
        self, folder_id: str, session_id: str, names: List[str]
    ) -> dict: ...
    async def create_file(
        self, session_id: str, folder_id: str, file_name: str, file_size: int
    ) -> CreateFileResponse: ...
    async def open_file_upload(
        self, session_id: str, file_id: str, file_size: int
    ) -> OpenFileUploadResponse: ...
    async def upload_file_chunk(
        self,
        session_id: str,
        file_id: str,
        temp_location: str,
        chunk_offset: int,
        chunk_size: int,
        file_path: str,
    ) -> UploadFileChunkResponse: ...
    async def close_file_upload(
        self,
        session_id: str,
        file_id: str,
        file_size: int,
        temp_location: str,
        file_time: int,
    ) -> CloseFileUploadResponse: ...
    async def retrieve_thumb(
        self, session_id: str, file_id: str
    ) -> RetrieveThumbResponse: ...
