"""

"""

# Builtin imports
from typing import Annotated
from datetime import timedelta, datetime, timezone
import logging

# Project specific imports
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
import jwt

# Local imports
from ..database.model import Users
from ..hashing import Hasher
from ..db_init import DB_DEPENDENCY

# Suppress the passlib warning. 
logging.getLogger('passlib').setLevel(logging.ERROR)

# JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


router = APIRouter()

#-----------------------------------------------------------------------------#
# Models
#-----------------------------------------------------------------------------#
class UserRequest(BaseModel):
    email_address: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

#-----------------------------------------------------------------------------#
# Functions
#-----------------------------------------------------------------------------#

def authenticate_user(db: DB_DEPENDENCY, email_address: str, password: str) -> Users:
    user = db.query(Users).filter(Users.email_address == email_address).first()
    if not user:
        return None
    
    verified = Hasher.verify_password(password, user.hashed_password)
    if not verified:
        return None
    
    return user

def create_access_token(data: dict[str, str], expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})

    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_address = payload.get('sub')
        id = payload.get('id')
        role = payload.get('role')
        if email_address is None or id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
        return {'email_address': email_address, 'id': id, 'role': role}

    except jwt.exceptions.InvalidTokenError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

#-----------------------------------------------------------------------------#
# Routes
#-----------------------------------------------------------------------------#
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: DB_DEPENDENCY, user_data: UserRequest):
    new_user = Users(email_address = user_data.email_address,
                     first_name = user_data.first_name,
                     last_name = user_data.last_name,
                     hashed_password = Hasher.hash_password(user_data.password),
                     active = False,
                     role = user_data.role)
    
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='User already exists')


@router.post("/token", status_code=status.HTTP_201_CREATED, response_model=Token)
async def signin_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                      db: DB_DEPENDENCY) -> Token:
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid signin credentials')
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email_address, "id": user.id, "role": user.role}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


#-----------------------------------------------------------------------------#
# Dependency
#-----------------------------------------------------------------------------#
USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]
