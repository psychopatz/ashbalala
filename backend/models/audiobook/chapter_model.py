# backend/models/audiobook/chapter_model.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.audiobook.audiobook_model import Audiobook


class Chapter(Base):
    __tablename__ = "chapters"

    chapter_id = Column(Integer, primary_key=True, index=True)
    audiobook_id = Column(Integer, ForeignKey("audiobooks.audiobook_id"))
    title = Column(String(255), nullable=False)
    duration = Column(Float, nullable=False)
    file_url = Column(String(255), nullable=False)
    sequence_number = Column(Integer, nullable=False)

    audiobook = relationship(Audiobook, backref="chapters")
