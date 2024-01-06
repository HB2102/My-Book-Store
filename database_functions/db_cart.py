from database.models import Cart, CartItem, Payment, Book, User
from schemas.schemas import UserBase
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_
from database.hash import Hash
from fastapi.exceptions import HTTPException
from fastapi import status
import datetime


def add_to_cart(book_id: int, user_id: int, number: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    book = db.query(Book).filter(Book.id == book_id).first()

    if user.current_cart_id == 0:
        cart = Cart(
            user_id=user.id,
            total_price=0,
            payment_id=0,
        )
        db.add(cart)
        db.commit()

        payment = Payment(
            id=cart.id,
            cart_id=cart.id,
            created_at=datetime.datetime.now(),
            is_paid=False
        )

        db.add(payment)
        db.commit()

        cart.payment_id = payment.id
        db.commit()

        user.current_cart_id = cart.id
        db.commit()

    else:
        cart_id = user.current_cart_id
        cart = db.query(Cart).filter(Cart.id == cart_id).first()

    if book.quantity == 0:
        return """Sorry we don't have this book anymore :("""

    if book.quantity < number:
        return """Sorry we don't have this many of this book :("""

    cart_item = db.query(CartItem).filter(and_(CartItem.cart_id == cart.id, CartItem.book_id == book.id)).first()
    if not cart_item:
        cart_item = CartItem(
            cart_id=cart.id,
            book_id=book.id,
            quantity=number,
            total_price_of_item=book.price * number,
        )

        db.add(cart_item)
        db.commit()

    else:
        for i in range(0, number):
            increase_nuber_of_item(book_id, user_id, db)

    book.quantity = book.quantity - number
    db.commit()

    cart.total_price = cart.total_price + cart_item.total_price_of_item
    db.commit()

    return 'Item added to cart'


def increase_nuber_of_item(book_id: int, user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    book = db.query(Book).filter(Book.id == book_id).first()
    cart = db.query(Cart).filter(Cart.id == user.current_cart_id).first()

    if book.quantity == 0:
        return """Sorry we don't have this book anymore :("""

    cart_item = db.query(CartItem).filter(and_(CartItem.cart_id == cart.id, CartItem.book_id == book.id)).first()

    book.quantity = book.quantity - 1
    cart_item.total_price_of_item = cart_item.total_price_of_item + book.price
    cart.total_price = cart.total_price + book.price
    cart_item.quantity = cart_item.quantity + 1
    db.commit()

    return 'Book added to your cart'
