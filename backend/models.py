from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base

class Joke(Base):

    __tablename__ = "jokes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    joke = Column(String)

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True
    )

    password = Column(String)