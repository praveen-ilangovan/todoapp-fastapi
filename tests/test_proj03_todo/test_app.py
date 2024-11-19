"""
Test the main app
"""
import os
from fastapi import status

def test_health(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'health': 'ok'}

def test_url():
    assert os.environ['DB_SQLITE'] == "sqlite:///./test_todosapp.db"
