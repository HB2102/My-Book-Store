from fastapi import FastAPI
from database.database import Base
from database.database import engine
from database import models
from routers_general import user, book
from routers_admin import admin_user
from authentication import authentication




app = FastAPI()
app.include_router(user.router)
app.include_router(book.router)
app.include_router(authentication.router)
app.include_router(admin_user.router)


Base.metadata.create_all(engine)



@app.get('/')
def home():
    message = 'Welcome to the book store'
    return message

