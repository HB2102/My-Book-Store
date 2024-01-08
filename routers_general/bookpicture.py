from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from schemas.schemas import BookDisplay, CommentBase, CommentDisplay, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_comment
from database.models import BookPicture, User, Book
from typing import List
from authentication import auth

router = APIRouter(prefix='/picture', tags=['picture'])


@router.get('/get_pictures_of_book/{book_id}', response_class=FileResponse)
def get_pictures_of_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found !")

    picture = db.query(BookPicture).filter(BookPicture.book_id == book_id).first()
    if not picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No picture found !")

    pic = picture.picture

    return pic
