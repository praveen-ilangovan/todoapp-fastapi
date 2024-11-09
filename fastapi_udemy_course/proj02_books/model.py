"""
"""

# Project specific imports
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: int = Field(gt=0)
    title: str
    author: str
    description: str
    rating: int = Field(gt=0, lt=6)
