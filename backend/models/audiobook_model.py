from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Audiobook(Base):
    __tablename__ = "audiobooks"

    audiobook_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    narrator = Column(String(255), nullable=False)
    duration = Column(Float, nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(String(255), nullable=False)
    genre_id = Column(Integer, nullable=False)
    file_url = Column(String(255), nullable=False)
    cover_image_url = Column(String(255), nullable=False)
