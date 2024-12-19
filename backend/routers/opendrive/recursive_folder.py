# /backend/routers/opendrive/recursive_folder.py

from fastapi import APIRouter, Depends, HTTPException
from core.config import get_db, ROOT_ID, AUDIOBOOK_ID
from services.opendrive.recursive_folder_service import RecursiveFolderService
from services.opendrive.folder_service import FolderService
from core.opendrive_interface import IFolderService
from models.opendrive.recursive_folder_model import RecursiveFolderResponse


router = APIRouter(
    prefix="/opendrive/recursive-folder", tags=["OpenDrive Recursive Folder"]
)


def get_folder_service() -> IFolderService:
    return FolderService()


@router.get("/{session_id}", response_model=RecursiveFolderResponse)
async def read_recursive_folder(
    session_id: str,
    folder_id: str = AUDIOBOOK_ID,
    folder_service: IFolderService = Depends(get_folder_service),
):
    recursive_folder_service = RecursiveFolderService(folder_service)
    try:
        return await recursive_folder_service.get_recursive_folder(
            session_id, folder_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
