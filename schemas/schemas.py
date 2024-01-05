from pydantic import BaseModel
from datetime import datetime
from typing import List



class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True

