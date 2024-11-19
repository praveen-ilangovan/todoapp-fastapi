"""
Test admin route
"""

from fastapi import status

from . import constants as Key

def test_get_user_data(client):
    response = client.get("/me")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email_address'] == 'praveen@gmail.com'
    
def test_update_user_data(client):
    request_data = {'first_name': 'praveen', 'last_name': 'ilangovan', 'phone_number': '1234567889'}
    response = client.put("/me", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    data = response = client.get("/me").json()
    assert data['phone_number'] == request_data['phone_number']

def test_update_password(client):
    request_data = {'current_password':'test123', 'new_password': 'test1234'}
    response = client.post("/me/update_password", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    data = response = client.get("/me").json()
    assert data['hashed_password'] != Key.HASHED_PASSWORD

def test_update_password_with_wrong_current_pwd(client):
    request_data = {'current_password':'Hello', 'new_password': 'test1234'}
    response = client.post("/me/update_password", json=request_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
