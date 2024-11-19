"""

"""

# Project specific imports
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

# Local imports
from ..db_init import DB_DEPENDENCY
from .auth import USER_DEPENDENCY
from ..database.model import Users
from ..hashing import Hasher

router = APIRouter()

#-----------------------------------------------------------------------------#
# Models
#-----------------------------------------------------------------------------#
class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

class UpdateUserData(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: USER_DEPENDENCY, db: DB_DEPENDENCY):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    user_data = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    
    return user_data

@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: USER_DEPENDENCY, db: DB_DEPENDENCY, new_user_data: UpdateUserData):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    user_data = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    
    # Update the user's password
    user_data.first_name = new_user_data.first_name
    user_data.last_name = new_user_data.last_name
    user_data.phone_number = new_user_data.phone_number

    db.add(user_data)
    db.commit()

@router.post("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: USER_DEPENDENCY, db: DB_DEPENDENCY, update_data: UpdatePassword):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    user_data = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    
    # Verify the user's current password
    verified = Hasher.verify_password(update_data.current_password, user_data.hashed_password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is wrong")
    
    # Update the user's password
    user_data.hashed_password = Hasher.hash_password(update_data.new_password)

    db.add(user_data)
    db.commit()
