from fastapi import APIRouter, Depends
from schemas.schemas import UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_order
from authentication import auth

router = APIRouter(
    tags=['Admin Order'],
    prefix='/admin/order',
)


@router.get('/get_all_orders')
def admin_get_all_orders(db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_order.admin_get_all_orders(db, admin.id)


@router.get('/admin_get_one_order/{order_id}')
def admin_get_one_order(order_id: int, db: Session = Depends(get_db),
                        admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_order.admin_get_one_order(order_id, db, admin.id)


@router.get('/get_all_sent_orders')
def admin_get_all_sent_orders(db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_order.admin_get_all_sent_orders(db, admin.id)


@router.get('/get_all_not_sent_orders')
def admin_get_all_not_sent_orders(db: Session = Depends(get_db),
                                  admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_order.admin_get_all_not_sent_orders(db, admin.id)


@router.put('/send_order/{order_id}')
def send_order(order_id: int, db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_order.admin_send_order(order_id, db, admin.id)
