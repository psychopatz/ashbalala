from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.config import get_db
from services import audiobook_service
from pydantic import BaseModel
from datetime import date

router = APIRouter()


class AudiobookCreate(BaseModel):
    title: str
    author: str
    narrator: str
    duration: float
    release_date: date
    description: str
    genre_id: int
    file_url: str
    cover_image_url: str


class AudiobookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    narrator: str | None = None
    duration: float | None = None
    release_date: date | None = None
    description: str | None = None
    genre_id: int | None = None
    file_url: str | None = None
    cover_image_url: str | None = None


class AudiobookResponse(BaseModel):
    audiobook_id: int
    title: str
    author: str
    narrator: str
    duration: float
    release_date: date
    description: str
    genre_id: int
    file_url: str
    cover_image_url: str


@router.post("/", response_model=AudiobookResponse, status_code=201)
def create_audiobook(audiobook: AudiobookCreate, db: Session = Depends(get_db)):
    try:
        return audiobook_service.create_audiobook(db, audiobook.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{audiobook_id}", response_model=AudiobookResponse)
def get_audiobook(audiobook_id: int, db: Session = Depends(get_db)):
    try:
        db_audiobook = audiobook_service.get_audiobook(db, audiobook_id)
        if db_audiobook is None:
            raise HTTPException(status_code=404, detail="Audiobook not found")
        return db_audiobook
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[AudiobookResponse])
def get_audiobooks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return audiobook_service.get_audiobooks(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{audiobook_id}", response_model=AudiobookResponse)
def update_audiobook(
    audiobook_id: int, audiobook: AudiobookUpdate, db: Session = Depends(get_db)
):
    try:
        updated_audiobook = audiobook_service.update_audiobook(
            db, audiobook_id, audiobook.dict(exclude_unset=True)
        )
        if updated_audiobook is None:
            raise HTTPException(status_code=404, detail="Audiobook not found")
        return updated_audiobook
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{audiobook_id}", status_code=204)
def delete_audiobook(audiobook_id: int, db: Session = Depends(get_db)):
    try:
        if not audiobook_service.delete_audiobook(db, audiobook_id):
            raise HTTPException(status_code=404, detail="Audiobook not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
