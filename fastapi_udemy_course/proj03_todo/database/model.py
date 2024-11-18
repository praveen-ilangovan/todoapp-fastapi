"""
"""

# Project specific imports
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# Local imports
from .database import BASE

class Users(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    active = Column(Boolean, default=False)
    role = Column(String)
    phone_number = Column(String)

class Todos(BASE):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
