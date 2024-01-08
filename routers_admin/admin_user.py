from fastapi import APIRouter, Depends
from schemas.schemas import AdminUserDisplay, UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_user
from authentication import auth
from typing import List

router = APIRouter(
    tags=['Admin Accounts'],
    prefix='/admin/accounts',
)


@router.get('/get_user/{id}', response_model=AdminUserDisplay)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.admin_get_user_by_id(user_id=user_id, db=db, admin_id=admin.id)


@router.get('/get_all_users', response_model=List[AdminUserDisplay])
def get_all_users(db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.admin_get_all_users(db=db, admin_id=admin.id)


@router.get('/get_all_admins', response_model=List[AdminUserDisplay])
def get_all_admins(db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.admin_get_all_admins(db=db, admin_id=admin.id)


@router.get('/get_user_by_username/{username}', response_model=AdminUserDisplay)
def get_user_by_username(username: str, db: Session = Depends(get_db),
                         admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.admin_get_user_by_username(username=username, db=db, admin_id=admin.id)


@router.delete('/delete_user/{id}')
def delete_user(id: int, db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.admin_delete_user(user_id=id, db=db, admin_id=admin.id)


@router.delete('/delete_user_by_username/{username}')
def delete_user(username: str, db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.admin_delete_user_by_username(username=username, db=db, admin_id=admin.id)


@router.put('/promote_user/{id}')
def promote_user_to_admin(id: int, db: Session = Depends(get_db),
                          admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.promotr_to_admin(user_id=id, db=db, admin_id=admin.id)


@router.put('/promote_user_by_username/{username}')
def promote_user_to_admin_by_username(username: str, db: Session = Depends(get_db),
                                      admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_user.promotr_to_admin_by_username(username=username, db=db, admin_id=admin.id)
