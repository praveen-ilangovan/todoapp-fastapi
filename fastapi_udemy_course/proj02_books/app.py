"""
"""

# Builtin imports
from typing import Optional

# Project specific imports
from fastapi import FastAPI, status, HTTPException, Body

# Local imports
from .model import Book

#-----------------------------------------------------------------------------#
# APP
#-----------------------------------------------------------------------------#

app = FastAPI()

#-----------------------------------------------------------------------------#
# Database
#-----------------------------------------------------------------------------#

BOOKS = [Book(id=1, title='The Alchemist', author='Paulo Coelho', description='Great Book', rating=4),
         Book(id=2, title='My Name is Red', author='Orhan Pamuk', description='One of the best books', rating=4),
         Book(id=3, title='Jurassic Park', author='Michael Crichton', description='Amazing Book', rating=3),
         Book(id=4, title='1984', author='George Orwell', description='Best SciFi', rating=3),
         Book(id=5, title='Animal Farm', author='George Orwell', description='Great Book', rating=4),
         Book(id=6, title='The Pilgrimage', author='Paulo Coelho', description='Great Book', rating=2)]

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@app.get("/", tags=['Root'])
async def index() -> dict[str, str]:
    return {"message": "FastAPI udemy tutorial - Books2"}

@app.post("/books", tags=['Books'], response_model=Book)
async def create_book(book: Book) -> Book:
    BOOKS.append(book)
    return BOOKS[-1]

@app.get("/books", tags=['Books'])
async def get_all_books() -> list[Book]:
    return BOOKS
