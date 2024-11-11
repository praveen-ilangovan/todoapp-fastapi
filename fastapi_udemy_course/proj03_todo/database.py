"""

"""

# Builtin imports
from typing import Annotated

# Project specific imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

#-----------------------------------------------------------------------------#
# Setup
#-----------------------------------------------------------------------------#
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SESSIONLOCAL = sessionmaker(autoflush=False, bind=ENGINE)
BASE = declarative_base()

#-----------------------------------------------------------------------------#
# Database
#-----------------------------------------------------------------------------#
def get_db():
    db = SESSIONLOCAL()
    try:
        yield db
    finally:
        db.close()

# DB dependency type
DB_DEPENDENCY = Annotated[Session, Depends(get_db)]
