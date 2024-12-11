from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.opendrive_service import OpenDriveService
from typing import Optional
import os
import uuid
import aiofiles

router = APIRouter()
service = OpenDriveService()

@router.post("/login")
async def login():
    login_details = await service.login()
    return login_details

@router.post("/newfolder")
async def create_new_folder(
    folder_name: str,
    folder_is_public: int = 0,
    folder_public_upl: int = 0,
    folder_public_display: int = 0,
    folder_public_dnl: int = 0,
    folder_description: str = "",
    folder_sub_parent: Optional[str] = None,
):
    """
    Endpoint to create a new folder with advanced options.
    """
    try:
        # Handle optional folder_sub_parent:
        if folder_sub_parent is None:
            folder_sub_parent = "0"  # Set to "0" for root folder

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