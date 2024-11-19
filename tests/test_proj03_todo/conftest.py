"""
Define fixtures
"""

import os
import pytest

# Project specific imports
from fastapi.testclient import TestClient

# Local imports
from fastapi_udemy_course.proj03_todo.app import app
from fastapi_udemy_course.proj03_todo.routers.auth import get_current_user
from fastapi_udemy_course.proj03_todo.database.model import Todos, Users
from fastapi_udemy_course.proj03_todo import db_init

from . import constants as Key

def current_user():
    return {'email_address': 'praveen@gmail.com', 'id': 1, 'role': 'admin'}

#-----------------------------------------------------------------------------#
# Fixtures
#-----------------------------------------------------------------------------#
@pytest.fixture(scope="session")
def test_db():
    # Clear the db file if it exists
    db_url = os.environ['DB_SQLITE']
    if os.path.exists(db_url):
        os.remove(db_url)

    # Get the db instance
    db = next(db_init.get_db())

    # Populate
    for item in Key.TODO_ITEMS:
        db.add( Todos(**item) )
    for user in Key.USER_DATA:
        db.add( Users(**user) )
    db.commit()

    # Yield
    yield db

    # Cleanup
    db.query(Todos).delete()
    db.query(Users).delete()
    db.commit()

@pytest.fixture(scope="session")
def client(test_db):
    app.dependency_overrides[get_current_user] = current_user
    return TestClient(app)

