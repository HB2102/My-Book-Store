from database.models import User, Payment, Oreder, Cart
from schemas.schemas import UserBase, UpdateUserBase, SetOrder
from sqlalchemy.orm import Session
from database.hash import Hash
from database_functions.db_cart import get_current_cart
from fastapi.exceptions import HTTPException
from fastapi import status
import datetime


def pay_for_cart(request: SetOrder, db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user.current_cart_id == 0:
        return "No cart available for payment"

    cart = db.query(Cart).filter(Cart.id == user.current_cart_id).first()
    payment = db.query(Payment).filter(Payment.id == cart.payment_id).first()

    order = Oreder(
        user_id=user.id,
        cart_id=cart.id,
        payment_id=payment.id,
        address=request.address,
        postal_code=request.postal_code,
        price=cart.total_price,
        phone_number=request.phone_number,
        paid_at=datetime.datetime.now(),
        is_sent=False,
    )

    db.add(order)
    db.commit()

    payment.is_paid = True
    db.commit()

    display_of_cart = get_current_cart(user.id, db)

    user.current_cart_id = 0
    db.commit()

    # return "your order has been set. It will be sent to you soon"
    return display_of_cart
