from fastapi import APIRouter, Depends
from schemas.schemas import UserDisplay, UserBase, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_cart
from authentication import auth

router = APIRouter(prefix='/cart', tags=['cart'])


@router.get('/add_to_cart/{book_id}/{number}')
def add_to_cart(book_id: int, number: int, db: Session = Depends(get_db),
                user: UserAuth = Depends(auth.get_current_user)):
    return db_cart.add_to_cart(user_id=user.id, book_id=book_id, number=number, db=db)


@router.put('/increase_nuber_of_item/{book_id}')
def increase_nuber_of_item(book_id: int, db: Session = Depends(get_db),
                           user: UserAuth = Depends(auth.get_current_user)):
    return db_cart.increase_nuber_of_item(book_id=book_id, user_id=user.id, db=db)
