from database.models import User
from schemas.schemas import UserBase, UpdateUserBase
from sqlalchemy.orm import Session
from database.hash import Hash
from fastapi.exceptions import HTTPException
from fastapi import status


def create_user(request: UserBase, db: Session):
    check_username = request.username
    checked_username = check_username_duplicate(check_username, db)
    if checked_username:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='This username already exists')

    user = User(
        username=request.username,
        password=Hash.bcrypt(request.password),
        email=request.email,
        current_cart_id=0,
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def user_update_info(request: UpdateUserBase, db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    check_username = request.username
    checked_username = check_username_duplicate(check_username, db)
    if checked_username == True and user.username != request.username:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='This username already exists')

    user.username = request.username
    user.password = Hash.bcrypt(request.password)
    user.first_name = request.first_name
    user.last_name = request.last_name
    user.phone_number = request.phone_number
    user.email = request.email

    db.commit()

    return user


def get_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found !')

    return user


def check_username_duplicate(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return True
    else:
        return False


def admin_get_user_by_id(user_id: int, db: Session, admin_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found !')

    return user


def admin_get_user_by_username(username: str, db: Session, admin_id: int):
    user = db.query(User).filter(User.username == username).first()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found !')

    return user


def delete_user_self(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    try:
        db.delete(user)
        db.commit()
        return 'User Deleted'
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_delete_user(user_id: int, db: Session, admin_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        db.delete(user)
        db.commit()
        return 'User Deleted'
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_delete_user_by_username(username: str, db: Session, admin_id: int):
    user = db.query(User).filter(User.username == username).first()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        db.delete(user)
        db.commit()
        return 'User Deleted'
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def promotr_to_admin(user_id: int, db: Session, admin_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        user.is_admin = True
        db.commit()
        return 'User promoted to admin'

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def promotr_to_admin_by_username(username: str, db: Session, admin_id: int):
    user = db.query(User).filter(User.username == username).first()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        user.is_admin = True
        db.commit()
        return 'User promoted to admin'
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_get_all_users(db: Session, admin_id: int):
    users = db.query(User).all()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Users not found !')

    return users


def admin_get_all_admins(db: Session, admin_id: int):
    users = db.query(User).filter(User.is_admin == True).all()
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Users not found !')

    return users
