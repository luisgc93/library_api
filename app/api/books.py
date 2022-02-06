import logging.config

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.crud import crud_books
from app.core.database import get_db
from app.core import schemas


logging.config.fileConfig("config/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


router = APIRouter(tags=["books"])


@router.post("/books/")
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if crud_books.get_book_by_title(title=book.title, db=db) is not None:
        raise HTTPException(status_code=422, detail=f"A book with title {book.title} already exists.")
    return crud_books.create_book(db=db, book=book)


@router.get("/books/")
async def read_books(db: Session = Depends(get_db)):
    return crud_books.get_all_books(db=db)
