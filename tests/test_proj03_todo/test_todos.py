"""
Test todos route
"""

from fastapi import status

from . import constants as Key

# Get all
def test_get_all_todos(client):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()
    assert len(items) == 5

def test_get_all_complete_items(client):
    response = client.get("/todos?complete=true")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()
    assert len(items) == 2

def test_get_all_top_priority_items(client):
    response = client.get("/todos?priority=5")
    assert response.status_code == status.HTTP_200_OK
    items = response.json()
    assert len(items) == 2

def test_get_invalid_priority(client):
    response = client.get("/todos?priority=6")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_unavailable_priority(client):
    response = client.get("/todos?priority=3")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Get an item
def test_get_an_item(client):
    response = client.get("/todos/3")
    assert response.status_code == status.HTTP_200_OK
    item = response.json()
    assert item['id'] == 3

def test_get_an_item(client):
    response = client.get("/todos/11")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Post an item
def test_create_item(client):
    request_data = {'title': 'New',
                    'description': 'Its a new item',
                    'priority': 5,
                    'complete': False}
    response = client.post('/todos', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    items = client.get('/todos').json()
    assert len(items) == 6

# Update an item
def test_update_item(client):
    request_data = {'title': 'TestUpdated',
                    'description': 'Updated description',
                    'priority': 5,
                    'complete': True}
    response = client.put('/todos/2', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    item = client.get('/todos/2').json()
    assert item['title'] == request_data['title']
    assert item['description'] == request_data['description']

def test_update_non_existent_item(client):
    request_data = {'title': 'TestUpdated',
                    'description': 'Updated description',
                    'priority': 5,
                    'complete': True}
    response = client.put('/todos/222', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Delete an item
def test_delete_item(client):
    items = client.get('/todos').json()
    id_to_delete = items[-1]['id']
    response = client.delete(f'/todos/{id_to_delete}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_non_existent_item(client):
    response = client.delete('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND

