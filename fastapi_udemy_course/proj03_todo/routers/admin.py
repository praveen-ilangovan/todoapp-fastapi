"""

"""

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Path


# Local imports
from .auth import USER_DEPENDENCY
from ..db_init import DB_DEPENDENCY
from ..database.model import Todos

router = APIRouter()

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(user: USER_DEPENDENCY, db: DB_DEPENDENCY):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    return db.query(Todos).all()

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_todoitem(user: USER_DEPENDENCY, db: DB_DEPENDENCY,  id: int = Path(gt=0)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    todoitem = db.query(Todos).filter(Todos.id == id).first()
    if not todoitem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No item with {id} found')
    
    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()

