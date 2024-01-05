from fastapi import APIRouter, Depends
from schemas.schemas import UserDisplay, UserBase
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_user


router = APIRouter(prefix='/user', tags=['user'])


@router.post('/create', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(request, db)

