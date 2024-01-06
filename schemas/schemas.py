from pydantic import BaseModel
from fastapi import Query
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str = Query(regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class AdminUserDisplay(BaseModel):
    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    email: str

    class Config:
        from_attributes = True


class UserAuth(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class BookDisplay(BaseModel):
    title: str
    publisher: Optional[str]
    price: Optional[int]
    published: Optional[int]

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    publisher: Optional[str]
    price: int
    published: Optional[int]
    quantity: Optional[int]
    category_id: Optional[int]

    # pictures: Optional[List[]]


class AdminBookDisplay(BaseModel):
    id: int
    title: str
    publisher: Optional[str]
    price: Optional[int]
    published: Optional[int]
    quantity: Optional[int]

    class Config:
        from_attributes = True


class CartItemDisplay(BaseModel):
    title: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class CartDisplay(BaseModel):
    user_id: UserDisplay
    total_price: float

    # is_paid: bool

    class Config:
        from_attributes = True


class CategoryDisplay(BookDisplay):
    name: str

    class Config:
        from_attributes = True
