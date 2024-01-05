from pydantic import BaseModel
from datetime import datetime
from typing import List , Optional



class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
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
