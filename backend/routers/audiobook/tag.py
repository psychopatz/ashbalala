# /backend/routers/audiobook/tag.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.config import get_db
from services.audiobook import tag_service
from pydantic import BaseModel


router = APIRouter()


class AudiobookTagCreate(BaseModel):
    audiobook_id: int
    tag_name: str


class AudiobookTagUpdate(BaseModel):
    tag_name: str | None = None


class AudiobookTagResponse(BaseModel):
    tag_id: int
    audiobook_id: int
    tag_name: str


@router.post("/", response_model=AudiobookTagResponse, status_code=201)
def create_audiobook_tag(
    audiobook_tag: AudiobookTagCreate, db: Session = Depends(get_db)
):
    try:
        return tag_service.create_audiobook_tag(db, audiobook_tag.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tag_id}", response_model=AudiobookTagResponse)
def get_audiobook_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        db_audiobook_tag = tag_service.get_audiobook_tag(db, tag_id)
        if db_audiobook_tag is None:
            raise HTTPException(status_code=404, detail="Audiobook Tag not found")
        return db_audiobook_tag
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[AudiobookTagResponse])
def get_audiobook_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return tag_service.get_audiobook_tags(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{tag_id}", response_model=AudiobookTagResponse)
def update_audiobook_tag(
    tag_id: int, audiobook_tag: AudiobookTagUpdate, db: Session = Depends(get_db)
):
    try:
        updated_audiobook_tag = tag_service.update_audiobook_tag(
            db, tag_id, audiobook_tag.dict(exclude_unset=True)
        )
        if updated_audiobook_tag is None:
            raise HTTPException(status_code=404, detail="Audiobook Tag not found")
        return updated_audiobook_tag
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{tag_id}", status_code=204)
def delete_audiobook_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        if not tag_service.delete_audiobook_tag(db, tag_id):
            raise HTTPException(status_code=404, detail="Audiobook Tag not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
