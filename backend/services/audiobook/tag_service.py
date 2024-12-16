# /backend/services/audiobook/tag_service.py

from sqlalchemy.orm import Session
from models.audiobook.tag_model import AudiobookTag
from sqlalchemy import exc


def create_audiobook_tag(db: Session, audiobook_tag: dict):
    try:
        db_audiobook_tag = AudiobookTag(**audiobook_tag)
        db.add(db_audiobook_tag)
        db.commit()
        db.refresh(db_audiobook_tag)
        return db_audiobook_tag
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def get_audiobook_tag(db: Session, tag_id: int):
    try:
        return db.query(AudiobookTag).filter(AudiobookTag.tag_id == tag_id).first()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def get_audiobook_tags(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(AudiobookTag).offset(skip).limit(limit).all()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def update_audiobook_tag(db: Session, tag_id: int, audiobook_tag: dict):
    try:
        db_audiobook_tag = (
            db.query(AudiobookTag).filter(AudiobookTag.tag_id == tag_id).first()
        )
        if db_audiobook_tag:
            for key, value in audiobook_tag.items():
                setattr(db_audiobook_tag, key, value)
            db.commit()
            db.refresh(db_audiobook_tag)
            return db_audiobook_tag
        return None
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def delete_audiobook_tag(db: Session, tag_id: int):
    try:
        db_audiobook_tag = (
            db.query(AudiobookTag).filter(AudiobookTag.tag_id == tag_id).first()
        )
        if db_audiobook_tag:
            db.delete(db_audiobook_tag)
            db.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")
