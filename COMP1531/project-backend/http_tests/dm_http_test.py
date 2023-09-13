import pytest
import requests
import json
from src import config
from src.error import InputError, AccessError


##FIXTURES##############################################################################################################################################################################################################
#creates users to be used in the following tests

@pytest.fixture
def clear_data():
    requests.delete(config.url+'clear/v2')

@pytest.fixture
def first_user():
    return requests.post(config.url+r'auth/register/v2', json={'email': 'name@example.com', 'password': 'password123', 'name_first': 'John', 'name_last': 'Smith'}).json()
    
@pytest.fixture
def second_user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'name2@example.com', 'password':'password234', 'name_first':'Joanne', 'name_last':'Smith'}).json()

@pytest.fixture
def third_user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'user@UNSW.com', 'password':'iloveunsw', 'name_first':'Steve', 'name_last':'Jobs'}).json()


 
##DM DETAILS#################################################################################
def test_details_valid(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    details = requests.get(config.url+r'dm/details/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id']}).json()
    assert(len(details['members']) == 3)

def test_details_invalid_authuser(clear_data, first_user, second_user, third_user):
    u_ids = [third_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': second_user['token'], 'u_ids': u_ids}).json()
    response = requests.get(config.url+r'dm/details/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id']})
    assert response.status_code == 403
    
def test_details_invalid_dm_id(clear_data, first_user):
    response = requests.get(config.url+r'dm/details/v1', params={'token': first_user['token'], 'dm_id': 928314})
    assert response.status_code == 400
  
##DM LIST############################################################################################
def test_list_valid(clear_data, first_user, second_user, third_user):
    #dm 1
    u_ids = [ third_user['auth_user_id']]
    requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids})
    #dm 2
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids})
    #checking if it works
    dm_list = requests.get(config.url+r'dm/list/v1', params={'token': first_user['token']}).json()
    print(dm_list)
    assert(len(dm_list['dm']) == 2)

##DM CREATE###########################################################################################
def test_create_valid(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    details = requests.get(config.url+r'dm/details/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id']})
    assert details.status_code == 200

def test_create_invalid_uid(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], 5000]
    response = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids})
    assert response.status_code == 400
    
##DM REMOVE############################################################################################
def test_remove_invalid_dm_id(clear_data, second_user):
    response = requests.delete(config.url+r'dm/remove/v1', json={'token': second_user['token'], 'dm_id': '57588578'})
    assert response.status_code == 400
    
def test_remove_invalid_access(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    response = requests.delete(config.url+r'dm/remove/v1', json={'token': second_user['token'], 'dm_id': dm['dm_id']})
    assert response.status_code == 403
    
def test_remove_valid(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    requests.delete(config.url+r'dm/remove/v1', json={'token': first_user['token'], 'dm_id': dm['dm_id']})
    dm_list = requests.get(config.url+r'dm/list/v1', params={'token': first_user['token']}).json()
    assert(len(dm_list['dm']) == 0)

##DM INVITE#########################################################################################################
def test_invite_invalid_dm_id(clear_data, first_user, third_user):
    response = requests.post(config.url+r'dm/invite/v1', json={'token': first_user['token'], 'dm_id': '34545', 'u_id': third_user['auth_user_id']})
    assert response.status_code == 400
 
def test_invite_invalid_uid(clear_data, first_user, second_user):
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    response = requests.post(config.url+r'dm/invite/v1', json={'token': first_user['token'], 'dm_id': dm['dm_id'], 'u_id': '4753686'})
    assert response.status_code == 400

def test_invite_invalid_auth_user(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    response = requests.post(config.url+r'dm/invite/v1', json={'token': third_user['token'], 'dm_id': dm['dm_id'], 'u_id': third_user['auth_user_id']})
    assert response.status_code == 403
 
def test_invite_valid(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    requests.post(config.url+r'dm/invite/v1', json={'token': first_user['token'], 'dm_id': dm['dm_id'], 'u_id': third_user['auth_user_id']})
    details = requests.get(config.url+r'dm/details/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id']}).json()
    member_list = [details['members'][i]['name_first']+" "+details['members'][i]['name_last'] for i, member in enumerate(details['members'])]
    assert('John Smith' in member_list)
    assert('Joanne Smith' in member_list)
    assert('Steve Jobs' in member_list)

##DM LEAVE################################################################################################
def test_leave_valid(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    requests.post(config.url+r'dm/leave/v1', json={'token':third_user['token'], 'dm_id':dm['dm_id']})
    details = requests.get(config.url+r'dm/details/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id']}).json()
    member_list = [details['members'][i]['name_first']+" "+details['members'][i]['name_last'] for i, member in enumerate(details['members'])]
    assert('John Smith' in member_list)
    assert('Joanne Smith' in member_list)
    assert('Steve Jobs' not in member_list)

def test_leave_invalid_auth_user(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    response = requests.post(config.url+r'dm/leave/v1', json={'token': third_user['token'], 'dm_id': dm['dm_id']})
    assert response.status_code == 403
    
def test_leave_invalid_dm_id(clear_data, first_user):
    response = requests.post(config.url+r'dm/leave/v1', json={'token': first_user['token'], 'dm_id': '4783485'})
    assert response.status_code == 400

##DM MESSAGES###############################################################################################
def test_messages_invalid_auth_user(clear_data, first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    response = requests.get(config.url+r'dm/messages/v1', params={'token': third_user['token'], 'dm_id': dm['dm_id'], 'start': 0})
    assert response.status_code == 403
    
def test_messages_invalid_dm_id(clear_data, first_user):
    response = requests.get(config.url+r'dm/messages/v1', params={'token': first_user['token'], 'dm_id': '489835', 'start': 0})
    assert response.status_code == 400

def test_messages_invalid_index(clear_data, first_user, second_user):
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    requests.post(config.url+r'message/senddm/v1', json={'token': first_user['token'], 'dm_id': dm['dm_id'], 'message': 'hi hoya'})
    response = requests.get(config.url+r'dm/messages/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id'], 'start': 6})
    assert response.status_code == 400
    
def test_messages_valid_50(clear_data, first_user, second_user):
    #test 50 messages
    #user1 creates channel & is owner
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    #user1 sends 60 messages
    for _ in range(60):
        requests.post(config.url+r'message/senddm/v1', json={'token': first_user['token'], 'dm_id': dm['dm_id'], 'message': 'hi hoya'})
    
    result = requests.get(config.url+r'dm/messages/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id'], 'start': 0}).json()
    assert(len(result['messages']) == 50 and int(result['start']) == 0 and int(result['end']) == 50)

def test_messages_valid_5(clear_data, first_user, second_user):
    #test 5 messages
    #user1 creates channel & is owner
    u_ids = [second_user['auth_user_id']]
    dm = requests.post(config.url+r'dm/create/v1', json={'token': first_user['token'], 'u_ids': u_ids}).json()
    #user1 sends 5 messages
    for _ in range(5):
        requests.post(config.url+r'message/senddm/v1', json={'token': first_user['token'], 'dm_id': dm['dm_id'], 'message': 'hi hoya'})
    
    result = requests.get(config.url+r'dm/messages/v1', params={'token': first_user['token'], 'dm_id': dm['dm_id'], 'start': 0}).json()
    print(result)
    assert(len(result['messages']) == 5 and int(result['start']) == 0 and int(result['end']) == -1)