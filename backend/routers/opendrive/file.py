from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Response
import os
import uuid
from backend.services.opendrive.file_service import FileService
from backend.models.opendrive.file_models import (
    CheckFileExistsRequest,
    CheckFileExistsResponse,
    CreateFileRequest,
    OpenFileUploadRequest,
    UploadFileChunkRequest,
    CloseFileUploadRequest,
)
from backend.core.opendrive_interface import IFileService

router = APIRouter()


def get_file_service() -> IFileService:
    return FileService()


@router.post("/check_file_exists", response_model=CheckFileExistsResponse)
async def check_file_exists(
    request: CheckFileExistsRequest, service: IFileService = Depends(get_file_service)
):
    try:
        result = await service.check_file_exists(
            folder_id=request.folder_id,
            session_id=request.session_id,
            names=request.name,
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
    service: IFileService = Depends(get_file_service),
):
    try:
        file_size = file.size
        # 1. Create File
        create_file_response = await service.create_file(
            session_id=session_id,
            folder_id=folder_id,
            file_name=dest_file_name,
            file_size=file_size,
        )
        file_id = create_file_response.FileId
        file_time = (
            create_file_response.DirUpdateTime
            if create_file_response.DirUpdateTime
            else int(os.time())
        )

        # 2. Open File for Upload
        open_file_response = await service.open_file_upload(
            session_id=session_id, file_id=file_id, file_size=file_size
        )
        temp_location = open_file_response.TempLocation

        # 3. Upload Chunks
        chunk_offset = 0
        chunk_size = 50 * 1024 * 1024  # 50MB

        while True:
            chunk = await file.read(chunk_size)
            chunk_length = len(chunk)

            if chunk_length == 0:
                break

            # Create a temporary file to hold the chunk
            temp_file_path = f"{uuid.uuid4()}.tmp"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(chunk)

            upload_chunk_response = await service.upload_file_chunk(
                session_id=session_id,
                file_id=file_id,
                temp_location=temp_location,
                chunk_offset=chunk_offset,
                chunk_size=chunk_length,
                file_path=temp_file_path,
            )
            if upload_chunk_response.TotalWritten != chunk_length:
                raise HTTPException(status_code=500, detail="Chunk upload failed")

            os.remove(temp_file_path)
            chunk_offset += chunk_length

        # 4. Close File Upload
        close_file_response = await service.close_file_upload(
            session_id=session_id,
            file_id=file_id,
            file_size=file_size,
            temp_location=temp_location,
            file_time=file_time,
        )
        return {"message": "File uploaded successfully", "result": close_file_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/file/{file_id}/thumbnail")
async def get_file_thumbnail(
    file_id: str, session_id: str, service: IFileService = Depends(get_file_service)
):
    try:
        thumbnail_response = await service.retrieve_thumb(
            session_id=session_id, file_id=file_id
        )
        return Response(
            content=thumbnail_response.content,
            media_type=thumbnail_response.content_type,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
