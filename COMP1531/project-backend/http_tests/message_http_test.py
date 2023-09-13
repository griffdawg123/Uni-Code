import pytest
import requests
import json
from src import config
import time

from src.other import decode_token, get_users, get_messages

@pytest.fixture
def clear_data():
    requests.delete(config.url+'clear/v2')

@pytest.fixture
def user_and_channel():
    user = requests.post(config.url+'auth/register/v2', json={'email':'name@example.com','password':'password123', 'name_last':'Smith', 'name_first':'John'}).json()
    channel = requests.post(config.url+'channels/create/v2', json={'token':user['token'], 'name':'general', 'is_public':True}).json()
    return [user, channel]

@pytest.fixture
def second_user():
    return requests.post(config.url+'auth/register/v2', json={'email':'example@name.com','password':'ILOVEUNSW', 'name_last':'Kane','name_first':'Harry'}).json()

##MESSAGE_SEND_V1_TESTS##################################################################
#test if message sends works in a channel
def test_send_message_valid(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'})
    messages = requests.get(config.url+'channel/messages/v2', params={'token':user['token'],'channel_id':channel['channel_id'], 'start':0}).json()
    message_list = [message['message'] for message in messages['messages']]
    assert('Hello world!' in message_list)
#test if InputError is raised if message > 1000 characters
def test_send_message_invalid_message(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    response = requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Iloveunsw<3.'*100})
    assert response.status_code == 400 
#test if AccessError is raised if user is not part of the channel but is trying to 
#send a message    
def test_send_message_invalid_user(clear_data, user_and_channel, second_user):
    channel = user_and_channel[1]
    #user2_id tries to send a message in channel_id  but is not part of it
    response = requests.post(config.url+r'message/send/v2', json={'token' :second_user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'})
    assert response.status_code == 403
##message_edit_v1_TESTS##################################################################
#test if InputError is raised if message > 1000 characters
def test_message_edit_invalid_message(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    #create a meassage which is to be edited
    message_id = requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'}).json()
    response = requests.put(config.url+r'message/edit/v2', json={'token' :user['token'], 'message_id':message_id['message_id'], 'message' : 'Iloveunsw<3.'*100})
    assert response.status_code == 400
#test if InputError is raised if user wants to edit a message that has been deleted
#can also be used to test message_remove_v1_valid
def test_message_edit_message_id_invalid(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    #create a meassage which is to be deleted
    message_id = requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'}).json()
    #delete message
    requests.delete(config.url+r'message/remove/v1', json={'token':user['token'], 'message_id': message_id['message_id']})
    response = requests.put(config.url+r'message/edit/v2', json={'token' :user['token'], 'message_id': message_id['message_id'], 'message' : 'Hi!'})
    assert response.status_code == 400
#test if AccessError is raised if another user wants to edit a message 
#the user did not send and also is not the owner of the channel or Dreams
def test_message_edit_invalid_user(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    #user2 joins the channel
    requests.post(config.url+r'channel/join/v2', json={'token' : second_user['token'], 'channel_id': channel['channel_id']})
    #user sends a message in the channel
    message_id = requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'}).json()
    #user2 tries to edit the message
    response = requests.put(config.url+r'message/edit/v2', json={'token' :second_user['token'], 'message_id':message_id['message_id'], 'message' : 'Hi!'})
    assert response.status_code == 403
##MESSAGE_REMOVE_V1_TESTS##################################################################
#as message_remove_v1 was tested above for channel, this test will be testing for dms
def test_message_remove_dm(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    #create dm_id
    dm_id = requests.post(config.url+r'dm/create/v1', json={'token' :user['token'], 'u_ids': [second_user['auth_user_id']]}).json()
    #send the first message in the dm
    message_id = requests.post(config.url+r'message/senddm/v1', json={'token' : user['token'], 'message' : 'Hello world!', 'dm_id':dm_id['dm_id']}).json()
    #delete the message in the dm 
    requests.delete(config.url+r'message/remove/v1', json={'token':user['token'], 'message_id': str(message_id['message_id'])})
    messages = requests.get(config.url+'dm/messages/v1', params={'token' : user['token'], 'dm_id' : dm_id['dm_id'], 'start' : 0}).json()
    assert(len(messages['messages']) == 0)
#test if InputError is raised if user tries to delete an already deleted message
def test_message_remove_inputerror(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    #send the first message in the channel
    message_id = requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'}).json()
    #delete the message in that channel
    requests.delete(config.url+r'message/remove/v1', json={'token':user['token'], 'message_id': message_id['message_id']})
    #user tries to delete the already deleted message 
    response = requests.delete(config.url+r'message/remove/v1', json={'token':user['token'], 'message_id': message_id['message_id']})
    assert response.status_code == 400
#test if AccessError is raised if user2 tries to delete a message user2 did not send
def test_message_remove_invalid_user(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    #sends first message
    message_id = requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'}).json()
    
    #user2 tries to delete the message that was sent by user 
    response = requests.delete(config.url+r'message/remove/v1', json={'token':second_user['token'], 'message_id': message_id['message_id']})
    assert response.status_code == 403
#tests if AccessError is raised if user2 (not an owner) tries to delete a message
def test_message_remove_not_owner(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    #user is the ownder of the channel and Dreams
    message_id = requests.post(config.url+"message/send/v2", json={'token':user['token'], 'channel_id':channel['channel_id'], 'message': "Hello world!"}).json() 
    #user2 joins the channel and is only a member
    requests.post(config.url+r'channel/join/v2', json={'token' :  second_user['token'], 'channel_id': channel['channel_id']})
    response = requests.delete(config.url+r'message/remove/v1', json={'token':second_user['token'], 'message_id': message_id['message_id']})
    assert response.status_code == 403
##MESSAGE_SHARE_V1_TESTS##################################################################
#test for sharing a message in a channel
def test_share_message_valid_channel(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    #create a second channel to share og_message and new message to
    channel2 = requests.post(config.url+r'channels/create/v2', json={'token':user['token'], 'name':'Study1', 'is_public':True}).json()
    #create a message_id and call is og_message_id - first message in Dreams
    og_message_id = requests.post(config.url+r'message/send/v2', json={'token' :user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'}).json()    
    #so now sharing this first message to channel2_id, add on message is "Bye", share_message_id = 2 
    #since it is the second message in Dreams
    requests.post(config.url+r'message/share/v1', json={'token' :user['token'], 'og_message_id' : og_message_id['message_id'],'message' : 'Bye', 'channel_id': channel2['channel_id'], 'dm_id':-1}).json()
    messages = requests.get(config.url+'channel/messages/v2', params={'token' : user['token'], 'channel_id' : channel2['channel_id'], 'start' : 0}).json()
    message_list = [message['message'] for message in messages['messages']]
    assert("Hello world!Bye" in message_list)
#test for sharing a message in a dm
def test_share_message_valid_dms(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    #create 3rd user for dms
    user3 = requests.post(config.url+r'auth/register/v2', json={'email':'name3@example.com', 'password':'user2121', 'name_first':'Nicole', 'name_last':'Chen'}).json()
    #create 2 dms which user is a part of for both, one with user2 and the other with user3
    dm_id = requests.post(config.url+r'dm/create/v1', json={'token' :user['token'], 'u_ids': [second_user['auth_user_id']]}).json()
    dm2_id = requests.post(config.url+r'dm/create/v1', json={'token' :user['token'], 'u_ids': [user3['auth_user_id']]}).json()
    #create a message_id and call is og_message_id - first message in Dreams in a dm
    og_message_id = requests.post(config.url+r'message/senddm/v1', json={'token' :user['token'], 'dm_id':dm_id['dm_id'], 'message' : 'Hello world!'}).json()

    #user shares a the og_message from dm_id to dm2_id. the shared_message_id = 2 
    #since it is the second message on teams
    requests.post(config.url+r'message/share/v1', json={'token' :user['token'], 'og_message_id' : og_message_id['message_id'],'message' : 'Bye', 'channel_id': -1, 'dm_id': dm2_id['dm_id']}).json()
    messages = requests.get(config.url+'dm/messages/v1', params={'token' : user['token'], 'dm_id' : dm2_id['dm_id'], 'start' : 0}).json()
    assert("Hello world!Bye" in messages['messages'])
#test if AccessError is raised if user 2 is trying to share a message to a channel
#they are not a part of
def test_share_message_invalid(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    channel = user_and_channel[1]    
    #second_user is part of channel
    requests.post(config.url+r'channel/join/v2', json={'token' : second_user['token'], 'channel_id': channel['channel_id']})
    #second_user is not part of channel2
    #creating channel2, user is the owner
    channel2 = requests.post(config.url+r'channels/create/v2', json={'token':user['token'], 'name':'Study1', 'is_public':True}).json()
    #create a message_id and call is og_message_id - first message in Dreams
    og_message_id = requests.post(config.url+r'message/send/v2', json={'token' :second_user['token'], 'channel_id':channel['channel_id'], 'message' : 'Hello world!'}).json()
    #raise AccessError as second_user is not part of channel2_id but is trying to share a message there
    response = requests.post(config.url+r'message/share/v1', json={'token' :second_user['token'], 'og_message_id' : og_message_id['message_id'],'message' : 'Hi', 'channel_id': channel2['channel_id'], 'dm_id': -1})
    assert response.status_code == 403
       

 ##MESSAGE_SENDDM_V1_TESTS##################################################################   

 #test if messages can be sent on dms
def test_senddm_message_valid(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    #creates user and second_user dm 
    dm_id = requests.post(config.url+r'dm/create/v1', json={'token' :user['token'], 'u_ids': [second_user['auth_user_id']]}).json()
    #send a dm message on dm_id
    #will be the first message in Dreams
    requests.post(config.url+r'message/senddm/v1', json={'token' :user['token'], 'message' : 'Hello!', 'dm_id':dm_id['dm_id']}).json()
    messages = requests.get(config.url+'dm/messages/v1', params={'token' : user['token'], 'dm_id':dm_id['dm_id'], 'start':0}).json()
    assert ('Hello!' in messages['messages'])
#test if InputError is raised when message > 1000 characters
def test_senddm_message_invalid_message(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    dm_id = requests.post(config.url+r'dm/create/v1', json={'token' :user['token'], 'u_ids': [second_user['auth_user_id']]}).json()
    response = requests.post(config.url+r'message/senddm/v1', json={'token' :user['token'], 'dm_id':dm_id['dm_id'], 'message' : 'Iloveunsw<3.'*100})
    assert response.status_code == 400   
#test if AccessError is raised when user3 tries to send a message to dm_id when user3 is 
#not part of dm_id
def test_senddm_message_invalid_user(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    #create 3rd user for dms
    user3 = requests.post(config.url+r'auth/register/v2', json={'email':'name3@example.com', 'password':'user2121', 'name_first':'Nicole', 'name_last':'Chen'}).json()

    dm_id = requests.post(config.url+r'dm/create/v1', json={'token' :user['token'], 'u_ids':[second_user['auth_user_id']]}).json()
    response = requests.post(config.url+r'message/senddm/v1', json={'token' :user3['token'], 'dm_id':dm_id['dm_id'], 'message' : 'Hi'})
    assert response.status_code == 403
    
