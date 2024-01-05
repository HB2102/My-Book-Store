from database.models import Book, Author, BookAuthor
from schemas.schemas import BookDisplay
from sqlalchemy import Select
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status


def get_book(id: int, db: Session):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found !')

    return book


def get_book_by_title(title: str, db: Session):
    books = db.query(Book).filter(Book.title == title).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books


def get_book_by_author(author: str, db: Session):
    books = db.query(Book).join(BookAuthor).join(Author).filter(Author.name == author).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books

def get_book_by_publisher(publisher: str, db: Session):
    books = db.query(Book).filter(Book.publisher == publisher).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books




