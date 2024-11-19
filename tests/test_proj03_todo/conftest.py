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
from fastapi_udemy_course.proj03_todo.database.model import Todos
from fastapi_udemy_course.proj03_todo import db_init

def current_user():
    return {'email_address': 'praveen@gmail.com', 'id': 1, 'role': 'admin'}

@pytest.fixture(scope="session")
def test_db():
    # Clear the db file if it exists
    db_url = os.environ['DB_SQLITE']
    if os.path.exists(db_url):
        os.remove(db_url)

    # Get the db instance
    db = next(db_init.get_db())

    # Populate
    todoitem_1 = Todos(title="Test", description="Test item 1", priority=5, complete=True, owner_id = 1)
    db.add(todoitem_1)
    db.commit()

    # Yield
    yield db

    # Cleanup
    db.query(Todos).filter(Todos.id == 1).delete()
    db.commit()

@pytest.fixture(scope="session")
def client(test_db):
    app.dependency_overrides[get_current_user] = current_user
    return TestClient(app)
