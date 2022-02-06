from .database import Base
from sqlalchemy import Column, Integer, String


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    author = Column(String, nullable=False)
    pages = Column(Integer)

