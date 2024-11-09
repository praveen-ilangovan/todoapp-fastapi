"""
"""

# Builtin imports
from typing import Optional, TYPE_CHECKING, Union

# Project specific imports
from fastapi import FastAPI, status, HTTPException, Body
from fastapi.encoders import jsonable_encoder


# Local imports
from .model import Book, UpdateBook

if TYPE_CHECKING:
    from uuid import UUID

#-----------------------------------------------------------------------------#
# APP
#-----------------------------------------------------------------------------#

app = FastAPI()

#-----------------------------------------------------------------------------#
# Database
#-----------------------------------------------------------------------------#

BOOKS = [Book(title='The Alchemist', author='Paulo Coelho', description='Great Book', published=1988, rating=4),
         Book(title='My Name is Red', author='Orhan Pamuk', description='One of the best books', published=1998, rating=4),
         Book(title='Jurassic Park', author='Michael Crichton', description='Amazing Book', published=1990, rating=3),
         Book(title='1984', author='George Orwell', description='Best SciFi', published=1949, rating=3),
         Book(title='Animal Farm', author='George Orwell', description='Great Book', published=1945, rating=4),
         Book(title='The Pilgrimage', author='Paulo Coelho', description='Great Book', published=1987, rating=2)]

#-----------------------------------------------------------------------------#
# Utils
#-----------------------------------------------------------------------------#
def encode_input(data) -> dict[str, Optional[Union[str, int]]]:
    data = jsonable_encoder(data)
    data = {k: v for k, v in data.items() if v is not None}
    return data

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
async def get_all_books(rating: Optional[int] = None, published: Optional[int] = None) -> list[Book]:
    if rating:
        return [book for book in BOOKS if book.rating == rating]
    elif published:
        return [book for book in BOOKS if book.published == published]
    else:
        return BOOKS

@app.get("/books/{id}", tags=['Books'])
async def get_book(id: str) -> Optional[Book]:
    for book in BOOKS:
        if str(book.id) == id:
            return book

@app.put("/books/{id}", tags=['Books'], response_model=UpdateBook)
async def update_book(id: str, data_to_update:UpdateBook)-> Book:
    for index, book in enumerate(BOOKS):
        if str(book.id) == id:
            # cleanup dict
            data = encode_input( data_to_update.model_dump() )
            BOOKS[index] = book.model_copy(update=data)
            return BOOKS[index]                

@app.delete("/books/{id}", tags=['Books'])
async def delete_book(id: str):
    for index, book in enumerate(BOOKS):
        if str(book.id) == id:
            del BOOKS[index]
            return
