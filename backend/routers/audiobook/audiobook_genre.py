# backend/routers/audiobook/audiobook_genre.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.config import get_db
from services.audiobook import audiobook_genre_service
from pydantic import BaseModel


router = APIRouter()


class AudiobookGenreCreate(BaseModel):
    audiobook_id: int
    genre_id: int


class AudiobookGenreResponse(BaseModel):
    audiobook_genre_id: int
    audiobook_id: int
    genre_id: int


@router.post("/", response_model=AudiobookGenreResponse, status_code=201)
def create_audiobook_genre(
    audiobook_genre: AudiobookGenreCreate, db: Session = Depends(get_db)
):
    try:
        return audiobook_genre_service.create_audiobook_genre(
            db, audiobook_genre.audiobook_id, audiobook_genre.genre_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{audiobook_genre_id}", response_model=AudiobookGenreResponse)
def get_audiobook_genre(audiobook_genre_id: int, db: Session = Depends(get_db)):
    try:
        db_audiobook_genre = audiobook_genre_service.get_audiobook_genre(
            db, audiobook_genre_id
        )
        if db_audiobook_genre is None:
            raise HTTPException(status_code=404, detail="Audiobook Genre not found")
        return db_audiobook_genre
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[AudiobookGenreResponse])
def get_audiobook_genres(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        return audiobook_genre_service.get_audiobook_genres(
            db, skip=skip, limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{audiobook_genre_id}", status_code=204)
def delete_audiobook_genre(audiobook_genre_id: int, db: Session = Depends(get_db)):
    try:
        if not audiobook_genre_service.delete_audiobook_genre(
            db, audiobook_genre_id
        ):
            raise HTTPException(status_code=404, detail="Audiobook Genre not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audiobook/{audiobook_id}", response_model =List[AudiobookGenreResponse] )
def get_genres_by_audiobook_id(audiobook_id: int, db: Session = Depends(get_db)):
     try:
        db_audiobook_genres = audiobook_genre_service.get_genres_by_audiobook_id(
            db, audiobook_id
        )
        if db_audiobook_genres is None:
            raise HTTPException(status_code=404, detail="Audiobook Genre not found")
        return db_audiobook_genres
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))