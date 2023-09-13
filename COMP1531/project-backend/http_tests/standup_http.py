from src.config import url
from src.error import InputError, AccessError

import pytest
import requests
import datetime
import time

OKAY = 200
INPUT = 400
ACCESS = 403

@pytest.fixture
def clear_data():
    requests.delete(url+'clear/v2')

@pytest.fixture
def user_and_channel(clear_data):
    user = requests.post(url+'auth/register/v2', json={'email':'name@example.com','password':'password123', 'name_last':'Smith', 'name_first':'John'})
    user_json = user.json()
    channel = requests.post(url+'channels/create/v2', json={'token':user_json['token'], 'name':'general', 'is_public':True})
    return [user, channel]

@pytest.fixture
def second_user():
    return requests.post(url+'auth/register/v2', json={'email':'example@name.com','password':'ILOVEUNSW', 'name_last':'Kane','name_first':'Harry'})

## Standup Start ##

    ## valid
def test_valid_start(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 20
    }
    time_now = time.time()
    response = requests.post(url+'standup/start/v1', json=payload)
    assert response.status_code == OKAY
    assert response.json().get('time_finish') > time_now

    ## invalid channel_id
def test_invalid_channel_id(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()
    channel_id = 0
    while channel_id == int(channel.get("channel_id")):
        channel_id += 1

    payload = {
        'token' : user.get('token'),
        'channel_id' : channel_id,
        'length' : 20
    }
    response = requests.post(url+'standup/start/v1', json=payload)
    assert response.status_code == INPUT

    ## standup already active
def test_already_active(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()
    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 20
    }
    requests.post(url+'standup/start/v1', json=payload)
    response = requests.post(url+'standup/start/v1', json=payload)
    assert response.status_code == INPUT

    ## authorised user not in channel
def test_user_not_in_channel(clear_data, user_and_channel, second_user):
    channel = user_and_channel[1].json()
    second_user_json = second_user.json()
    payload = {
        'token' : second_user_json.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 20
    }
    response = requests.post(url+'standup/start/v1', json=payload)
    assert response.status_code == ACCESS
def test_invalid_duration(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()
    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : -1
    }
    response = requests.post(url+'standup/start/v1', json=payload)
    assert response.status_code == INPUT
## Standup Active ##

    ## valid - active
def test_is_active_valid(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 20
    }
    requests.post(url+'standup/start/v1', json=payload)
    response = requests.get(url+'standup/active/v1', params={'token':user.get('token'), 'channel_id':channel.get('channel_id')})
    assert response.status_code == OKAY
    assert response.json().get('is_active')
    ## valid - not active
def test_is_not_active_valid(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    response = requests.get(url+'standup/active/v1', params={'token':user.get('token'), 'channel_id':channel.get('channel_id')})
    assert response.status_code == OKAY
    assert not response.json().get('is_active')
    ## channel ID is not valid
def test_invalid_channel_id_active(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()
    channel_id = 0
    while channel_id == int(channel.get("channel_id")):
        channel_id += 1

    response = requests.get(url+'standup/active/v1', params={'token':user.get('token'), 'channel_id':channel_id})
    assert response.status_code == INPUT
## Standup Send ##

    ## valid - one message - same user
def test_valid_one_message(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 3
    }
    requests.post(url+'standup/start/v1', json=payload)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    print(message_list)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    message = {
        'token' : user.get("token"),
        'channel_id' : channel.get("channel_id"),
        'message' : "Hello World!"
    }
    response = requests.post(url+'standup/send/v1', json=message)
    assert response.status_code == OKAY
    time.sleep(3)
    message_list = requests.get(url+f'/channel/messages/v2?token={user.get("token")}&start=0&channel_id={channel.get("channel_id")}').json()
    assert len(message_list['messages']) == 1

    ## valid - one message - different user
def test_valid_one_message_other(clear_data, user_and_channel, second_user):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()
    second_user_json = second_user.json()
    invite = {
        'token' : user.get("token"),
        'channel_id' : channel.get("channel_id"),
        'u_id' : second_user_json.get("auth_user_id")
    }
    requests.post(url+'channel/invite/v2', json=invite)
    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 3
    }
    requests.post(url+'standup/start/v1', json=payload)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    message = {
        'token' : second_user_json.get("token"),
        'channel_id' : channel.get("channel_id"),
        'message' : "Hello World!"
    }
    response = requests.post(url+'standup/send/v1', json=message)
    assert response.status_code == OKAY
    time.sleep(3)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 1

    ## valid - multiple messages
def test_valid_multiple_message(clear_data, user_and_channel, second_user):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 3
    }
    requests.post(url+'standup/start/v1', json=payload)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    message = {
        'token' : user.get("token"),
        'channel_id' : channel.get("channel_id"),
        'message' : "Hello World!"
    }
    requests.post(url+'standup/send/v1', json=message)
    requests.post(url+'standup/send/v1', json=message)
    requests.post(url+'standup/send/v1', json=message)
    time.sleep(3)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 1

    ## invalid channel
def test_invalid_channel_send(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 3
    }
    requests.post(url+'standup/start/v1', json=payload)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    channel_id = 0
    while channel_id == int(channel.get("channel_id")):
        channel_id += 1
    message = {
        'token' : user.get("token"),
        'channel_id' : channel_id,
        'message' : "Hello World!"
    }
    response = requests.post(url+'standup/send/v1', json=message)
    assert response.status_code == INPUT
    

    ## message length >1000
def test_invalid_too_long(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 3
    }
    requests.post(url+'standup/start/v1', json=payload)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    message = {
        'token' : user.get("token"),
        'channel_id' : channel.get("channel_id"),
        'message' : "A"*1001
    }
    response = requests.post(url+'standup/send/v1', json=message)
    assert response.status_code == INPUT
    
    ## no active standup
def test_no_active_standup(clear_data, user_and_channel):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()

    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    message = {
        'token' : user.get("token"),
        'channel_id' : channel.get("channel_id"),
        'message' : "A"*1001
    }
    response = requests.post(url+'standup/send/v1', json=message)
    assert response.status_code == INPUT

    ## auth user is not a part of the channel
def test_invalid_user_send(clear_data, user_and_channel, second_user):
    user = user_and_channel[0].json()
    channel = user_and_channel[1].json()
    second_user_json = second_user.json()
    payload = {
        'token' : user.get('token'),
        'channel_id' : channel.get('channel_id'),
        'length' : 3
    }
    requests.post(url+'standup/start/v1', json=payload)
    message_list = requests.get(url+'channel/messages/v2', params={'token':user.get('token'), 'channel_id':channel.get('channel_id'), 'start' : 0}).json()
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    message = {
        'token' : second_user_json.get("token"),
        'channel_id' : channel.get("channel_id"),
        'message' : "Hello World!"
    }
    response = requests.post(url+'standup/send/v1', json=message)
    assert response.status_code == ACCESS