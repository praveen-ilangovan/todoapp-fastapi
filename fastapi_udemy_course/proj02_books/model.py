"""
"""

# Project specific imports
from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
