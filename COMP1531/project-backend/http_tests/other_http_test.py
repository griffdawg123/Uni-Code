import pytest
import requests
import json
from src.config import url
from src.error import InputError
from src.data import get_users, get_channels

@pytest.fixture
def clear_data():
    requests.delete(url+'clear/v2')

@pytest.fixture
def a_user():
    return requests.post(url+'auth/register/v2', json={'email':'name@example.com', 'password':'password123', 'name_first':'John', 'name_last':'Smith'}).json()

@pytest.fixture
def another_user():
    return requests.post(url+'auth/register/v2', json={'email':'example@name.com', 'password':'123abc', 'name_first':'Sarah', 'name_last':'Chan'}).json()

@pytest.fixture
def user():
    requests.delete(url+'clear/v1')
    yield requests.post(url+r'auth/register/v2', json={'email':'name@example.com', 'password':'password123', 'name_first':'John', 'name_last':'Smith'})

def test_retrieve_messages_channel(clear_data, a_user):
    # create a user and a channel and send messages and then retrieve them
    channel = requests.post(url+r'channels/create/v2', json={'token':a_user['token'], 'name':'example', 'is_public':True}).json()
    requests.post(url+r'message/send/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'message':'Hello World'})
    requests.post(url+r'message/send/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'message':'Goodbye World'})
    message_list = requests.get(url+r'search/v2', params={'token':a_user['token'], 'query_str':"World"}).json()
    assert (len(message_list['messages']) == 2)

def test_retrieve_messages_dm(clear_data, a_user, another_user):
    # create a user and a dm and send messages and then retrieve messages
    dm = requests.post(url+r'dm/create/v1', json={'token':a_user['token'], 'u_ids':[another_user['auth_user_id']]}).json()
    requests.post(url+r'message/senddm/v1', json={'token':a_user['token'], 'message':'Hello World', 'dm_id':dm['dm_id']})
    requests.post(url+r'message/senddm/v1', json={'token':a_user['token'], 'message':'Goodbye World', 'dm_id':dm['dm_id']})
    message_list = requests.get(url+r'search/v2', params={'token':a_user['token'], 'query_str':"World"}).json()
    assert (len(message_list) == 2)

def test_retrieve_messages_mixed(clear_data, a_user, another_user):
    # create a user and a dm and a channel and retrieve messages
    channel = requests.post(url+r'channels/create/v2', json={'token':a_user['token'], 'name':'example', 'is_public':True}).json()
    dm = requests.post(url+r'dm/create/v1', json={'token':a_user['token'], 'u_ids':[another_user['auth_user_id']]}).json()
    requests.post(url+r'message/senddm/v1', json={'token':a_user['token'], 'message':'Hello World', 'dm_id':dm['dm_id']})
    requests.post(url+r'message/send/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'message':'Goodbye World'})
    message_list = requests.get(url+r'search/v2', params={'token':a_user['token'], 'query_str':"World"}).json()
    assert (len(message_list) == 2)

def test_retrieve_messages_none(clear_data, a_user, another_user):
    # check if string does not exist and empty dict is returned
    channel = requests.post(url+r'channels/create/v2', json={'token':a_user['token'], 'name':'example', 'is_public':True}).json()
    dm = requests.post(url+r'dm/create/v1', json={'token':a_user['token'], 'u_ids':[another_user['auth_user_id']]}).json()
    print(dm)
    requests.post(url+r'message/senddm/v1', json={'token':a_user['token'], 'message':'Hello World', 'dm_id':dm['dm_id']})
    requests.post(url+r'message/send/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'message':'Goodbye World'})
    message_list = requests.get(url+r'search/v2', params={'token':a_user['token'], 'query_str':"UNSW"}).json()
    assert (len(message_list['messages']) == 0)

def test_search_invalid(clear_data, a_user, another_user):
    # check if search throws an input error for charNum >1000
    channel = requests.post(url+r'channels/create/v2', json={'token':a_user['token'], 'name':'example', 'is_public':True}).json()
    dm = requests.post(url+r'dm/create/v1', json={'token':a_user['token'], 'u_ids':[another_user['auth_user_id']]}).json()
    requests.post(url+r'message/senddm/v1', json={'token':a_user['token'], 'message':'Hello World', 'dm_id':dm['dm_id']})
    requests.post(url+r'message/send/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'message':'Goodbye World'})
    response = requests.get(url+r'search/v2', params={'token':a_user['token'], 'query_str':"A"*1001})
    assert response.status_code == 400

# Notification tests

def test_channel_message_notif(clear_data, a_user, another_user):
    user_list = get_users()
    a_user_handle = user_list[str(a_user['auth_user_id'])]['handle_str']
    another_user_handle = user_list[str(another_user['auth_user_id'])]['handle_str']

    channel = requests.post(url+'channels/create/v2', json={'token':a_user['token'], 'name':'general', 'is_public':True}).json()
    channel_name = "general"
    requests.post(url+'channel/invite/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'u_id':another_user['auth_user_id']})
    requests.post(url+'message/send/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'message':f"@{another_user_handle}"})

    notif_list = requests.get(url+'notifications/get/v1', params={'token':another_user['token']}).json()['notifications']
    assert(notif_list[0]['channel_id'] == channel['channel_id'])
    assert(notif_list[0]['dm_id'] == -1)
    assert(notif_list[0]['notification_message'] == f"{a_user_handle} added you to {channel_name}")
    assert(notif_list[1]['channel_id'] == channel['channel_id'])
    assert(notif_list[1]['dm_id'] == -1)
    assert(notif_list[1]['notification_message'] == f"{a_user_handle} tagged you in {channel_name}: @{another_user_handle}")

def test_dm_message_notif(clear_data, a_user, another_user):
    user_list = get_users()
    a_user_handle = user_list[str(a_user['auth_user_id'])]['handle_str']
    another_user_handle = user_list[str(another_user['auth_user_id'])]['handle_str']

    dm = requests.post(url+'dm/create/v1', json={'token':a_user['token'], 'u_ids':[another_user['auth_user_id']]}).json()
    requests.post(url+'message/senddm/v1', json={'token':a_user['token'], 'dm_id':dm['dm_id'], 'message':f"@{another_user_handle}"})

    notif_list = requests.get(url+'notifications/get/v1', params={'token':another_user['token']}).json()['notifications']
    assert(notif_list[0]['channel_id'] == -1)
    assert(notif_list[0]['dm_id'] == dm['dm_id'])
    assert(notif_list[0]['notification_message'] == f"{a_user_handle} added you to {dm['dm_name']}")
    assert(notif_list[1]['channel_id'] == -1)
    assert(notif_list[1]['dm_id'] == dm['dm_id'])
    assert(notif_list[1]['notification_message'] == f"{a_user_handle} tagged you in {dm['dm_name']}: @{another_user_handle}")

def test_mixed_all_notif(clear_data, a_user, another_user):
    print(another_user)
    user_list = get_users()
    print(user_list)
    a_user_handle = user_list[str(a_user['auth_user_id'])]['handle_str']
    another_user_handle = user_list[str(another_user['auth_user_id'])]['handle_str']

    channel = requests.post(url+'channels/create/v2', json={'token':a_user['token'], 'name':'general', 'is_public':True}).json()
    channel_name = "general"
    requests.post(url+'channel/invite/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'u_id':another_user['auth_user_id']})
    requests.post(url+'message/send/v2', json={'token':a_user['token'], 'channel_id':channel['channel_id'], 'message':f"@{another_user_handle}"})

    dm = requests.post(url+'dm/create/v1', json={'token':a_user['token'], 'u_ids':[another_user['auth_user_id']]}).json()
    requests.post(url+'message/senddm/v1', json={'token':a_user['token'], 'dm_id':dm['dm_id'], 'message':f"@{another_user_handle}"})
    notif_list = requests.get(url+'notifications/get/v1', params={'token':another_user['token']}).json()['notifications']
    print(notif_list)
    assert(notif_list[0]['channel_id'] == channel['channel_id'])
    assert(notif_list[0]['dm_id'] == -1)
    assert(notif_list[0]['notification_message'] == f"{a_user_handle} added you to {channel_name}")
    assert(notif_list[1]['channel_id'] == channel['channel_id'])
    assert(notif_list[1]['dm_id'] == -1)
    assert(notif_list[1]['notification_message'] == f"{a_user_handle} tagged you in {channel_name}: @{another_user_handle}")
    assert(notif_list[2]['channel_id'] == -1)
    assert(notif_list[2]['dm_id'] == dm['dm_id'])
    assert(notif_list[2]['notification_message'] == f"{a_user_handle} added you to {dm['dm_name']}")
    assert(notif_list[3]['channel_id'] == -1)
    assert(notif_list[3]['dm_id'] == dm['dm_id'])
    assert(notif_list[3]['notification_message'] == f"{a_user_handle} tagged you in {dm['dm_name']}: @{another_user_handle}")

def test_none(clear_data, a_user):
    notif_list = requests.get(url+'notifications/get/v1', params={'token':a_user['token']}).json()
    assert(len(notif_list['notifications']) == 0)
