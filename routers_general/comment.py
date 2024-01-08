from fastapi import APIRouter, Depends
from schemas.schemas import CommentBase, CommentDisplay, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_comment
from typing import List
from authentication import auth

router = APIRouter(prefix='/comment', tags=['Comment'])


@router.post('/add_comment', response_model=CommentDisplay)
def add_comment(request: CommentBase, db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_comment.add_comment(request, db, user.id)


@router.get('/get_my_comments', response_model=List[CommentDisplay])
def get_all_my_comments(db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_comment.get_all_my_comments(db, user.id)


@router.get('/get_comments_of_book/{book_id}', response_model=List[CommentDisplay])
def get_all_comments_of_book(book_id, db: Session = Depends(get_db)):
    return db_comment.get_all_comments_of_book(book_id, db)


@router.delete('/delete_comment/{comment_id}')
def user_delete_comment(comment_id: int, db: Session = Depends(get_db),
                        user: UserAuth = Depends(auth.get_current_user)):
    return db_comment.user_delete_comment(comment_id, db, user.id)
