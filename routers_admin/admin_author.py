from fastapi import APIRouter, Depends
from schemas.schemas import UserAuth
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_author
from authentication import auth

router = APIRouter(
    tags=['Admin Author'],
    prefix='/admin/author',
)


@router.post('/add_author/{author_name}')
def add_author(author_name: str, db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_author.add_author(author_name, db, admin.id)


@router.put('/update_author_by_id/{author_id}/{new_name}')
def update_author_by_id(author_id: int, new_name: str, db: Session = Depends(get_db),
                        admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_author.admin_update_author_by_id(author_id, new_name, db, admin.id)


@router.put('/update_author_by_name/{author_name}/{new_name}')
def update_author_by_name(author_name: str, new_name: str, db: Session = Depends(get_db),
                          admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_author.admin_update_author_by_name(author_name, new_name, db, admin.id)


@router.delete('/delete_author_by_id/{author_id}')
def delete_author_by_id(author_id: int, db: Session = Depends(get_db),
                        admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_author.admin_remove_author_by_id(author_id, db, admin.id)


@router.delete('/delete_author_by_name/{author_name}')
def delete_author_by_name(author_name: str, db: Session = Depends(get_db),
                          admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_author.admin_remove_author_by_name(author_name, db, admin.id)
