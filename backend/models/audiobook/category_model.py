# backend/models/audiobook/category_model.py
from sqlalchemy import Column, Integer, String
from models.base import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
