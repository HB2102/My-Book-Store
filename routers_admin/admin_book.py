from fastapi import APIRouter, Depends
from schemas.schemas import AdminUserDisplay, UserBase, UserAuth, AdminBookDisplay, BookBase
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_book
from authentication import auth
from typing import List

router = APIRouter(
    tags=['Admin products'],
    prefix='/admin/products',
)


@router.post('/add_book', response_model=AdminBookDisplay)
def add_book(request: BookBase, db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.add_book(request, db, admin.id)


@router.get('/get_book/{id}', response_model=AdminBookDisplay)
def admin_get_book(id: int, db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_get_book(id, db, admin.id)


@router.get('/get_all_books', response_model=List[AdminBookDisplay])
def admin_get_all_books(db: Session = Depends(get_db), admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_get_all_books(db, admin.id)


@router.get('/get_books_by_title/{title}', response_model=List[AdminBookDisplay])
def admin_get_book_by_title(title: str, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_get_book_by_title(title, db, admin.id)


@router.get('/get_books_by_author/{author}', response_model=List[AdminBookDisplay])
def admin_get_books_by_author(author: str, db: Session = Depends(get_db),
                              admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_get_book_by_author(author, db, admin.id)


@router.get('/get_books_by_publisher/{publisher}', response_model=List[AdminBookDisplay])
def admin_get_books_by_publisher(publisher: str, db: Session = Depends(get_db),
                                 admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_get_book_by_publisher(publisher, db, admin.id)


@router.put('/update_book/{id}', response_model=AdminBookDisplay)
def update_book(id: int, request: BookBase, db: Session = Depends(get_db),
                admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_update_book(id, request, db, admin.id)


@router.put('/update_book_price/{id}/{new_price}', response_model=AdminBookDisplay)
def update_price(id: int, new_price: int, db: Session = Depends(get_db),
                 admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_update_price(id, new_price, db, admin.id)


@router.put('/update_book_price_by_percent/{id}/{percent}', response_model=AdminBookDisplay)
def update_price_by_percent(id: int, percent: int, db: Session = Depends(get_db),
                            admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_update_price_by_percent(id, percent, db, admin.id)


@router.put('/update_all_book_prices/{percent}', response_model=List[AdminBookDisplay])
def update_all_prices(percent: int, db: Session = Depends(get_db),
                      admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_update_all_prices(percent, db, admin.id)


@router.put('/update_book_quantity/{id}/{new_quantity}', response_model=AdminBookDisplay)
def update_book_quantity(id: int, new_quantity: int, db: Session = Depends(get_db),
                         admin: UserAuth = Depends(auth.get_current_user_admin)):
    return db_book.admin_update_quantity(id, new_quantity, db, admin.id)
