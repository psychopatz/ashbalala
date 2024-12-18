# /backend/core/opendrive_interface.py

from abc import ABC, abstractmethod
from models.opendrive.auth_models import LoginRequest, LoginResponse, UserInfoResponse
from models.opendrive.file_models import (
    CreateFileResponse,
    OpenFileUploadResponse,
    UploadFileChunkResponse,
    CloseFileUploadResponse,
    RetrieveThumbResponse,
    RemoveDeleteResponse,
    RenameFileResponse,
    ExpiringLinkResponse,  # Import the new model
)
from models.opendrive.folder_models import (
    ListFolderResponse,
    RemoveFolderResponse,
    RenameFolderResponse,
)


class IAuthService(ABC):
    @abstractmethod
    async def login(self, login_request: LoginRequest) -> LoginResponse:
        pass

    @abstractmethod
    async def check_session(self, session_id: str) -> dict:
        pass

    @abstractmethod
    async def get_user_info(self, session_id: str) -> UserInfoResponse:
        pass


class IFileService(ABC):
    @abstractmethod
    async def check_file_exists(
        self, folder_id: str, session_id: str, names: list
    ) -> dict:
        pass

    @abstractmethod
    async def create_file(
        self, session_id: str, folder_id: str, file_name: str, file_size: int
    ) -> CreateFileResponse:
        pass

    @abstractmethod
    async def open_file_upload(
        self, session_id: str, file_id: str, file_size: int
    ) -> OpenFileUploadResponse:
        pass

    @abstractmethod
    async def upload_file_chunk(
        self,
        session_id: str,
        file_id: str,
        temp_location: str,
        chunk_offset: int,
        chunk_size: int,
        file_path: str,
    ) -> UploadFileChunkResponse:
        pass

    @abstractmethod
    async def close_file_upload(
        self,
        session_id: str,
        file_id: str,
        file_size: int,
        temp_location: str,
        file_time: int,
    ) -> CloseFileUploadResponse:
        pass

    @abstractmethod
    async def retrieve_thumb(
        self, session_id: str, file_id: str
    ) -> RetrieveThumbResponse:
        pass

    @abstractmethod
    async def remove_delete(
        self, session_id: str, file_id: str, access_folder_id: str = ""
    ) -> RemoveDeleteResponse:
        pass

    @abstractmethod
    async def rename_file(
        self,
        session_id: str,
        new_file_name: str,
        file_id: str,
        access_folder_id: str = "",
    ) -> RenameFileResponse:
        pass

    @abstractmethod
    async def get_expiring_link(
        self, session_id: str, date: str, counter: int, file_id: str, enable: str
    ) -> ExpiringLinkResponse:
        pass


class IFolderService(ABC):
    @abstractmethod
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
        pass

    @abstractmethod
    async def list_folder(self, session_id: str, folder_id: str) -> ListFolderResponse:
        pass

    @abstractmethod
    async def remove_folder(
        self, session_id: str, folder_id: str
    ) -> RemoveFolderResponse:
        pass

    @abstractmethod
    async def rename_folder(
        self, session_id: str, folder_id: str, folder_name: str
    ) -> RenameFolderResponse:
        pass
