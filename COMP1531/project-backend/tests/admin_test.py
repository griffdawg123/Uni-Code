import pytest
import requests
import json
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.user import user_profile_v1
from src.data import get_users

@pytest.fixture
def user():
    # create a user to be used in the following tests.
    clear_v1()
    return auth_register_v1('name@example.com', 'password123', 'John', 'Smith')

def test_remove_user(user):
    # create two users, one as an owner and assert the other user has been removed correctly
    # note this tests valid use of userpermission as well
    # owner - 1; regular - 0
    user2 = auth_register_v1('user@UNSW.com', 'iloveunsw', 'Steve', 'Jobs')
    assert(len(get_users()) == 2)
    admin_userpermission_change_v1(user['token'], user['auth_user_id'], 1)
    admin_user_remove_v1(user['token'], user2['auth_user_id'])
    deleted_user = user_profile_v1(user['token'], user2['auth_user_id'])
    print(deleted_user)
    assert(deleted_user['user']['name_first'] == 'Removed')
    assert(deleted_user['user']['name_last'] == 'user')

def test_remove_user_access_error(user):
    # create two users and try to remove another, assert AccessError
    user2 = auth_register_v1('user@UNSW.com', 'iloveunsw', 'Steve', 'Jobs')
    with pytest.raises(AccessError):
        admin_user_remove_v1(user2['token'], user['auth_user_id'])

def test_remove_user_invalid_id(user):
    # create a user and try to remove a user that doesn't exist and throws an input error
    with pytest.raises(InputError):
        admin_user_remove_v1(user['token'], 123456789)

def test_remove_self(user):
    # create a user that attempts to remove itself and throws  an input error
    with pytest.raises(InputError):
        admin_user_remove_v1(user['token'], user['auth_user_id'])

def test_user_permission_invalid_user_id(user):
    # create a user and try to change the permissions of a user that doesnt exist
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user['token'], 123456789, 1)

def test_user_permission_invalid_permission_id(user):
    # create a user and try to change the permissions of a user with a permission id that 
    # doesn't exist
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user['token'], user['auth_user_id'], 123456789)

def test_user_permission_access_error(user):
    # create two users and try to change the permissions of the other user 
    # but authorised user is not an owner
    user2 = auth_register_v1('user@UNSW.com', 'iloveunsw', 'Steve', 'Jobs')
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], user['auth_user_id'], 2)