from fastapi import APIRouter, Depends
from schemas.schemas import UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_cart
from authentication import auth

router = APIRouter(
    tags=['Admin Carts'],
    prefix='/admin/carts',
)


@router.get('/get_carts_of_user/{user_id}')
def admin_get_carts_of_user(user_id: int, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_cart.admin_get_carts_of_user(user_id=user_id, db=db, admin_id=admin.id)


@router.get('/get_carts_of_user_by_username/{username}')
def admin_get_carts_of_user_by_username(username: str, db: Session = Depends(get_db),
                                        admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_cart.admin_get_carts_of_user_by_username(username=username, db=db, admin_id=admin.id)


@router.get('/get_cart_by_id/{cart_id}')
def admin_get_cart_by_id(cart_id: int, db: Session = Depends(get_db),
                         admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_cart.admin_get_cart_by_id(cart_id=cart_id, db=db, admin_id=admin.id)


@router.delete('/delete_cart_by_id')
def admin_delete_cart_by_id(cart_id: int, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_cart.admin_delete_cart(cart_id, db, admin.id)
