from database.models import Cart, CartItem, Payment, Book, User
from schemas.schemas import UserBase, BookDisplay
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
            increase_number_of_item(book_id, user_id, db)

    book.quantity = book.quantity - number
    db.commit()

    cart.total_price = cart.total_price + cart_item.total_price_of_item
    db.commit()

    return 'Item added to cart'


def increase_number_of_item(book_id: int, user_id: int, db: Session):
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


def decrease_number_of_item(book_id: int, user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    book = db.query(Book).filter(Book.id == book_id).first()
    cart = db.query(Cart).filter(Cart.id == user.current_cart_id).first()
    cart_item = db.query(CartItem).filter(and_(CartItem.cart_id == cart.id, CartItem.book_id == book_id)).first()

    if cart_item.quantity == 1:
        return delete_item(book_id=book_id, db=db, user_id=user_id)

    book.quantity = book.quantity + 1
    cart_item.total_price_of_item = cart_item.total_price_of_item - book.price
    cart.total_price = cart.total_price - book.price
    cart_item.quantity = cart_item.quantity - 1
    db.commit()

    return 'Book removed from your cart'


def is_cart_empty(cart_id: int, db: Session):
    items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    if not items:
        return True
    else:
        return False


def delete_item(book_id: int, db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    cart = db.query(Cart).filter(Cart.id == user.current_cart_id).first()
    cart_item = db.query(CartItem).filter(and_(CartItem.cart_id == cart.id, CartItem.book_id == book_id)).first()
    book = db.query(Book).filter(Book.id == cart_item.book_id).first()

    book.quantity = book.quantity + cart_item.quantity

    db.delete(cart_item)
    db.commit()

    if is_cart_empty(cart_id=cart.id, db=db):
        return delete_cart(db=db, user_id=user.id)

    return 'Item removed from your cart.'


def delete_cart(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user.current_cart_id != 0:
        cart = db.query(Cart).filter(Cart.id == user.current_cart_id).first()
        items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        for item in items:
            book = db.query(Book).filter(Book.id == item.book_id).first()
            book.quantity = book.quantity + item.quantity
            db.delete(item)
            db.commit()

        payment = db.query(Payment).filter(Payment.cart_id == cart.id).first()
        user.current_cart_id = 0

        db.delete(payment)
        db.delete(cart)
        db.commit()

        return 'Cart deleted.'

    else:
        return 'No cart to delete'


def get_current_cart(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if user.current_cart_id == 0:
        return """Your current cart in empty"""

    else:
        cart = db.query(Cart).filter(Cart.id == user.current_cart_id).first()
        payment = db.query(Payment).filter(Payment.id == cart.payment_id).first()
        is_paid = payment.is_paid

        user_display = {
            'username': user.username,
            'email': user.email
        }

        items = db.query(CartItem).join(Book).filter(CartItem.cart_id == cart.id).all()
        items2 = []
        for item in items:
            book = db.query(Book).filter(Book.id == item.book_id).first()
            item_display = {
                'name': book.title,
                'quantity': item.quantity,
                'item_price': item.total_price_of_item,
            }
            items2.append(item_display)

        display = {
            'user': user_display,
            'total_price': cart.total_price,
            'is_paid': is_paid,
            'items': items2,
        }

        return display


def get_all_self_carts(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    carts = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not carts:
        return 'You have no carts'

    user_display = {
        'username': user.username,
        'email': user.email
    }

    carts_display = []

    for cart in carts:
        payment = db.query(Payment).filter(Payment.id == cart.payment_id).first()
        is_paid = payment.is_paid

        items = db.query(CartItem).join(Book).filter(CartItem.cart_id == cart.id).all()
        items2 = []
        for item in items:
            book = db.query(Book).filter(Book.id == item.book_id).first()
            item_display = {
                'name': book.title,
                'quantity': item.quantity,
                'item_price': item.total_price_of_item,
            }
            items2.append(item_display)

        each_cart = {
            'total_price': cart.total_price,
            'is_paid': is_paid,
            'items': items2,
        }

        carts_display.append(each_cart)

    display = {
        'user': user_display,
        'carts': carts_display,
    }

    return display


def admin_get_carts_of_user(user_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = db.query(User).filter(User.id == user_id).first()
    carts = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not carts:
        return 'User has no carts'

    user_display = {
        'username': user.username,
        'email': user.email
    }

    carts_display = []

    for cart in carts:
        payment = db.query(Payment).filter(Payment.id == cart.payment_id).first()
        is_paid = payment.is_paid

        items = db.query(CartItem).join(Book).filter(CartItem.cart_id == cart.id).all()
        items2 = []
        for item in items:
            book = db.query(Book).filter(Book.id == item.book_id).first()
            item_display = {
                'name': book.title,
                'quantity': item.quantity,
                'item_price': item.total_price_of_item,
            }
            items2.append(item_display)

        each_cart = {
            'total_price': cart.total_price,
            'is_paid': is_paid,
            'items': items2,
        }

        carts_display.append(each_cart)

    display = {
        'user': user_display,
        'carts': carts_display,
    }

    return display


def admin_get_carts_of_user_by_username(username: str, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = db.query(User).filter(User.username == username).first()
    carts = db.query(Cart).filter(Cart.user_id == user.id).all()

    if not carts:
        return 'User has no carts'

    user_display = {
        'username': user.username,
        'email': user.email
    }

    carts_display = []

    for cart in carts:
        payment = db.query(Payment).filter(Payment.id == cart.payment_id).first()
        is_paid = payment.is_paid

        items = db.query(CartItem).join(Book).filter(CartItem.cart_id == cart.id).all()
        items2 = []
        for item in items:
            book = db.query(Book).filter(Book.id == item.book_id).first()
            item_display = {
                'name': book.title,
                'quantity': item.quantity,
                'item_price': item.total_price_of_item,
            }
            items2.append(item_display)

        each_cart = {
            'total_price': cart.total_price,
            'is_paid': is_paid,
            'items': items2,
        }

        carts_display.append(each_cart)

    display = {
        'user': user_display,
        'carts': carts_display,
    }

    return display


def get_cart(cart_id: int, db: Session):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    user = db.query(User).filter(User.id == cart.user_id).first()
    payment = db.query(Payment).filter(Payment.id == cart.payment_id).first()
    is_paid = payment.is_paid

    user_display = {
        'username': user.username,
        'email': user.email
    }

    items = db.query(CartItem).join(Book).filter(CartItem.cart_id == cart.id).all()
    items2 = []
    for item in items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        item_display = {
            'name': book.title,
            'quantity': item.quantity,
            'item_price': item.total_price_of_item,
        }
        items2.append(item_display)

    display = {
        'user': user_display,
        'total_price': cart.total_price,
        'is_paid': is_paid,
        'items': items2,
    }

    return display


def admin_get_cart(cart_id: int, db: Session):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    user = db.query(User).filter(User.id == cart.user_id).first()
    payment = db.query(Payment).filter(Payment.id == cart.payment_id).first()
    is_paid = payment.is_paid

    user_display = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    items = db.query(CartItem).join(Book).filter(CartItem.cart_id == cart.id).all()
    items2 = []
    for item in items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        item_display = {
            'id': book.id,
            'name': book.title,
            'quantity': item.quantity,
            'item_price': item.total_price_of_item,
            'publisher': book.publisher,
        }
        items2.append(item_display)

    display = {
        'user': user_display,
        'total_price': cart.total_price,
        'is_paid': is_paid,
        'items': items2,
    }

    return display


def admin_get_cart_by_id(cart_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    display = admin_get_cart(cart_id, db)

    return display


def admin_delete_cart(cart_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cart not found !')

    payment = db.query(Payment).filter(Payment.cart_id == cart.id).first()
    if payment.is_paid == True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not authorized to delete paid carts !')

    user = db.query(User).filter(User.current_cart_id == cart.id)
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    for item in items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        book.quantity = book.quantity + item.quantity
        db.delete(item)
        db.commit()

    user.current_cart_id = 0

    db.delete(payment)
    db.delete(cart)
    db.commit()

    return "Cart deleted."
