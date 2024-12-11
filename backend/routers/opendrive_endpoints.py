from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.opendrive_service import OpenDriveService
import os
import uuid

router = APIRouter()
service = OpenDriveService()

@router.post("/login")
async def login():
    login_details = await service.login()
    return login_details


@router.post("/upload")
async def upload_file(folder_id: str, file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_filename = f"/tmp/{uuid.uuid4()}_{file.filename}"
        with open(temp_filename, "wb") as f:
            content = await file.read()
            f.write(content)
        file_id = await service.upload_file(folder_id=folder_id, file_path=temp_filename)
        os.remove(temp_filename)
        return {"file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download")
async def download_file(file_id: str):
    try:
        # Download to a temp location
        temp_filename = f"/tmp/{uuid.uuid4()}_download"
        dest_path = await service.download_file(file_id=file_id, dest_path=temp_filename)
        # Normally you'd return the file content directly. For a real API,
        # you might return a StreamingResponse. Here we just say where we saved it.
        # For demonstration, just return the path.
        return {"downloaded_file": dest_path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/folder")
async def create_folder(parent_id: str, folder_name: str):
    try:
        response = await service.create_folder(parent_id=parent_id, folder_name=folder_name)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/folder/content")
async def get_folder_content(folder_id: str):
    try:
        response = await service.get_folder_content(folder_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/all_files")
async def get_all_files():
    try:
        # Use the root_folder_id obtained from login
        await service.ensure_session()
        response = await service.get_folder_content(service.root_folder_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
