from database.models import Cart, CartItem, Payment, Book, User, Oreder
from schemas.schemas import UserBase, BookDisplay
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_
from database.hash import Hash
from fastapi.exceptions import HTTPException
from fastapi import status
from database_functions.db_cart import get_cart, admin_get_cart
import datetime


def get_order(order_id, db: Session):
    order = db.query(Oreder).filter(Oreder.id == order_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found!')

    cart = db.query(Cart).filter(Cart.id == order.cart_id).first()
    cart_display = get_cart(cart.id, db)

    display = {
        'cart': cart_display,
        'is_sent': order.is_sent,
    }

    return display


def admin_get_order(order_id, db: Session):
    order = db.query(Oreder).filter(Oreder.id == order_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found!')

    cart = db.query(Cart).filter(Cart.id == order.cart_id).first()

    cart_display = get_cart(cart.id, db)

    display = {
        'cart': cart_display,
        'paid at': order.paid_at,
        'phone_number': order.phone_number,
        'price': order.price,
        'address': order.address,
        'postal_code': order.postal_code,
        'is_sent': order.is_sent,
    }

    return display


def user_get_all_orders(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    orders = db.query(Oreder).filter(Oreder.user_id == user.id).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    display = []

    for order in orders:
        this_order = get_order(order.id, db)
        display.append(this_order)

    return display


def user_get_one_order(order_id: int, db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    order = db.query(Oreder).filter(Oreder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    if order.user_id == user.id:
        return get_order(order.id, db)

    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def user_get_sent_orders(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    orders = db.query(Oreder).filter(Oreder.user_id == user.id).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    display = []

    for order in orders:
        if order.is_sent == True:
            this_order = get_order(order.id, db)
            display.append(this_order)

    if not display:
        return 'No order found here'

    return display


def user_get_not_sent_orders(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    orders = db.query(Oreder).filter(Oreder.user_id == user.id).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    display = []

    for order in orders:
        if order.is_sent == False:
            this_order = get_order(order.id, db)
            display.append(this_order)

    if not display:
        return 'No order found here'

    return display


def admin_get_all_orders(db: Session, admin_id):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    orders = db.query(Oreder).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    display = []

    for order in orders:
        this_order = admin_get_order(order.id, db)
        display.append(this_order)

    if not display:
        return 'No order found here'

    return display


def admin_get_one_order(order_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    order = db.query(Oreder).filter(Oreder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    return admin_get_order(order.id, db)


def admin_get_all_sent_orders(db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    orders = db.query(Oreder).filter(Oreder.is_sent == True).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    display = []

    for order in orders:
        this_order = admin_get_order(order.id, db)
        display.append(this_order)

    if not display:
        return 'No order found here'

    return display


def admin_get_all_not_sent_orders(db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    orders = db.query(Oreder).filter(Oreder.is_sent == False).all()

    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NO order was found!')

    display = []

    for order in orders:
        this_order = admin_get_order(order.id, db)
        display.append(this_order)

    if not display:
        return 'No order found here'

    return display


def admin_send_order(order_id: int, db: Session, admin_id: int):
    admin = db.query(User).filter(User.id == admin_id).first()
    if admin.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    order = db.query(Oreder).filter(Oreder.id == order_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found!')

    if order.is_sent == True:
        return "Order already sent"

    order.is_sent = True

    db.commit()

    return "Order on the way..."
