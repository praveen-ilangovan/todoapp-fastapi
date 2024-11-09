"""
"""

# Builtin imports
import uuid
from typing import Optional

# Project specific imports
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: uuid.UUID = Field(init=False, default_factory=uuid.uuid4)
    title: str
    author: str
    description: str
    published: int
    rating: int = Field(gt=0, lt=6)

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    published: Optional[int] = None
    rating: Optional[int] = None

