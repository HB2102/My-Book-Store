from fastapi import FastAPI
from database.database import Base
from database.database import engine
from database import models
from routers import user, book




app = FastAPI()
app.include_router(user.router)
app.include_router(book.router)


Base.metadata.create_all(engine)



@app.get('/')
def home():
    message = 'Welcome to the book store'
    return message

