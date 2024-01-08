from fastapi import APIRouter, Depends
from schemas.schemas import UserAuth, SetOrder
from sqlalchemy.orm import Session
from database.database import get_db
from database_functions import db_payment
from authentication import auth

router = APIRouter(prefix='/payment', tags=['Payment'])


@router.post('/pay_for_cart')
def pay_for_cart(request: SetOrder, db: Session = Depends(get_db), user: UserAuth = Depends(auth.get_current_user)):
    return db_payment.pay_for_cart(request, db, user.id)
