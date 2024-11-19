"""

"""

# Builtin imports
import os

# Project specific imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

from dotenv import load_dotenv

# LOAD env file
load_dotenv()

USE_POSTGRES = os.getenv("USE_POSTGRES", "0") == "1"

#-----------------------------------------------------------------------------#
# Setup
#-----------------------------------------------------------------------------#

if USE_POSTGRES:
    SQLALCHEMY_DATABASE_URL = os.environ["DB_URL"].format(
            USER=os.getenv("DB_USER_ID"), PWD=os.getenv("DB_PASSWORD"),
            HOST=os.getenv("DB_HOST"), DBNAME=os.getenv("DB_NAME")
        )
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("DB_SQLITE")
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

print(SQLALCHEMY_DATABASE_URL)
SESSIONLOCAL = sessionmaker(autoflush=False, bind=ENGINE)
BASE = declarative_base()
