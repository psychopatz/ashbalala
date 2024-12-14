from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from backend.services.opendrive.folder_service import FolderService
from backend.models.opendrive.folder_models import (
   ListFolderRequest, ListFolderResponse,
   RemoveFolderRequest, RemoveFolderResponse
)
from backend.core.opendrive_interface import IFolderService

router = APIRouter()

def get_folder_service() -> IFolderService:
    return FolderService()

@router.post("/newfolder")
async def create_new_folder(
    folder_name: str,
    folder_is_public: int = 0,
    folder_public_upl: int = 0,
    folder_public_display: int = 0,
    folder_public_dnl: int = 0,
    folder_description: str = "",
    folder_sub_parent: Optional[str] = None,
    service: IFolderService = Depends(get_folder_service)
):
    try:
        if folder_sub_parent is None:
            folder_sub_parent = "0"  # root folder
        response = await service.create_new_folder(
            folder_name=folder_name,
            folder_sub_parent=folder_sub_parent,
            folder_is_public=folder_is_public,
            folder_public_upl=folder_public_upl,
            folder_public_display=folder_public_display,
            folder_public_dnl=folder_public_dnl,
            folder_description=folder_description,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/list", response_model=ListFolderResponse)
async def list_folder(
    request: ListFolderRequest,
    service: IFolderService = Depends(get_folder_service)
):
    try:
        result = await service.list_folder(request.folder_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remove", response_model=RemoveFolderResponse)
async def remove_folder(
    folder_id: str,
    service: IFolderService = Depends(get_folder_service)
):
  try:
      result = await service.remove_folder(folder_id)
      return result
  except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))