"""
"""

# Project specific imports
from sqlalchemy import Column, Integer, String, Boolean

# Local imports
from .database import BASE

class Todos(BASE):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

