import pytest
import requests
import json
from src import config
from src import error

@pytest.fixture
def clear_data():
    requests.delete(config.url+'clear/v2')

@pytest.fixture
def user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'name@example.com', 'password':'password123', 'name_first':'John', 'name_last':'Smith'}).json()

def test_create_channel_valid(clear_data, user):
    channel = requests.post(config.url+r'channels/create/v2', json={'token':user['token'], 'name':'example', 'is_public':True}).json()
    channel_list = requests.get(config.url+r'channels/listall/v2', params={'token':user['token']}).json()
    new_channel_id = channel['channel_id']
    assert (channel_list[new_channel_id]['name'] == 'example')
    assert (str(user['auth_user_id']) in channel_list[new_channel_id]['authorised_users'])
    assert (channel_list[new_channel_id]['is_public'] == True)

def test_create_channel_invalid(clear_data, user):
    # create a new channel that is invalid and is not in the channels list
    response = requests.post(config.url+r'channels/create/v2', json={'token':user['token'], 'name':'a'*21, 'is_public':True})
    assert response.status_code == 400
    channel_list = requests.get(config.url+r'channels/listall/v2', params={'token':user['token']}).json()
    assert (channel_list == {})

def test_create_multiple_listall(clear_data, user):
    # create multiple channels and check they're listed
    requests.post(config.url+r'channels/create/v2', json={'token':user['token'], 'name':'example1', 'is_public':True})
    requests.post(config.url+r'channels/create/v2', json={'token':user['token'], 'name':'example2', 'is_public':True})
    channel_list = requests.get(config.url+r'channels/listall/v2', params={'token':user['token']}).json()
    assert(len(channel_list) == 2)

def test_invalid_access_list(clear_data, user):
    # create a two users and a channel and assert that one user is not in the channel
    user2 = requests.post(config.url+r'auth/register/v2', json={'email':'example@unsw.com', 'password':'iloveUNSW', 'name_first':'Hayden', 'name_last':'Smith'}).json()
    requests.post(config.url+r'channels/create/v2', json={'token':user['token'], 'name':'example1', 'is_public':True})
    channel_list_one = requests.get(config.url+r'channels/list/v2', params={'token':user['token']}).json()
    channel_list_two = requests.get(config.url+r'channels/list/v2', params={'token':user2['token']}).json()
    assert(len(channel_list_one) == 1)
    assert(len(channel_list_two) == 0)