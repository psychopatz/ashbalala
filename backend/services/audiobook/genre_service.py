# /backend/services/audiobook/genre_service.py
from sqlalchemy.orm import Session
from models.audiobook.genre_model import Genre
from sqlalchemy import exc


def create_genre(db: Session, genre: dict):
    try:
        db_genre = Genre(**genre)
        db.add(db_genre)
        db.commit()
        db.refresh(db_genre)
        return db_genre
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def get_genre(db: Session, genre_id: int):
    try:
        return db.query(Genre).filter(Genre.genre_id == genre_id).first()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def get_genres(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Genre).offset(skip).limit(limit).all()
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def update_genre(db: Session, genre_id: int, genre: dict):
    try:
        db_genre = db.query(Genre).filter(Genre.genre_id == genre_id).first()
        if db_genre:
            for key, value in genre.items():
                setattr(db_genre, key, value)
            db.commit()
            db.refresh(db_genre)
            return db_genre
        return None
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def delete_genre(db: Session, genre_id: int):
    try:
        db_genre = db.query(Genre).filter(Genre.genre_id == genre_id).first()
        if db_genre:
            db.delete(db_genre)
            db.commit()
            return True
        return False
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")
