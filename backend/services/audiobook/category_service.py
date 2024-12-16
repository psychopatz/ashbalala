# /backend/services/audiobook/category_service.py
from sqlalchemy.orm import Session
from models.audiobook.category_model import Category
from sqlalchemy import exc


def create_category(db: Session, category: dict):
    try:
        db_category = Category(**category)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def get_category(db: Session, category_id: int):
    try:
        return db.query(Category).filter(Category.category_id == category_id).first()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Category).offset(skip).limit(limit).all()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def update_category(db: Session, category_id: int, category: dict):
    try:
        db_category = (
            db.query(Category).filter(Category.category_id == category_id).first()
        )
        if db_category:
            for key, value in category.items():
                setattr(db_category, key, value)
            db.commit()
            db.refresh(db_category)
            return db_category
        return None
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def delete_category(db: Session, category_id: int):
    try:
        db_category = (
            db.query(Category).filter(Category.category_id == category_id).first()
        )
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")
