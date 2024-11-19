"""
Test todos route
"""

from fastapi import status

from . import constants as Key

# Get all
def test_get_all_todos_admin(client):
    response = client.get("/admin")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()
    assert len(items) == Key.NUMBER_OF_TODO_ITEMS

# Delete anotehr user's item
def test_delete_another_user_item(client):
    items = client.get("/admin").json()
    id_to_delete = [item for item in items if item['owner_id'] == 3][0]['id']

    response = client.delete(f"/admin/{id_to_delete}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
