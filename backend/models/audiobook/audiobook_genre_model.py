# backend/models/audiobook/audiobook_genre_model.py
from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base


class AudiobookGenre(Base):
    __tablename__ = "audiobook_genres"

    audiobook_genre_id = Column(Integer, primary_key=True, index=True)
    audiobook_id = Column(Integer, ForeignKey("audiobooks.audiobook_id"))
    genre_id = Column(Integer, ForeignKey("genres.genre_id"))