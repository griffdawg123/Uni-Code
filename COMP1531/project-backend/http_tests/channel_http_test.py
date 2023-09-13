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
    return requests.post(config.url+r'auth/register/v2', json={'email':'name@example.com', 'password':'password123', 'name_first':'John', 'name_last':'Smith'}).json()

@pytest.fixture
def second_user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'name2@example.com', 'password':'password234', 'name_first':'Joanne', 'name_last':'Smith'}).json()

@pytest.fixture
def third_user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'user@UNSW.com', 'password':'iloveunsw', 'name_first':'Steve', 'name_last':'Jobs'}).json()
    
##CHANNEL INVITE#########################################################################################################################################################################################################

def test_invite_invalid_channel(clear_data, first_user, second_user):
    #firt user invites second user to a nonexistent channel
    response = requests.post(config.url+r'channel/invite/v2', json={'token':first_user['token'], 'channel_id':'nonexistent' , 'u_id':second_user['auth_user_id']})
    assert response.status_code == 400

def test_invite_invalid_auth_user(clear_data, first_user, second_user, third_user):
    #user3 creates channel so user1 and 2 are not owners, then user 1 tries to invite user 2 to channel
    channel = requests.post(config.url+r'channels/create/v2', json={'token':third_user['token'], 'name':'newchannel', 'is_public':True}).json()
    response = requests.post(config.url+r'channel/invite/v2', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':second_user['auth_user_id']})
    assert response.status_code == 403

def test_invite_invalid_user(clear_data, first_user):
    #user1 creates a channel and invites a user a does not exist
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    response = requests.post(config.url+r'channel/invite/v2', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':100})
    assert response.status_code == 400

'''''''''''''''''''''''''''''''''''''''
######channel invite valid case ############################################################################
valid case is tested by remove owner valid case
'''''''''''''''''''''''''''''''''''''''

##CHANNEL DETAILS###########################################################################################################################################

def test_details_invalid_channel(clear_data, first_user):
    #user1 calls the details of a channel that does not exist
    response = requests.get(config.url+r'channel/details/v2', params={'token':first_user['token'], 'channel_id': 404})
    assert response.status_code == 400

def test_details_invalid_auth_user(clear_data, first_user, second_user):
    #channel created by user1, but details for the channel called by user2 who is not in channel
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    response = requests.get(config.url+r'channel/details/v2', params={'token':second_user['token'], 'channel_id':channel['channel_id']})
    assert response.status_code == 403

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
######no channel details valid case yet##################################
def test_details_valid(first_user, second_user):
    data_clear()
    channel_id = channels_create_v1(first_user, "memes",True)
    #check everything works
    assert(channel_details_v1(first_user, channel_id['channel_id']) == {
        'name': "memes",
        'owner_members': [users[first_user]],
        'all_members': [users[first_user]]
    })
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

##CHANNEL JOIN###########################################################################
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
######no channel join valid case yet##################################
covered by test_removeowner_invalid_useraccess
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def test_join_invalid_channel_nonexistent(clear_data, first_user):
    response = requests.post(config.url+r'channel/join/v2', json={'token':first_user['token'], 'channel_id': 404})
    assert response.status_code == 400

##when channel is private
def test_join_invalid_channel_private(clear_data, first_user, second_user):
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':False}).json()
    response = requests.post(config.url+r'channel/join/v2', json={'token':second_user['token'], 'channel_id': channel['channel_id']})
    assert response.status_code == 403

##CHANNEL ADD OWNER################################################################
def test_addowner_invalid_channel(clear_data, first_user, second_user):
    #user1 tries to make user2 an owner in a channel that doesnt exist
    response = requests.post(config.url+r'channel/addowner/v1', json={'token':second_user['token'], 'channel_id': 45, 'u_id':first_user['auth_user_id']})
    assert response.status_code == 400

def test_addowner_invalid_user(clear_data, first_user, second_user):##this test might be iffy
    #uid already owner of channel
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    requests.post(config.url+r'channel/invite/v2', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':second_user['auth_user_id']})
    requests.post(config.url+r'channel/addowner/v1', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':second_user['auth_user_id']})
    response = requests.post(config.url+r'channel/addowner/v1', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':second_user['auth_user_id']})
    assert response.status_code == 400 
    
def test_addowner_invalid_authuser(clear_data, first_user, second_user, third_user):
    channel = requests.post(config.url+r'channels/create/v2', json={'token':third_user['token'], 'name':'newchannel', 'is_public':True}).json()
    #make user 1 and 2 members
    requests.post(config.url+r'channel/invite/v2', json={'token':third_user['token'], 'channel_id': channel['channel_id'], 'u_id':second_user['auth_user_id']})
    requests.post(config.url+r'channel/join/v2', json={'token':first_user['token'], 'channel_id':channel['channel_id']})
    #test error
    response = requests.post(config.url+r'channel/addowner/v1', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':second_user['auth_user_id']})
    assert response.status_code == 403
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
######no channel add owner valid case yet##################################
covered by remove owner
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

##CHANNEL REMOVE OWNER#########################################################

def test_removeowner_invalid_channel(clear_data, first_user, second_user):
    response = requests.post(config.url+r'channel/removeowner/v1', json={'token':first_user['token'], 'channel_id': 'nonexistent', 'u_id':second_user['auth_user_id']})
    assert response.status_code == 400

def test_removeowner_invalid_user(clear_data, first_user, second_user):
    #uid not owner of channel 
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    response = requests.post(config.url+r'channel/removeowner/v1', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':second_user['auth_user_id']})
    response.status_code == 403

def test_removeowner_invalid_onlyowner(clear_data, first_user):
    #owner tries to remove themselves but cant
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    response = requests.post(config.url+r'channel/removeowner/v1', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'u_id':first_user['auth_user_id']})
    assert response.status_code == 400

def test_removeowner_invalid_useraccess(clear_data, first_user, second_user):
    #user trying to remove owner is not an owner themselves
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    requests.post(config.url+r'channel/join/v2', json={'token':second_user['token'], 'channel_id':channel['channel_id']})
    response = requests.post(config.url+r'channel/removeowner/v1', json={'token':second_user['token'], 'channel_id': channel['channel_id'], 'u_id':first_user['auth_user_id']})
    assert response.status_code == 403

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
######no channel remove owner valid case yet##################################
def test_removeowner_valid(first_user, second_user):
    data_clear()
    #first user create channel
    channel_id = channels_create_v1(first_user, "new_channel", True)
    #have user2 invited as member
    channel_invite_v1(first_user, channel_id['channel_id'], second_user)
    #user1 makes user2 owner - both owner
    channel_addowner_v1(first_user, channel_id['channel_id'], second_user)
    #user1 removes user2 as owner
    channel_removeowner_v1(first_user, channel_id['channel_id'], second_user)
    #check if it worked - user2 should be an owner
    assert(second_user not in channels[channel_id]['owners'])

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


##CHANNEL LEAVE#####################################################################
def test_leave_invalid_channel(clear_data, first_user):
    response = requests.post(config.url+r'channel/leave/v1', json={'token':first_user['token'], 'channel_id': 'nonexistent'})
    assert response.status_code == 400

def test_leave_invalid_auth_user(clear_data, first_user, second_user):
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    response = requests.post(config.url+r'channel/leave/v1', json={'token':second_user['token'], 'channel_id': channel['channel_id']})
    assert response.status_code == 403


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
######no channel leave owner valid case yet##################################
def test_leave_valid(first_user):
    data_clear()
    channel_id = channels_create_v1(first_user, "new_channel", True)
    channel_leave_v1(first_user, channel_id['channel_id'])
    assert(channel_id['channel_id'] in channels_list_v1(first_user))

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


##CHANNEL MESSAGES###############################################################################

def test_messages_invalid_channel(clear_data, first_user):###unsure abt this test
    response = requests.get(config.url+r'channel/messages/v2', json={'token':first_user['token'], 'channel_id': 'none', 'start':0})
    assert response.status_code == 400

def test_messages_invalid_index(clear_data, first_user):
    #start is greater than the total number of messages in the channel
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    requests.get(config.url+r'message/send/v2', params={'token':first_user['token'], 'channel_id': channel['channel_id'], 'message':'hi hoya'})
    response = requests.get(config.url+r'channel/messages/v2', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'start':5})
    assert response.status_code == 400

def test_messages_invalid_authuser(clear_data, first_user, second_user):
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    response = requests.get(config.url+r'channel/messages/v2', params={'token':second_user['token'], 'channel_id': channel['channel_id'], 'start':0})
    assert response.status_code == 403

def test_messages_valid_50(clear_data, first_user):
    #test 50 messages
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    for _ in range(60):
        requests.post(config.url+r'message/send/v2', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'message':'hi hoya'})

    result = requests.get(config.url+r'channel/messages/v2', params={'token':first_user['token'], 'channel_id': channel['channel_id'], 'start':0}).json()
    assert(len(result['messages']) == 50 and int(result['start']) == 0 and int(result['end']) == 50)

def test_messages_valid_5(clear_data, first_user):
    #test 5 messages
    channel = requests.post(config.url+r'channels/create/v2', json={'token':first_user['token'], 'name':'newchannel', 'is_public':True}).json()
    for _ in range(5):
        requests.post(config.url+r'message/send/v2', json={'token':first_user['token'], 'channel_id': channel['channel_id'], 'message':'hi hoya'})
    
    result = requests.get(config.url+r'channel/messages/v2', params={'token':first_user['token'], 'channel_id': channel['channel_id'], 'start':0}).json()
    assert(len(result['messages']) == 5 and int(result['start']) == 0 and int(result['end']) == -1)
