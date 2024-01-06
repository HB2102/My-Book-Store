from database.models import Book, Author, BookAuthor, BookPicture, User, Category
from schemas.schemas import BookDisplay, BookBase
from sqlalchemy import Select
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status


def admin_add_category(category_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    category = Category(
        name=category_name
    )

    db.add(category)
    db.commit()

    return f'Category {category.name} added.'


def admin_remove_category_by_id(category_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    category = db.query(Category).filter(Category.id == category_id).first()
    name = category.name

    db.delete(category)
    db.commit()

    return f'Category {name} deleted.'


def admin_remove_category_by_name(category_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    category = db.query(Category).filter(Category.name == category_name).first()
    name = category.name

    db.delete(category)
    db.commit()

    return f'Category {name} deleted.'


def admin_update_category_by_id(category_id: int, new_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    category = db.query(Category).filter(Category.id == category_id).first()
    old_name = category.name
    category.name = new_name

    db.commit()

    return f'Category {old_name} changed to {new_name}'


def admin_update_category_by_name(category_name: str, new_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    category = db.query(Category).filter(Category.name == category_name).first()
    old_name = category.name
    category.name = new_name

    db.commit()

    return f'Category {old_name} changed to {new_name}'
