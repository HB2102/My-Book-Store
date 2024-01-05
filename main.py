from fastapi import FastAPI
from database.database import Base
from database.database import engine
from database import models




app = FastAPI()



Base.metadata.create_all(engine)



@app.get('/')
def home():
    message = 'Welcome to the book store'
    return message

