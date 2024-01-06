from fastapi import APIRouter, Depends
from schemas.schemas import AdminUserDisplay, UserBase, UserAuth, AdminBookDisplay, BookBase, CategoryDisplay
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_category
from authentication import auth
from typing import List

router = APIRouter(
    tags=['Admin category'],
    prefix='/admin/category',
)


@router.post('/add_category/{category_name}')
def add_category(category_name: str, db: Session = Depends(get_db),
                 admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_category.admin_add_category(category_name, db, admin.id)


@router.put('/update_category_by_id/{category_id}/{new_name}')
def update_category_by_id(category_id: int, new_name: str, db: Session = Depends(get_db),
                          admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_category.admin_update_category_by_id(category_id, new_name, db, admin.id)


@router.put('/update_category_by_name/{category_name}/{new_name}')
def update_category_by_name(category_name: str, new_name: str, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_category.admin_update_category_by_name(category_name, new_name, db, admin.id)


@router.delete('/delete_category_by_id/{category_id}')
def delete_category_by_id(category_id: int, db: Session = Depends(get_db),
                          admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_category.admin_remove_category_by_id(category_id, db, admin.id)


@router.delete('/delete_category_by_name/{category_name}')
def delete_category_by_name(category_name: str, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_category.admin_remove_category_by_name(category_name, db, admin.id)
