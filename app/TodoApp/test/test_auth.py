from app.TodoApp.models import Users
from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from fastapi import status
from datetime import timedelta
from jose import jwt
import pytest 


app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user  = await authenticate_user(test_user.username, 'password', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = await authenticate_user('WrongUserName', 'testpassword', db)
    assert non_existent_user is False

    wrong_password_user = await authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, 
                               SECRET_KEY, 
                               algorithms = [ALGORITHM], 
                               options={'verify_signature': False})
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():

    encode = {'sub': 'testuser','id':1,'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'user_name': 'testuser', 'id': 1, 'user_role': 'admin'}