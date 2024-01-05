from database.database import Base, sessionlocal
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship


# USER TABLE ============================================================================================
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String(20))
    email = Column(String)
    current_cart_id = Column(Integer, ForeignKey('cart.id'))
    is_admin = Column(Boolean)


# BOOK TABLE ============================================================================================
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    publisher = Column(String)
    price = Column(Float)
    published = Column(Integer)
    quantity = Column(Integer)


# BOOK PICTURE TABLE ============================================================================================
class BookPicture(Base):
    __tablename__ = 'book_picture'
    id = Column(Integer, index=True, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    picture = Column(String)


# AUTHOR TABLE ============================================================================================
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)



# BOOK AUTHOR TABLE ============================================================================================
class BookAuthor(Base):
    __tablename__ = 'book_author'
    id = Column(Integer, index=True, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    author_id = Column(Integer, ForeignKey('author.id'))


# CART TABLE ============================================================================================
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, index=True, primary_key=True)
    number_of_items = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    total_price = Column(Float)
    payment_id = Column(Integer, ForeignKey('payment.id'))


# CART ITEM TABLE ============================================================================================
class CartItem(Base):
    __tablename__ = 'cart_item'
    id = Column(Integer, index=True, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    quantity = Column(Integer)

# PAYMENT TABLE ============================================================================================
class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    created_at = Column(DateTime)
    is_paid = Column(Boolean)


