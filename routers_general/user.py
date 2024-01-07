from fastapi import APIRouter, Depends
from schemas.schemas import UserDisplay, UserBase, UserAuth, UpdateUserBase
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_user
from authentication import auth

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/create', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(request, db)


@router.put('/update_info', response_model=UpdateUserBase)
def create_user(request: UpdateUserBase, db: Session = Depends(get_db),
                user: UserAuth = Depends(auth.get_current_user)):
    return db_user.user_update_info(request, db, user.id)


@router.delete('/delete_self_account/{id}')
def delete_user(current_user: UserAuth = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return db_user.delete_user_self(user_id=current_user.id, db=db)
