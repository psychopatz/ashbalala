# backend/services/audiobook/audiobook_genre_service.py
from sqlalchemy.orm import Session
from models.audiobook.audiobook_genre_model import AudiobookGenre
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError, DataError, OperationalError


def create_audiobook_genre(db: Session, audiobook_id: int, genre_id: int):
    try:
        db_audiobook_genre = AudiobookGenre(audiobook_id=audiobook_id, genre_id=genre_id)
        db.add(db_audiobook_genre)
        db.commit()
        db.refresh(db_audiobook_genre)
        return db_audiobook_genre
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Database integrity error: {e}")
    except DataError as e:
        db.rollback()
        raise Exception(f"Database data error: {e}")
    except OperationalError as e:
        db.rollback()
        raise Exception(f"Database operational error: {e}")
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")


def get_audiobook_genre(db: Session, audiobook_genre_id: int):
    try:
       return db.query(AudiobookGenre).filter(AudiobookGenre.audiobook_genre_id == audiobook_genre_id).first()
    except IntegrityError as e:
        raise Exception(f"Database integrity error: {e}")
    except DataError as e:
        raise Exception(f"Database data error: {e}")
    except OperationalError as e:
        raise Exception(f"Database operational error: {e}")
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def get_audiobook_genres(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(AudiobookGenre).offset(skip).limit(limit).all()
    except IntegrityError as e:
        raise Exception(f"Database integrity error: {e}")
    except DataError as e:
        raise Exception(f"Database data error: {e}")
    except OperationalError as e:
        raise Exception(f"Database operational error: {e}")
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")


def delete_audiobook_genre(db: Session, audiobook_genre_id: int):
    try:
        db_audiobook_genre = (
            db.query(AudiobookGenre)
            .filter(AudiobookGenre.audiobook_genre_id == audiobook_genre_id)
            .first()
        )
        if db_audiobook_genre:
            db.delete(db_audiobook_genre)
            db.commit()
            return True
        return False
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Database integrity error: {e}")
    except DataError as e:
        db.rollback()
        raise Exception(f"Database data error: {e}")
    except OperationalError as e:
        db.rollback()
        raise Exception(f"Database operational error: {e}")
    except exc.SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Database error: {e}")

def get_genres_by_audiobook_id(db: Session, audiobook_id:int):
    try:
        return db.query(AudiobookGenre).filter(AudiobookGenre.audiobook_id == audiobook_id).all()
    except IntegrityError as e:
        raise Exception(f"Database integrity error: {e}")
    except DataError as e:
        raise Exception(f"Database data error: {e}")
    except OperationalError as e:
        raise Exception(f"Database operational error: {e}")
    except exc.SQLAlchemyError as e:
        raise Exception(f"Database error: {e}")