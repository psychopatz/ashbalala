from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import Optional
from backend.services.opendrive_service import OpenDriveService
from backend.models.opendrive import (
    LoginRequest, SessionCheckRequest, SessionCheckResponse,
    CheckFileExistsRequest, CheckFileExistsResponse,
    CreateFileRequest, 
    OpenFileUploadRequest, 
    UploadFileChunkRequest, 
    CloseFileUploadRequest,
    ListFolderRequest, ListFolderResponse
)
import os
import uuid
router = APIRouter()

def get_opendrive_service():
    return OpenDriveService()

@router.post("/login")
async def login(
    login_request: LoginRequest = Depends(),
    service: OpenDriveService = Depends(get_opendrive_service)
):
    if login_request.session_id:
        service.session_id = login_request.session_id
        return {"message": "Session ID set", "session_id": service.session_id}
    else:
        login_details = await service.login()
        return login_details

@router.post("/session/check")
async def check_session(
    session_check: SessionCheckRequest = Depends(),
    service: OpenDriveService = Depends(get_opendrive_service)
) -> SessionCheckResponse:
    try:
        response = await service.check_session(session_check.session_id)
        return SessionCheckResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/newfolder")
async def create_new_folder(
    folder_name: str,
    folder_is_public: int = 0,
    folder_public_upl: int = 0,
    folder_public_display: int = 0,
    folder_public_dnl: int = 0,
    folder_description: str = "",
    folder_sub_parent: Optional[str] = None,
    service: OpenDriveService = Depends(get_opendrive_service)
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

@router.post("/check_file_exists", response_model=CheckFileExistsResponse)
async def check_file_exists(
    request: CheckFileExistsRequest,
    service: OpenDriveService = Depends(get_opendrive_service)
):
    try:
        result = await service.check_file_exists(
            folder_id=request.folder_id,
            session_id=request.session_id,
            names=request.name
        )
        return CheckFileExistsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload_file")
async def upload_file(
    session_id: str,
    folder_id: str,
    dest_file_name: str,
    file: UploadFile = File(...),
    service: OpenDriveService = Depends(get_opendrive_service)
):
    try:
        file_size = file.size
        # 1. Create File
        create_file_request = CreateFileRequest(
            session_id=session_id,
            folder_id=folder_id,
            file_name=dest_file_name,
            file_size=file_size,
            open_if_exists=1 # Use open_if_exists to handle duplicate names
        )
        create_file_response = await service.create_file(create_file_request)
        file_id = create_file_response.FileId
        file_time = create_file_response.DirUpdateTime if create_file_response.DirUpdateTime else int(os.time())

        # 2. Open File for Upload
        open_file_request = OpenFileUploadRequest(
            session_id=session_id,
            file_id=file_id,
            file_size=file_size
        )
        open_file_response = await service.open_file_upload(open_file_request)
        temp_location = open_file_response.TempLocation

        # 3. Upload Chunks
        chunk_offset = 0
        chunk_size = 50 * 1024 * 1024 # 50MB
        
        while True:
            chunk = await file.read(chunk_size)
            chunk_length = len(chunk)

            if chunk_length == 0:
                break

             # Create a temporary file to hold the chunk
            temp_file_path = f"{uuid.uuid4()}.tmp"
            with open(temp_file_path, "wb") as temp_file:
                  temp_file.write(chunk)

            upload_chunk_request = UploadFileChunkRequest(
                session_id = session_id,
                file_id = file_id,
                temp_location = temp_location,
                chunk_offset = chunk_offset,
                chunk_size = chunk_length
            )

            upload_chunk_response = await service.upload_file_chunk(upload_chunk_request, temp_file_path)
            if upload_chunk_response.TotalWritten != chunk_length:
                  raise HTTPException(status_code=500, detail="Chunk upload failed")
            
            os.remove(temp_file_path)
            chunk_offset += chunk_length
        

        # 4. Close File Upload
        close_file_request = CloseFileUploadRequest(
            session_id=session_id,
            file_id=file_id,
            file_size=file_size,
            temp_location=temp_location,
            file_time=file_time,
            access_folder_id="0", # default root folder
            file_compressed=0, # not compressed
            file_hash="", # not provided
            sharing_id=""  # no sharing id
        )
        close_file_response = await service.close_file_upload(close_file_request)
        return {
            "message": "File uploaded successfully",
            "result": close_file_response
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/folder/list", response_model=ListFolderResponse)
async def list_folder(
    request: ListFolderRequest,
    service: OpenDriveService = Depends(get_opendrive_service)
):
    try:
        result = await service.list_folder(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))