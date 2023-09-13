from src.data import get_channels, get_users, update_channels, update_users, data_clear, encode_token
from src.auth import auth_register_v1
from src.other import clear_v1
from src.channels import channels_create_v2, channels_list_v2
from src.error import AccessError
import pytest

def test_invalid_token():
    clear_v1()
    user = auth_register_v1("name@example.com", "password123", "Smith", "John")
    channels_create_v2(user['token'], "general", True)
    hacker = encode_token({
        'auth_user_id' : 420,
        'session_id' : 1
    })
    with pytest.raises(AccessError):
        channels_list_v2(hacker)

def test_clear():
    user1 = { '1' : {
    'firstName': 'John',
    'lastName': 'Smith',
    'email': 'jsmith@example.com',
    } }

    channel1 = {
        '1' : {
            'name': 'general',
            'authorised_users': '1',
            'users': '1',
            'is-public': True
        }
    }

    update_channels(channel1)
    update_users(user1)
    data_clear()
    assert (get_channels() == {})
    assert (get_users() == {})

def test_add():
    data_clear()
    user1 = { '1' : {
    'firstName': 'John',
    'lastName': 'Smith',
    'email': 'jsmith@example.com',
    } }

    channel1 = {
        '1' : {
            'name': 'general',
            'authorised_users': '1',
            'users' : '1',
            'is-public': True
        }
    }

    update_channels(channel1)
    update_users(user1)
    assert (get_channels() == {
        '1' : {
            'name': 'general',
            'authorised_users': '1',
            'users' : '1',
            'is-public': True
        }
    })
    assert (get_users() == { '1' : {
    'firstName': 'John',
    'lastName': 'Smith',
    'email': 'jsmith@example.com',
    } })

def test_update():
    data_clear()
    user1 = { '1' : {
    'firstName': 'John',
    'lastName': 'Smith',
    'email': 'jsmith@example.com',
    } }

    channel1 = {
        '1' : {
            'name': 'general',
            'authorised_users': '1',
            'users' : '1',
            'is-public': True
        }
    }

    update_channels(channel1)
    update_users(user1)
    user1 = { '1' : {
    'firstName': 'Sam',
    'lastName': 'Stones',
    'email': 'sstones@example.com',
    } }
    update_users(user1)
    assert (get_users() == { '1' : {
    'firstName': 'Sam',
    'lastName': 'Stones',
    'email': 'sstones@example.com',
    } })