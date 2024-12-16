# /backend/services/audiobook/chapter_service.py
from sqlalchemy.orm import Session
from models.audiobook.chapter_model import Chapter
from sqlalchemy import exc


def create_chapter(db: Session, chapter: dict):
    try:
        db_chapter = Chapter(**chapter)
        db.add(db_chapter)
        db.commit()
        db.refresh(db_chapter)
        return db_chapter
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def get_chapter(db: Session, chapter_id: int):
    try:
        return db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def get_chapters(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Chapter).offset(skip).limit(limit).all()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def update_chapter(db: Session, chapter_id: int, chapter: dict):
    try:
        db_chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
        if db_chapter:
            for key, value in chapter.items():
                setattr(db_chapter, key, value)
            db.commit()
            db.refresh(db_chapter)
            return db_chapter
        return None
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def delete_chapter(db: Session, chapter_id: int):
    try:
        db_chapter = db.query(Chapter).filter(Chapter.chapter_id == chapter_id).first()
        if db_chapter:
            db.delete(db_chapter)
            db.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")
