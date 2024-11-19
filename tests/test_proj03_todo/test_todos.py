"""
Test todos route
"""

from fastapi import status

def test_get_all_todos(client):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()
    assert items[0]['id'] == 1
