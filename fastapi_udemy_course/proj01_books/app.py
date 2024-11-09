"""
"""

# Builtin imports
from typing import Optional

# Project specific imports
from fastapi import FastAPI, status, HTTPException, Body

#-----------------------------------------------------------------------------#
# APP
#-----------------------------------------------------------------------------#

app = FastAPI()

#-----------------------------------------------------------------------------#
# Database
#-----------------------------------------------------------------------------#

BOOKS = [{'title': 'Book One', 'author': 'Author #1', 'category': 'maths'},
         {'title': 'Book Two', 'author': 'Author #2', 'category': 'physics'},
         {'title': 'Book Three', 'author': 'Author #3', 'category': 'chemistry'},
         {'title': 'Book Four', 'author': 'Author #4', 'category': 'biology'},
         {'title': 'Book Five', 'author': 'Author #2', 'category': 'chemistry'},
         {'title': 'Book Six', 'author': 'Author #5', 'category': 'physics'}]

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@app.get("/", tags=['Root'])
async def index() -> dict[str, str]:
    return {"message": "FastAPI udemy tutorial - Books"}

@app.post("/books", tags=['Books'])
async def create_book(book=Body()):
    BOOKS.append(book)


@app.get("/books", tags=['Books'])
async def get_all_books(category: Optional[str] = None) -> list[dict[str, str]]:
    if not category:
        return BOOKS
    
    books = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            books.append(book)
    if books:
        return books

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No books foud under category: {category}"
    )

#-----------------------------------------------------------------------------#
# Routes: Title
#-----------------------------------------------------------------------------#

@app.get("/books/{title}", tags=['Books'])
async def get_book(title: str) -> dict[str, str]:
    for book in BOOKS:
        if book['title'].casefold() == title.casefold():
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with title '{title}' not found."
    )

@app.put("/books/{title}", tags=['Books'])
async def update_book(title: str, new_data=Body()) -> Optional[dict[str, str]]:
    for book in BOOKS:
        if book['title'].casefold() == title.casefold():
            book.update(new_data)
            return book
        
@app.delete("/books/{title}", tags=['Books'])
async def delete_book(title: str):
    index_to_delete = -1
    for index, book in enumerate(BOOKS):
        if book['title'].casefold() == title.casefold():
            index_to_delete = index

    if index_to_delete > -1:
        del BOOKS[index_to_delete]
        return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No books found."
    )




#-----------------------------------------------------------------------------#
# Routes: Author
#-----------------------------------------------------------------------------#

@app.get("/{author}", tags=['Authors'])
async def get_books_by_author(author: str, category: Optional[str] = None) -> list[dict[str, str]]:
    books = []

    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            if not category or (category and book['category'].casefold() == category.casefold()):
                books.append(book)

    if books:
        return books
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No books found."
    )
