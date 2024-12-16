# /backend/routers/audiobook/chapter.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.config import get_db
from services.audiobook import chapter_service
from pydantic import BaseModel


router = APIRouter()


class ChapterCreate(BaseModel):
    audiobook_id: int
    title: str
    duration: float
    file_url: str
    sequence_number: int


class ChapterUpdate(BaseModel):
    title: str | None = None
    duration: float | None = None
    file_url: str | None = None
    sequence_number: int | None = None


class ChapterResponse(BaseModel):
    chapter_id: int
    audiobook_id: int
    title: str
    duration: float
    file_url: str
    sequence_number: int


@router.post("/", response_model=ChapterResponse, status_code=201)
def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db)):
    try:
        return chapter_service.create_chapter(db, chapter.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chapter_id}", response_model=ChapterResponse)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    try:
        db_chapter = chapter_service.get_chapter(db, chapter_id)
        if db_chapter is None:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return db_chapter
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ChapterResponse])
def get_chapters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return chapter_service.get_chapters(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{chapter_id}", response_model=ChapterResponse)
def update_chapter(
    chapter_id: int, chapter: ChapterUpdate, db: Session = Depends(get_db)
):
    try:
        updated_chapter = chapter_service.update_chapter(
            db, chapter_id, chapter.dict(exclude_unset=True)
        )
        if updated_chapter is None:
            raise HTTPException(status_code=404, detail="Chapter not found")
        return updated_chapter
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{chapter_id}", status_code=204)
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):
    try:
        if not chapter_service.delete_chapter(db, chapter_id):
            raise HTTPException(status_code=404, detail="Chapter not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
