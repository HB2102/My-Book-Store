from database.database import Base, sessionlocal
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship


# USER TABLE ============================================================================================
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    is_admin = Column(Boolean)
    current_cart_id = Column(Integer, ForeignKey('cart.id'))
    # cart_user = relationship('Cart', back_populates='user_cart')


# BOOK TABLE ============================================================================================
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    publisher = Column(String)
    price = Column(Integer)
    published = Column(Integer)
    quantity = Column(Integer)
    # book_picture_book = relationship('BookPicture', back_populates='book_book_picture')
    # book_author_book = relationship('BookAuthor', back_populates='book_book_author')
    # cart_item_book = relationship('CartItem', back_populates='book_cart_item')


# BOOK PICTURE TABLE ============================================================================================
class BookPicture(Base):
    __tablename__ = 'book_picture'
    id = Column(Integer, index=True, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    picture = Column(String)
    # book_book_picture = relationship('Book', back_populates='book_picture_book')


# AUTHOR TABLE ============================================================================================
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    # book_author_author = relationship('BookAuthor', back_populates='author_book_author')


# BOOK AUTHOR TABLE ============================================================================================
class BookAuthor(Base):
    __tablename__ = 'book_author'
    id = Column(Integer, index=True, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    author_id = Column(Integer, ForeignKey('author.id'))
    # book_book_author = relationship('Book', back_populates='book_author_book')
    # author_book_author = relationship('Author', back_populates='book_author_author')


# CART TABLE ============================================================================================
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    total_price = Column(Float)
    payment_id = Column(Integer, ForeignKey('payment.id'))
    # user_cart = relationship('User', back_populates='cart_user')
    # payment_cart = relationship('Payment', back_populates='cart_payment')
    # cart_item_cart = relationship('CartItem', back_populates='cart_cart_item')


# CART ITEM TABLE ============================================================================================
class CartItem(Base):
    __tablename__ = 'cart_item'
    id = Column(Integer, index=True, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    quantity = Column(Integer)
    total_price_of_item = Column(Integer)
    # cart_cart_item = relationship('Cart', back_populates='cart_item_cart')
    # book_cart_item = relationship('Book', back_populates='cart_item_book')


# PAYMENT TABLE ============================================================================================
class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    created_at = Column(DateTime)
    is_paid = Column(Boolean)
    # cart_payment = relationship('Cart', back_populates='payment_cart')


# Order TABLE ============================================================================================
class Oreder(Base):
    __tablename__ = 'order'
    id = Column(Integer, index=True, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    payment_id = Column(Integer, ForeignKey('payment.id'))
    address = Column(String)
    postal_code = Column(String)
    phone_number = Column(String(15))
    is_sent = Column(Boolean)


# COMMENT TABLE ============================================================================================
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    text = Column(String)
