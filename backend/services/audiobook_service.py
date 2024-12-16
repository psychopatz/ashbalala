from sqlalchemy.orm import Session
from models.audiobook_model import Audiobook
from sqlalchemy import exc


def create_audiobook(db: Session, audiobook: dict):
    try:
        db_audiobook = Audiobook(**audiobook)
        db.add(db_audiobook)
        db.commit()
        db.refresh(db_audiobook)
        return db_audiobook
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def get_audiobook(db: Session, audiobook_id: int):
    try:
        return (
            db.query(Audiobook).filter(Audiobook.audiobook_id == audiobook_id).first()
        )
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def get_audiobooks(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Audiobook).offset(skip).limit(limit).all()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def update_audiobook(db: Session, audiobook_id: int, audiobook: dict):
    try:
        db_audiobook = (
            db.query(Audiobook).filter(Audiobook.audiobook_id == audiobook_id).first()
        )
        if db_audiobook:
            for key, value in audiobook.items():
                setattr(db_audiobook, key, value)
            db.commit()
            db.refresh(db_audiobook)
            return db_audiobook
        return None
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def delete_audiobook(db: Session, audiobook_id: int):
    try:
        db_audiobook = (
            db.query(Audiobook).filter(Audiobook.audiobook_id == audiobook_id).first()
        )
        if db_audiobook:
            db.delete(db_audiobook)
            db.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")
