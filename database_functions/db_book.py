from database.models import Book, Author, BookAuthor, BookPicture, User, Category
from schemas.schemas import BookDisplay, BookBase
from sqlalchemy import Select
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status


def get_book(id: int, db: Session):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found !')

    return book


def get_all_books(db: Session):
    books = db.query(Book).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found !')

    return books


def get_book_by_title(title: str, db: Session):
    books = db.query(Book).filter(Book.title == title).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books


def get_book_by_author(author: str, db: Session):
    books = db.query(Book).join(BookAuthor).join(Author).filter(Author.name == author).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books


def get_book_by_publisher(publisher: str, db: Session):
    books = db.query(Book).filter(Book.publisher == publisher).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books


def get_book_by_category(category_name: str, db: Session):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No such a category was found !')

    books = db.query(Book).filter(Book.category_id == category.id).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found in this category!')

    return books


# =======================================================================================================
# =======================================================================================================
# =======================================================================================================
# =======================================================================================================
# =======================================================================================================


def add_book(request: BookBase, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        if not request.quantity:
            request.quantity = 0

        book = Book(
            title=request.title,
            publisher=request.publisher,
            price=request.price,
            published=request.published,
            quantity=request.quantity,
            category_id=request.category_id,
            number_of_comments=0,
        )
        db.add(book)
        db.commit()
        db.refresh(book)

        # book_pictures = request.pictures
        # for pic in book_pictures:
        #     axe = BookPicture(
        #         book_id = book.id,
        #         picture = pic
        #     )
        #
        #     db.add(axe)
        #     db.commit()
        #     db.refresh(axe)

        return book

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_get_book(id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found !')

    return book


def admin_get_all_books(db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    books = db.query(Book).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found !')

    return books


def admin_get_book_by_title(title: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    books = db.query(Book).filter(Book.title == title).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books


def admin_get_book_by_author(author: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    books = db.query(Book).join(BookAuthor).join(Author).filter(Author.name == author).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books


def admin_get_book_by_publisher(publisher: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    books = db.query(Book).filter(Book.publisher == publisher).all()

    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No book was found !')

    return books


def admin_update_book(id: int, request: BookBase, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        book = db.query(Book).filter(Book.id == id).first()

        book.title = request.title
        book.price = request.price
        book.published = request.published
        book.publisher = request.publisher
        book.price = request.price

        db.commit()
        db.refresh(book)

        return book

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_update_price(id: int, new_price: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        book = db.query(Book).filter(Book.id == id).first()
        book.price = new_price

        db.commit()

        return book

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_update_price_by_percent(id: int, percent: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        book = db.query(Book).filter(Book.id == id).first()
        book.price = book.price * (percent + 100) // 100

        db.commit()

        return book

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_update_all_prices(percent: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        books = db.query(Book).all()

        for book in books:
            book.price = book.price * (percent + 100) // 100
            db.commit()

        return books

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_update_quantity(id: int, new_quantity: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        book = db.query(Book).filter(Book.id == id).first()
        book.quantity = new_quantity

        db.commit()

        return book

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def admin_delete_book(id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        book = db.query(Book).filter(Book.id == id).first()
        if not book:
            return "No such a book"

        db.delete(book)
        db.commit()

        return 'Book deleted'

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
