from database.models import Book, User, Comment
from schemas.schemas import CommentBase
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status


def add_comment(request: CommentBase, db: Session, user_id: int):
    try:
        book = db.query(Book).filter(Book.id == request.book_id).first()

        comment = Comment(
            user_id=user_id,
            book_id=request.book_id,
            text=request.text,
            rating=request.rating,
        )

        db.add(comment)
        db.commit()

        book.number_of_comments = book.number_of_comments + 1
        db.commit()

        new_rating = get_average_rating_of_book(book.id, db)

        book.average_rating = new_rating
        db.commit()

        return comment

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_average_rating_of_book(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()
    comments = db.query(Comment).filter(Comment.book_id == book_id).all()
    number_of_comments = book.number_of_comments
    if number_of_comments == 0:
        return

    sum_of_rates = 0

    for comment in comments:
        if comment.rating:
            sum_of_rates = sum_of_rates + comment.rating

    rating = sum_of_rates / number_of_comments

    return round(rating, 2)


def user_delete_comment(comment_id: int, db: Session, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    book = db.query(Book).filter(Book.id == comment.book_id).first()

    if comment.user_id == user_id:
        db.delete(comment)
        db.commit()

        book.number_of_comments = book.number_of_comments - 1
        db.commit()

        new_rating = get_average_rating_of_book(book.id, db)
        book.average_rating = new_rating

        db.commit()

        return 'Comment deleted'

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def admin_delete_comment(comment_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        book = db.query(Book).filter(Book.id == comment.book_id).first()

        db.delete(comment)
        db.commit()

        book.number_of_comments = book.number_of_comments - 1
        db.commit()

        new_rating = get_average_rating_of_book(book.id, db)
        book.average_rating = new_rating

        db.commit()

        return 'Comment deleted'

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_all_my_comments(db: Session, user_id: int):
    comments = db.query(Comment).filter(Comment.user_id == user_id).all()

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='You have no comment')

    return comments


def admin_get_all_user_comments(user_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        comments = db.query(Comment).filter(Comment.user_id == user_id).all()

        if not comments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User has no comment')

        return comments

    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_all_comments_of_book(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='NO such a book')

    comments = db.query(Comment).filter(Comment.book_id == book_id).all()

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No comment yet')

    return comments


def admin_get_all_comments_of_book(book_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='NO such a book')

    comments = db.query(Comment).filter(Comment.book_id == book_id).all()

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No comment yet')

    return comments


def admin_delete_all_comments_of_user(user_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No such a user')

    comments = db.query(Comment).filter(Comment.user_id == user_id).all()

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User has no comment')

    for comment in comments:
        admin_delete_comment(comment.id, db, admin_id)

    return 'All the comments of this user has benn deleted'


def admin_delete_all_comments_of_book(book_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No such a book')

    comments = db.query(Comment).filter(Comment.book_id == book_id).all()

    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book has no comment')

    for comment in comments:
        admin_delete_comment(comment.id, db, admin_id)

    return 'All the comments of this book has been deleted.'
