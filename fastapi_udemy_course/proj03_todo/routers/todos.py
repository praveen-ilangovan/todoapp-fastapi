"""

"""

# Builtin imports
from typing import Optional

# Project specific imports
from fastapi import APIRouter, status, Query, HTTPException, Path, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

# Local imports
from ..db_init import DB_DEPENDENCY
from ..database.model import Todos
from .auth import USER_DEPENDENCY, get_current_user
from ..templating import TEMPLATES


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
# Pages
#-----------------------------------------------------------------------------#
def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response

@router.get("/todo-page")
async def show_todo_page(request: Request, db: DB_DEPENDENCY):
    try:
        user  = await get_current_user( request.cookies.get("access_token") )
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
        return TEMPLATES.TemplateResponse("todo.html", {'request': request, 'todos': todos, 'user': user})
    except HTTPException as err:
        return redirect_to_login()

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todoitem(user: USER_DEPENDENCY, db: DB_DEPENDENCY, item: TodoRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    new_item = Todos(**item.model_dump(), owner_id=user.get('id'))
    db.add(new_item)
    db.commit()

@router.get("/")
async def get_todos(user: USER_DEPENDENCY,
                    db: DB_DEPENDENCY,
                    complete: Optional[bool] = None,
                    priority: Optional[int] = Query(gt=0, lt=6, default=None)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    if complete is not None:
        res = db.query(Todos).filter(Todos.owner_id == user.get('id'), Todos.complete == complete).all()
        if res:
            return res
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')

    if priority is not None:
        res = db.query(Todos).filter(Todos.owner_id == user.get('id'), Todos.priority == priority).all()
        if res:
            return res
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')

    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_todo_item(user: USER_DEPENDENCY, db: DB_DEPENDENCY, id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    item = db.query(Todos).filter(Todos.owner_id == user.get('id'), Todos.id == id).first()
    if item:
        return item
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with id:{id} found')

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todoitem(user: USER_DEPENDENCY,
                          db: DB_DEPENDENCY,
                          item: TodoRequest,
                          id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    todoitem = db.query(Todos).filter(Todos.owner_id == user.get('id'),Todos.id == id).first()
    if not todoitem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')
    
    todoitem.title = item.title
    todoitem.description = item.description
    todoitem.priority = item.priority
    todoitem.complete = item.complete

    db.add(todoitem)
    db.commit()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todoitem(user: USER_DEPENDENCY,
                          db: DB_DEPENDENCY, id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    todoitem = db.query(Todos).filter(Todos.owner_id == user.get('id'),Todos.id == id).first()
    if not todoitem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')
    
    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()

