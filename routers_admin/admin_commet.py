from fastapi import APIRouter, Depends
from schemas.schemas import UserAuth, AminCommentDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_comment
from authentication import auth
from typing import List

router = APIRouter(
    tags=['Admin Comments'],
    prefix='/admin/comments',
)


@router.get('/get_user_all_comments/{user_id}', response_model=List[AminCommentDisplay])
def admin_get_all_user_comments(user_id: int, db: Session = Depends(get_db),
                                admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_comment.admin_get_all_user_comments(user_id, db, admin.id)


@router.get('/get_comments_of_book/{book_id}', response_model=List[AminCommentDisplay])
def get_all_comments_of_book(book_id: int, db: Session = Depends(get_db),
                             admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_comment.admin_get_all_comments_of_book(book_id, db, admin.id)


@router.delete('/delete_comment/{comment_id}')
def admin_delete_comment(comment_id: int, db: Session = Depends(get_db),
                         admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_comment.admin_delete_comment(comment_id, db, admin.id)


@router.delete('/delete_comments_of_book/{book_id}')
def delete_comments_of_book(book_id: int, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_comment.admin_delete_all_comments_of_book(book_id, db, admin.id)


@router.delete('/delete_comments_of_user/{user_id}')
def delete_comments_of_user(user_id: int, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_comment.admin_delete_all_comments_of_user(user_id, db, admin.id)
