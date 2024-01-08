from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from main import app

client = TestClient(app)


def test_get_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to the book store"


def test_create_user():
    response = client.post("/user/create", json={"username": "user1",
                                                 "email": "user1@gmai.com",
                                                 "password": "user1"
                                                 })
    assert response.status_code == 200 or response.status_code == 406
    assert response.json() == {"detail": "This username already exists"} or response.json() == {"username": "user1",
                                                                                                "email": "user1@gmai.com"}


def test_update_info():
    response = client.put('user/update_info', json={"username": "string",
                                                    "password": "string",
                                                    "first_name": "string",
                                                    "last_name": "string",
                                                    "email": "string",
                                                    "phone_number": "string"
                                                    })
    assert response.status_code == 401


def test_delete_account():
    response = client.delete('user/delete_self_account/3')
    assert response.status_code == 401
