# /backend/routers/audiobook/category.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.config import get_db
from services.audiobook import category_service
from pydantic import BaseModel


router = APIRouter()


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None = None


class CategoryResponse(BaseModel):
    category_id: int
    name: str


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return category_service.create_category(db, category.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        db_category = category_service.get_category(db, category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return db_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return category_service.get_categories(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)
):
    try:
        updated_category = category_service.update_category(
            db, category_id, category.dict(exclude_unset=True)
        )
        if updated_category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return updated_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        if not category_service.delete_category(db, category_id):
            raise HTTPException(status_code=404, detail="Category not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
