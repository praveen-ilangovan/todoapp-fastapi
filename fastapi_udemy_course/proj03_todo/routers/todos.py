"""

"""

# Builtin imports
from typing import Optional

# Project specific imports
from fastapi import APIRouter, status, Query, HTTPException, Path
from pydantic import BaseModel, Field

# Local imports
from ..db_init import DB_DEPENDENCY
from ..database.model import Todos

router = APIRouter()

#-----------------------------------------------------------------------------#
# Request Models
#-----------------------------------------------------------------------------#
class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todoitem(db: DB_DEPENDENCY, item: TodoRequest):
    new_item = Todos(**item.model_dump())
    db.add(new_item)
    db.commit()

@router.get("/")
async def get_todos(db: DB_DEPENDENCY, complete: Optional[bool] = None,
                    priority: Optional[int] = Query(gt=0, lt=6, default=None)):
    if complete is not None:
        res = db.query(Todos).filter(Todos.complete == complete).all()
        if res:
            return res
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')

    if priority is not None:
        res = db.query(Todos).filter(Todos.priority == priority).all()
        if res:
            return res
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')

    return db.query(Todos).all()

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_todo_item(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    item = db.query(Todos).filter(Todos.id == id).first()
    if item:
        return item
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todoitem(db: DB_DEPENDENCY,
                          item: TodoRequest,
                          id: int = Path(gt=0)):
    todoitem = db.query(Todos).filter(Todos.id == id).first()
    if not todoitem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')
    
    todoitem.title = item.title
    todoitem.description = item.description
    todoitem.priority = item.priority
    todoitem.complete = item.complete

    db.add(todoitem)
    db.commit()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todoitem(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    todoitem = db.query(Todos).filter(Todos.id == id).first()
    if not todoitem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')
    
    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()

