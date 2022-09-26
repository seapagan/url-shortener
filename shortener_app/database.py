"""Deal with the Database connection."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

if get_settings().db_backend == "postgresql":
    engine = create_engine(
        get_settings().db_url,
        pool_size=3,
        max_overflow=0,
    )
else:
    engine = create_engine(
        get_settings().db_url,
        connect_args={"check_same_thread": False},
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Create a new DB session with each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
