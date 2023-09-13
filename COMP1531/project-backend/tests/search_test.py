import pytest
from src.auth import auth_register_v1
from src.other import clear_v1, search_v1
from src.channels import channels_create_v2
from src.message import message_send_v1, message_senddm_v1
from src.dm import dm_create_v1
from src.error import InputError

@pytest.fixture
def user():
    # create a user to be used in the following tests.
    clear_v1()
    yield auth_register_v1('name@example.com', 'password123', 'John', 'Smith')

def test_retrieve_messages_channel(user):
    # create a user and a channel and send messages and then retrieve them
    channel = channels_create_v2(user['token'], 'example', True)
    message_send_v1(user['token'], channel['channel_id'], "Hello World!")
    message_send_v1(user['token'], channel['channel_id'], "Goodbye World!")
    message_list = search_v1(user['token'], "World")
    assert (len(message_list['messages']) == 2)


def test_retrieve_messages_dm(user):
    # create a user and a dm and send messages and then retrieve messages
    user2 = auth_register_v1('user@UNSW.com', 'iloveunsw', 'Steve', 'Jobs')
    dm = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_senddm_v1(user['token'], "Hello World!", dm['dm_id'])
    message_senddm_v1(user['token'], "Goodbye World!", dm['dm_id'])
    message_list = search_v1(user['token'], "World")
    assert (len(message_list['messages']) == 2)

def test_retrieve_messages_mixed(user):
    # create a user and a dm and a channel and retrieve messages
    user2 = auth_register_v1('user@UNSW.com', 'iloveunsw', 'Steve', 'Jobs')
    channel = channels_create_v2(user['token'], 'example', True)
    dm = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_send_v1(user['token'], channel['channel_id'], "Hello World!")
    message_senddm_v1(user['token'], "Goodbye World!", dm['dm_id'])
    message_list = search_v1(user['token'], "World")
    assert (len(message_list['messages']) == 2)

def test_retrieve_messages_none(user):
    # check if string does not exist and empty dict is returned
    user2 = auth_register_v1('user@UNSW.com', 'iloveunsw', 'Steve', 'Jobs')
    channel = channels_create_v2(user['token'], 'example', True)
    dm = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_send_v1(user['token'], channel['channel_id'], "Hello World!")
    message_senddm_v1(user['token'], "Goodbye World!", dm['dm_id'])
    message_list = search_v1(user['token'], "UNSW")
    assert (len(message_list['messages']) == 0)

def test_search_invalid(user):
    # check if search throws an input error for charNum >1000
    user2 = auth_register_v1('user@UNSW.com', 'iloveunsw', 'Steve', 'Jobs')
    channel = channels_create_v2(user['token'], 'example', True)
    dm = dm_create_v1(user['token'], [user2['auth_user_id']])
    message_send_v1(user['token'], channel['channel_id'], "Hello World!")
    message_senddm_v1(user['token'], "Goodbye World!", dm['dm_id'])
    with pytest.raises(InputError):
        search_v1(user['token'], "A"*1001)
