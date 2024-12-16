# /backend/models/audiobook/tag_model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.audiobook.audiobook_model import Audiobook


class AudiobookTag(Base):
    __tablename__ = "audiobook_tags"

    tag_id = Column(Integer, primary_key=True, index=True)
    audiobook_id = Column(Integer, ForeignKey("audiobooks.audiobook_id"))
    tag_name = Column(String(255), nullable=False)

    audiobook = relationship(Audiobook, backref="audiobook_tags")
