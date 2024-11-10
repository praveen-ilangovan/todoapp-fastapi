"""

"""

# Builtin imports
from typing import Annotated, Optional

# Project specific imports
from fastapi import FastAPI, Depends, status, HTTPException, Path, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

# Local imports
from .database import ENGINE, SESSIONLOCAL
from . import model

#-----------------------------------------------------------------------------#
# Database
#-----------------------------------------------------------------------------#
model.BASE.metadata.create_all(bind=ENGINE)

def get_db():
    db = SESSIONLOCAL()
    try:
        yield db
    finally:
        db.close()

# DB dependency type
DB_DEPENDENCY = Annotated[Session, Depends(get_db)]

#-----------------------------------------------------------------------------#
# App
#-----------------------------------------------------------------------------#
app = FastAPI()

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
@app.get("/", tags=['Root'])
async def index() -> dict[str, str]:
    return {'message': 'Welcome ToDos App powered by sqlite'}

#-----------------------------------------------------------------------------#
# Routes: ToDos
#-----------------------------------------------------------------------------#
@app.post("/todos", tags=['Todos'], status_code=status.HTTP_201_CREATED)
async def create_todoitem(db: DB_DEPENDENCY, item: TodoRequest):
    new_item = model.Todos(**item.model_dump())
    db.add(new_item)
    db.commit()

@app.get("/todos", tags=['Todos'])
async def get_todos(db: DB_DEPENDENCY, complete: Optional[bool] = None,
                    priority: Optional[int] = Query(gt=0, lt=6, default=None)):
    if complete is not None:
        res = db.query(model.Todos).filter(model.Todos.complete == complete).all()
        if res:
            return res
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')

    if priority is not None:
        res = db.query(model.Todos).filter(model.Todos.priority == priority).all()
        if res:
            return res
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')

    return db.query(model.Todos).all()

@app.get("/todos/{id}", tags=['Todos'], status_code=status.HTTP_200_OK)
async def get_todo_item(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    item = db.query(model.Todos).filter(model.Todos.id == id).first()
    if item:
        return item
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')

@app.put("/todos/{id}", tags=['Todos'], status_code=status.HTTP_204_NO_CONTENT)
async def update_todoitem(db: DB_DEPENDENCY,
                          item: TodoRequest,
                          id: int = Path(gt=0)):
    todoitem = db.query(model.Todos).filter(model.Todos.id == id).first()
    if not todoitem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')
    
    todoitem.title = item.title
    todoitem.description = item.description
    todoitem.priority = item.priority
    todoitem.complete = item.complete

    db.add(todoitem)
    db.commit()

@app.delete("/todos/{id}", tags=['Todos'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_todoitem(db: DB_DEPENDENCY, id: int = Path(gt=0)):
    todoitem = db.query(model.Todos).filter(model.Todos.id == id).first()
    if not todoitem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')
    
    db.query(model.Todos).filter(model.Todos.id == id).delete()
    db.commit()
