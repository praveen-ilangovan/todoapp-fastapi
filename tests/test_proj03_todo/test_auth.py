"""
How to test an async function
"""

from datetime import timedelta
import pytest

from fastapi_udemy_course.proj03_todo.routers import auth

from . import constants as Key

@pytest.mark.asyncio
async def test_get_current_user():

    # Create a token
    user = Key.USER_DATA[0]
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user['email_address'], "id": 1, "role": user['role']},
        expires_delta=access_token_expires
    )


    current_user = await auth.get_current_user(access_token)
    assert current_user['email_address'] == user['email_address']
    assert current_user['id'] == 1
    assert current_user['role'] == user['role']
