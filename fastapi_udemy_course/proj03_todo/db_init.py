"""

"""

# Builtin imports
from typing import Annotated

# Project specific imports
from fastapi import Depends
from sqlalchemy.orm import Session

# Local imports
from .database.database import SESSIONLOCAL

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
