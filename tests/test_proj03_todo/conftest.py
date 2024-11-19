"""
Define fixtures
"""

import pytest

# Project specific imports
from fastapi.testclient import TestClient

# Local imports
from fastapi_udemy_course.proj03_todo.app import app
from fastapi_udemy_course.proj03_todo.routers.auth import get_current_user

def current_user():
    return {'email_address': 'praveen@gmail.com', 'id': 1, 'role': 'admin'}

@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_current_user] = current_user
    return TestClient(app)
