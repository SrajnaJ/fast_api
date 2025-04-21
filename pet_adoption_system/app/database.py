from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import config
# import config.py

Base=declarative_base()

def get_engine(is_test=False):
    url = config.TEST_DATABASE_URL if is_test else config.DATABASE_URL
    return create_engine(url)

# default
engine = get_engine()

# default
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session_local(is_test=False):
    engine = get_engine(is_test=is_test)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = declarative_base()

def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()