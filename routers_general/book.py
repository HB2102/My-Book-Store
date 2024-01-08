from fastapi import APIRouter, Depends
from schemas.schemas import BookDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_book
from typing import List

router = APIRouter(prefix='/book', tags=['Book'])


@router.get('/get_book/{id}', response_model=BookDisplay)
def get_book(id: int, db: Session = Depends(get_db)):
    return db_book.get_book(id, db)


@router.get('/get_all_books', response_model=List[BookDisplay])
def get_all_books(db: Session = Depends(get_db)):
    return db_book.get_all_books(db)


@router.get('/get_books_by_title/{title}', response_model=List[BookDisplay])
def get_book_by_title(title: str, db: Session = Depends(get_db)):
    return db_book.get_book_by_title(title, db)


@router.get('/get_books_by_author/{author}', response_model=List[BookDisplay])
def get_books_by_author(author: str, db: Session = Depends(get_db)):
    return db_book.get_book_by_author(author, db)


@router.get('/get_books_by_publisher/{publisher}', response_model=List[BookDisplay])
def get_books_by_publisher(publisher: str, db: Session = Depends(get_db)):
    return db_book.get_book_by_publisher(publisher, db)


@router.get('/get_books_by_category/{category}', response_model=List[BookDisplay])
def get_books_by_category(category: str, db: Session = Depends(get_db)):
    return db_book.get_book_by_category(category, db)
