from fastapi import APIRouter, Depends
from schemas.schemas import UserDisplay, UserBase, UserAuth, CartDisplay, CartItemDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_order
from authentication import auth

router = APIRouter(prefix='/order', tags=['order'])


@router.get('/get_all_self_orders')
def user_get_all_self_orders(db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_order.user_get_all_orders(db, user.id)


@router.get('/get_one_self_orders/{order_id}')
def user_get_one_order(order_id: int, db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_order.user_get_one_order(order_id, db, user.id)


@router.get('/get_all_sent_orders')
def user_get_all_self_orders(db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_order.user_get_sent_orders(db, user.id)


@router.get('/get_all_not_sent_orders')
def user_get_all_self_orders(db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_order.user_get_not_sent_orders(db, user.id)
