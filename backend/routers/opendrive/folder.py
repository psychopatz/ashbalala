from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from backend.services.opendrive.folder_service import FolderService
from backend.models.opendrive.folder_models import (
    ListFolderRequest,
    ListFolderResponse,
    RemoveFolderRequest,
    RemoveFolderResponse,
    RenameFolderRequest,
    RenameFolderResponse,
    CreateFolderRequest,
)
from backend.core.opendrive_interface import IFolderService

router = APIRouter()


def get_folder_service() -> IFolderService:
    return FolderService()


@router.post("/newfolder")
async def create_new_folder(
    request: CreateFolderRequest,
    service: IFolderService = Depends(get_folder_service),
):
    try:
        response = await service.create_new_folder(
            session_id=request.session_id,
            folder_name=request.folder_name,
            folder_sub_parent=request.folder_sub_parent,
            folder_is_public=request.folder_is_public,
            folder_public_upl=request.folder_public_upl,
            folder_public_display=request.folder_public_display,
            folder_public_dnl=request.folder_public_dnl,
            folder_description=request.folder_description,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/list", response_model=ListFolderResponse)
async def list_folder(
    request: ListFolderRequest, service: IFolderService = Depends(get_folder_service)
):
    try:
        result = await service.list_folder(
            session_id=request.session_id, folder_id=request.folder_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/remove", response_model=RemoveFolderResponse)
async def remove_folder(
    request: RemoveFolderRequest, service: IFolderService = Depends(get_folder_service)
):
    try:
        result = await service.remove_folder(
            session_id=request.session_id, folder_id=request.folder_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rename", response_model=RenameFolderResponse)
async def rename_folder(
    request: RenameFolderRequest, service: IFolderService = Depends(get_folder_service)
):
    try:
        result = await service.rename_folder(
            session_id=request.session_id,
            folder_id=request.folder_id,
            folder_name=request.folder_name,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
