"""Describe the database."""
from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


class URL(Base):
    """Define the URL model."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)


class User(Base):
    """Define the User model."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
