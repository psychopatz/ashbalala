# routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
import aiofiles
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload_ebook/")
async def upload_ebook(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400, detail="Only .txt files are supported for now."
        )

    # Save the uploaded eBook file
    ebook_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    async with aiofiles.open(ebook_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return {"message": "eBook uploaded successfully", "file_path": ebook_path}
