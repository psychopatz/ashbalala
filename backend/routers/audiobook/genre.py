# /backend/routers/audiobook/genre.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.config import get_db
from services.audiobook import genre_service
from pydantic import BaseModel


router = APIRouter()


class GenreCreate(BaseModel):
    name: str


class GenreUpdate(BaseModel):
    name: str | None = None


class GenreResponse(BaseModel):
    genre_id: int
    name: str


@router.post("/", response_model=GenreResponse, status_code=201)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    try:
        return genre_service.create_genre(db, genre.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    try:
        db_genre = genre_service.get_genre(db, genre_id)
        if db_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return db_genre
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[GenreResponse])
def get_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return genre_service.get_genres(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(genre_id: int, genre: GenreUpdate, db: Session = Depends(get_db)):
    try:
        updated_genre = genre_service.update_genre(
            db, genre_id, genre.dict(exclude_unset=True)
        )
        if updated_genre is None:
            raise HTTPException(status_code=404, detail="Genre not found")
        return updated_genre
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{genre_id}", status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    try:
        if not genre_service.delete_genre(db, genre_id):
            raise HTTPException(status_code=404, detail="Genre not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
