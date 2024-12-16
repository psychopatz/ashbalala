# backend/models/audiobook/genre_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
