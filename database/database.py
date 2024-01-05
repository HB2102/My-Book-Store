from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///my_book_store.db', connect_args={'check_same_thread': False})
Base = declarative_base()
sessionlocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()
