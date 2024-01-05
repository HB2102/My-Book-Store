from database.models import User
from schemas.schemas import UserBase
from sqlalchemy.orm import Session
from database.hash import Hash
from fastapi.exceptions import HTTPException
from fastapi import status



def create_user(request: UserBase, db: Session):
    user = User(
        username = request.username,
        password = Hash.bcrypt(request.password),
        email = request.email,
        current_cart_id = 0,
        is_admin = False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


