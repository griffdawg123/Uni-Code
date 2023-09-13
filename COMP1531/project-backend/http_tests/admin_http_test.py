import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError

@pytest.fixture
def clear_data():
    requests.delete(config.url+'clear/v2')


@pytest.fixture
def user():
    # create a user to be used in the following tests.
    return requests.post(config.url+r'auth/register/v2', json={'email':'name@example.com', 'password':'password123', 'name_first':'John', 'name_last':'Smith'}).json()

@pytest.fixture
def user2():
    return requests.post(config.url+r'auth/register/v2', json={'email':'user@UNSW.com', 'password':'iloveunsw', 'name_first':'Steve', 'name_last':'Jobs'}).json()

def test_remove_user(clear_data, user, user2):
    # create two users, one as an owner and assert the other user has been removed correctly
    # note this tests valid use of userpermission as well
    # owner - 1; regular - 0
    requests.post(config.url+r'admin/userpermission/change/v1', json={'token' : user['token'], 'u_id' : user['auth_user_id'], 'permission_id' : 1})
    requests.delete(config.url+r'admin/user/remove/v1', json={'token':user['token'], 'u_id':user2['auth_user_id']})
    deleted_user = requests.get(config.url+r'user/profile/v2', params={'token':user['token'], 'u_id':user2['auth_user_id']}).json()
    print(deleted_user)
    assert(deleted_user['user']['name_first'] == 'Removed')
    assert(deleted_user['user']['name_last'] == 'user')

def test_remove_user_access_error(clear_data, user, user2):
    # create two users and try to remove another, assert AccessError
    response = requests.delete(config.url+r'admin/user/remove/v1', json={'token':user2['token'], 'u_id':user['auth_user_id']})
    assert response.status_code == 403

def test_remove_user_invalid_id(clear_data, user):
    # create a user and try to remove a user that doesn't exist and throws an input error
    response = requests.delete(config.url+r'admin/user/remove/v1', json={'token':user['token'], 'u_id':123456789})
    assert response.status_code == 400

def test_remove_self(clear_data, user):
    # create a user that attempts to remove itself and throws  an input error
    response = requests.delete(config.url+r'admin/user/remove/v1', json={'token':user['token'], 'u_id':user['auth_user_id']})
    assert response.status_code == 400

def test_user_permission_invalid_user_id(clear_data, user):
    # create a user and try to change the permissions of a user that doesnt exist
    response = requests.post(config.url+r'admin/userpermission/change/v1', json={'token' : user['token'], 'u_id' : 123456789, 'permission_id' : 1})
    assert response.status_code == 400

def test_user_permission_invalid_permission_id(clear_data, user):
    # create a user and try to change the permissions of a user with a permission id that 
    # doesn't exist
    response = requests.post(config.url+r'admin/userpermission/change/v1', json={'token' : user['token'], 'u_id' : user['auth_user_id'], 'permission_id' : 123456789})
    assert response.status_code == 400

def test_user_permission_access_error(clear_data, user, user2):
    # create two users and try to change the permissions of the other user 
    # but authorised user is not an owner
    response = requests.post(config.url+r'admin/userpermission/change/v1', json={'token' : user2['token'], 'u_id' : user['auth_user_id'], 'permission_id' : 0})
    assert response.status_code == 400