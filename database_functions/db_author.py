from database.models import Book, Author, BookAuthor, BookPicture, User, Category
from schemas.schemas import BookDisplay, BookBase
from sqlalchemy import Select
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status


def add_author(author_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        author = Author(
            name=author_name,
        )

        db.add(author)
        db.commit()
        db.refresh(author)

        return f'Author {author_name} Added'

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_remove_author_by_id(author_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    author = db.query(Author).filter(Author.id == author_id).first()
    name = author.name

    db.delete(author)
    db.commit()

    return f'Author {name} deleted.'


def admin_remove_author_by_name(author_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    author = db.query(Author).filter(Author.name == author_name).first()
    name = author.name

    db.delete(author)
    db.commit()

    return f'Author {name} deleted.'


def admin_update_author_by_id(author_id: int, new_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    category = db.query(Author).filter(Author.id == author_id).first()
    old_name = category.name
    category.name = new_name

    db.commit()

    return f'Category {old_name} changed to {new_name}'


def admin_update_author_by_name(author_name: str, new_name: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    category = db.query(Author).filter(Author.name == author_name).first()
    old_name = category.name
    category.name = new_name

    db.commit()

    return f'Category {old_name} changed to {new_name}'
