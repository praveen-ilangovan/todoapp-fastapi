"""

"""

# Project specific imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

#-----------------------------------------------------------------------------#
# Setup
#-----------------------------------------------------------------------------#
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SESSIONLOCAL = sessionmaker(autoflush=False, bind=ENGINE)
BASE = declarative_base()
