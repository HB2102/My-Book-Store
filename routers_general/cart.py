from fastapi import APIRouter, Depends
from schemas.schemas import UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_cart
from authentication import auth

router = APIRouter(prefix='/cart', tags=['Cart'])


@router.get('/add_to_cart/{book_id}/{number}')
def add_to_cart(book_id: int, number: int, db: Session = Depends(get_db),
                user: UserAuth = Depends(auth.get_current_user)):
    return db_cart.add_to_cart(user_id=user.id, book_id=book_id, number=number, db=db)


@router.put('/increase_nuber_of_item/{book_id}')
def increase_nuber_of_item(book_id: int, db: Session = Depends(get_db),
                           user: UserAuth = Depends(auth.get_current_user)):
    return db_cart.increase_number_of_item(book_id=book_id, user_id=user.id, db=db)


@router.put('/decrease_nuber_of_item/{book_id}')
def decrease_nuber_of_item(book_id: int, db: Session = Depends(get_db),
                           user: UserAuth = Depends(auth.get_current_user)):
    return db_cart.decrease_number_of_item(book_id=book_id, user_id=user.id, db=db)


@router.delete('/delete_item/{book_id}')
def delete_item(book_id: int, db: Session = Depends(get_db),
                user: UserAuth = Depends(auth.get_current_user)):
    return db_cart.delete_item(book_id=book_id, db=db, user_id=user.id)


@router.delete('/delete_cart')
def delete_cart(db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_cart.delete_cart(db=db, user_id=user.id)


@router.get('/get_current_cart')
def get_current_cart(user: UserAuth = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return db_cart.get_current_cart(user_id=user.id, db=db)


@router.get('/get_all_self_carts')
def get_all_self_carts(user: UserAuth = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return db_cart.get_all_self_carts(user_id=user.id, db=db)
