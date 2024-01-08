from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.database import Base
from database.database import engine
from database import models
from routers_general import user, book, cart, comment, payment, order, bookpicture
from routers_admin import admin_user, admin_book, admin_cart, admin_category, admin_author, admin_commet, admin_order, \
    admin_bookpictures
from authentication import authentication

app = FastAPI()
app.include_router(user.router)
app.include_router(book.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(comment.router)
app.include_router(payment.router)
app.include_router(bookpicture.router)
app.include_router(authentication.router)
app.include_router(admin_user.router)
app.include_router(admin_book.router)
app.include_router(admin_cart.router)
app.include_router(admin_order.router)
app.include_router(admin_author.router)
app.include_router(admin_commet.router)
app.include_router(admin_category.router)
app.include_router(admin_bookpictures.router)

Base.metadata.create_all(engine)

app.mount('/files', StaticFiles(directory='pictures'), name='files')


@app.get('/')
def home():
    message = 'Welcome to the book store'
    return message
