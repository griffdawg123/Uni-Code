import pytest
from src.auth import auth_register_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1
from src.error import InputError
import requests
import json
from src import config
import time
from src.message import message_senddm_v1
##im definitely importing too many things 

def approx_eq(a, b, margin):
    return abs(a-b) < margin

@pytest.fixture
def clear_data():
    requests.delete(config.url+'clear/v2')

@pytest.fixture
def first_user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'name@example.com', 'password':'password123', 'name_first':'John', 'name_last':'Smith'}).json()

@pytest.fixture
def second_user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'name2@example.com', 'password':'password234', 'name_first':'Joanne', 'name_last':'Smith'}).json()



##USER PROFILE#########################################################################

#User with u_id is not a valid user
def test_profile_invalid_user(clear_data,first_user):
    response = requests.get(config.url+r'user/profile/v2', json={'token':first_user['token'], 'auth_user_id': 'blah'})
    assert response.status_code == 400

'''''''''''''''''''''''''''''''''''
#user profile valid case covered by set email

'''''''''''''''''''''''''''''''''''

## USER PROFILE SET NAME##############################################################
#name_first is not between 1 and 50 characters
def test_setname_invalid_first(clear_data,first_user):
    response = requests.put(config.url+r'user/profile/setname/v2', json={'token':first_user['token'], 'name_first': "Qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwer", 'name_last':"Smith"})
    assert response.status_code == 400


#name_last is not between 1 and 50 characters
def test_setname_invalid_last(clear_data,first_user):
    response = requests.put(config.url+r'user/profile/setname/v2', json={'token':first_user['token'], 'name_first':"Smith", 'name_last':"Qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwer"})
    assert response.status_code == 400


def test_setname_valid(clear_data,first_user, second_user):
    requests.put(config.url+'user/profile/setname/v2', json={'token':second_user['token'], 'name_first':"Celine",'name_last': "Choo"})
    result = requests.get(config.url+'user/profile/v2', params={'token':second_user['token'], 'u_id': second_user['auth_user_id']}).json()
    assert result['user']['name_first'] == "Celine"
    assert result['user']['name_last'] == "Choo"


##USER PROFILE SET EMAIL#################################################
#email is not of valid email format
def test_setemail_invalid_format(clear_data,first_user):
    response = requests.put(config.url+r'user/profile/setemail/v2', json={'token':first_user['token'], 'email': 'ankitrai326.com'})
    assert response.status_code == 400


#email is already being used
def test_setemail_invalid_inuse(clear_data,first_user, second_user):
    response = requests.put(config.url+r'user/profile/setemail/v2', json={'token':second_user['token'], 'email': 'name@example.com'})
    assert response.status_code == 400


def test_setemail_valid(clear_data,first_user, second_user):
    requests.put(config.url+r'user/profile/setemail/v2', json={'token':first_user['token'], 'email': 'celinechoolingling@example.com'})
    result = requests.get(config.url+r'user/profile/v2', params={'token':second_user['token'], 'u_id': first_user['auth_user_id']}).json()
    print(result)
    assert(result['user']['email'] == 'celinechoolingling@example.com')

##USER PROFILE SET HANDLE#####################################################
def test_sethandle_valid(clear_data,first_user, second_user):
    requests.put(config.url+r'user/profile/sethandle/v2', json={'token':first_user['token'], 'handle_str': 'pizzaparty'})
    result = requests.get(config.url+'user/profile/v2', params={'token':second_user['token'], 'u_id': first_user['auth_user_id']}).json()
    print(result)
    assert(result['user']['handle_str'] == 'pizzaparty')

def test_sethandle_invalid_short(clear_data,first_user):
    response = requests.put(config.url+r'user/profile/sethandle/v2', json={'token':first_user['token'], 'handle_str': 'hi'})
    assert response.status_code == 400
    

def test_sethandle_invalid_long(clear_data, first_user):
    response = requests.put(config.url+r'user/profile/sethandle/v2', json={'token':first_user['token'], 'handle_str': 'thisisdefinitelywaywaywaytoolong'})
    assert response.status_code == 400
    

def test_sethandle_invalid_inuse(clear_data, first_user, second_user):
    response = requests.put(config.url+'user/profile/sethandle/v2', json={'token':second_user['token'], 'handle_str': 'johnsmith'})
    assert response.status_code == 400


def test_user_stats_valid():
    requests.delete(config.url+'clear/v1')
    requests.post(config.url+'auth/register/v2', json={'email': "authname@example.com", 'password': 'abc123', 'name_last' : 'Smith', 'name_first' : 'John'})
    
    user1_id = requests.post(config.url+'auth/login/v2', json={'email': 'authname@example.com', 'password' : 'abc123'}).json() 
    time_1 = int(time.time())
    stats_1 =  requests.get(config.url+"/user/stats/v1", params={'token':user1_id['token']}).json()

    assert (stats_1['channels_joined'][-1]['num_channels_joined']) == 0
    assert approx_eq(time_1, stats_1['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_1['dms_joined'][-1]['num_dms_joined']) == 0
    assert approx_eq(time_1, stats_1['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_1['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_1, stats_1['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_1['involvement_rate']) == 0

    #create other users -- 2 ,3 ,4
    requests.post(config.url+'auth/register/v2', json={'email': 'examplename@example.com', 'password': 'abcd1234', 'name_last' : 'Smith', 'name_first' : 'Joanna'})
    user2_id = requests.post(config.url+'auth/login/v2', json={'email': 'examplename@example.com', 'password' : 'abcd1234'}).json() 

    
    requests.post(config.url+'auth/register/v2', json={'email': 'name3@example.com', 'password': 'user2123', 'name_last' : 'Chen', 'name_first' : 'Nicole'})
    user3_id = requests.post(config.url+'auth/login/v2', json={'email': 'name3@example.com', 'password' : 'user2123'}).json() 

    requests.post(config.url+'auth/register/v2', json={'email': 'name4@example.com', 'password': 'users2123', 'name_last' : 'Choo', 'name_first' : 'Celine'})
    user4_id = requests.post(config.url+'auth/login/v2', json={'email': 'name4@example.com', 'password' : 'users2123'}).json() 

    #create 2 channels
    channel_id_1 = requests.post(config.url+'channels/create/v2', json={"token": user1_id['token'],"name": "General","is_public": True}).json()
    channel_id_2 = requests.post(config.url+'channels/create/v2', json={"token": user2_id['token'],"name": "Discussion","is_public": True}).json()
    time_2 = int(time.time())
    stats_2 = requests.get(config.url+"/user/stats/v1", params={'token':user1_id['token']}).json()

    assert (stats_2['channels_joined'][-1]['num_channels_joined']) == 1
    assert approx_eq(time_2, stats_2['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_2['dms_joined'][-1]['num_dms_joined']) == 0
    assert approx_eq(time_2, stats_2['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_2['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_2, stats_2['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_2['involvement_rate']) == 1/2
    
    
    #create 2 dms
    dm_id_1 = requests.post(config.url+'dm/create/v1', json={"token": user3_id['token'], "u_ids":[user4_id['auth_user_id']]})
    requests.post(config.url+'dm/create/v1', json={"token": user2_id['token'], "u_ids":[user3_id['auth_user_id']]})
    
    #user1 joins channel 2
    requests.post(config.url+'channel/join/v2', json={"token":user1_id['token'],"channel_id":channel_id_2['channel_id']})
    time_3 = int(time.time())
    stats_3 = requests.get(config.url+"/user/stats/v1", params={'token':user1_id['token']}).json()

    assert (stats_3['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_3, stats_3['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_3['dms_joined'][-1]['num_dms_joined']) == 0
    assert approx_eq(time_3, stats_3['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_3['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_3, stats_3['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_3['involvement_rate']) == 1/2

    #user1 joins dm 1
    requests.post(config.url+r'dm/invite/v1', json={'token' : user3_id['token'], 'dm_id' :dm_id_1['dm_id'], 'u_id': user1_id['auth_user_id']})
    time_4 = int(time.time())
    stats_4 = requests.post(config.url+r'users/stats/v2', params={'token' : user1_id['token']})

    assert (stats_4['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_4, stats_4['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_4['dms_joined'][-1]['num_dms_joined']) == 1
    assert approx_eq(time_4, stats_4['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_4['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_4, stats_4['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_4['involvement_rate']) == 3/4
    
    message_senddm_v1(user3_id['token'], "Hello", dm_id_1['dm_id'])

    #user1 sends a message to channel_id_1
    message_id_2 = requests.post(config.url+r'message/send/v2', params={'token' :user1_id['token'], 'channel_id':channel_id_1['channel_id'], 'message': "hi"})
    time_5 = int(time.time())
    stats_5 = requests.post(config.url+r'users/stats/v2', params={'token' : user1_id['token']})
    assert (stats_5['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_5, stats_5['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_5['dms_joined'][-1]['num_dms_joined']) == 1
    assert approx_eq(time_5, stats_5['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_5['messages_sent'][-1]['num_messages_sent']) == 1
    assert approx_eq(time_5, stats_5['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_5['involvement_rate']) == 2/3
    
    

    #check if the number of messages sent by user1 does affect involvement rate
    requests.post(config.url+r'message/remove/v1', params={'token' :user1_id['token'], 'message_id':message_id_2['message_id']})
    time_6 = int(time.time())
    stats_6 = requests.post(config.url+r'users/stats/v2', params={'token' : user1_id['token']})
    assert (stats_6['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_6, stats_6['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_6['dms_joined'][-1]['num_dms_joined']) == 1
    assert approx_eq(time_6, stats_6['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_6['messages_sent'][-1]['num_messages_sent']) == 1
    assert approx_eq(time_6, stats_6['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_6['involvement_rate']) == 4/5

##USERS_STATS_V1#####################################################

def test_users_stats_valid():
    requests.delete(config.url+'clear/v1')

    #auth_register_v1('authname@example.com', 'abc123', 'John', 'Smith')
    requests.post(config.url+'auth/register/v2', json={'email' :'authname@example.com', 'password':'abc123', 'name_first': 'John', 'name_last': 'Smith'})
    #auth_login_v1('authname@example.com', 'abc123')
    user1_id = requests.post(config.url+r'auth/login/v2', json={'email' :'authname@example.com', 'password':'abc123'}).json()
  
    time_1 = int(time.time())
    stats_1 = requests.get(config.url+r'users/stats/v1', params={'token' : user1_id['token']}).json()
    assert (stats_1['channels_exist'][-1]['num_channels_exist']) == 0
    assert approx_eq(time_1, stats_1['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_1['dms_exist'][-1]['num_dms_exist']) == 0
    assert approx_eq(time_1, stats_1['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_1['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_1, stats_1['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_1['utilization_rate']) == 0

    #creating other users 2, 3, 4, 5, 6
    #auth_register_v1('examplename@example.com', 'abcd1234', 'Joanna', 'Smith')
    requests.post(config.url+r'auth/register/v2', params={'email' :'authname@example.com', 'password':'abc1234', 'name_first': 'Joanna', 'name_last': 'Smith'})

    user2_id = requests.post(config.url+r'auth/login/v2', params={'email' :'examplename@example.com', 'password':'abc1234'})  #auth_login_v1('examplename@example.com', 'abcd1234')
    
    #auth_register_v1('name3@example.com', 'user2123', 'Nicole', 'Chen')
    requests.post(config.url+r'auth/register/v2', params={'email' :'name3@example.com', 'password':'user2123', 'name_first': 'Nicole', 'name_last': 'Chen'})

    user3_id = requests.post(config.url+r'auth/login/v2', params={'email' :'name3@example.com', 'password':'user2123'})#auth_login_v1('name3@example.com', 'user2123')
    

    #auth_register_v1('name4@example.com', 'users2123', 'Celine', 'Choo')
    requests.post(config.url+r'auth/register/v2', params={'email' :'name4@example.com', 'password':'users2123', 'name_first': 'Celine', 'name_last': 'Choo'})

    requests.post(config.url+r'auth/login/v2', params={'email' :'name4@example.com', 'password':'users2123'}) #auth_login_v1('name4@example.com', 'users2123')


    #auth_register_v1('name5@example.com', 'hi2123', 'Griffin', 'Doyle')
    requests.post(config.url+r'auth/register/v2', params={'email' :'name5@example.com', 'password':'hi2123', 'name_first': 'Griffin', 'name_last': 'Doyle'})
    requests.post(config.url+r'auth/login/v2', params={'email' :'name5@example.com', 'password':'hi2123'}) #auth_login_v1('name5@example.com', 'hi2123')

    #auth_register_v1('name6@example.com', 'hello2123', 'Karen', 'Smith')
    requests.post(config.url+r'auth/register/v2', params={'email' :'name6@example.com', 'password':'hello2123', 'name_first': 'Karen', 'name_last': 'Smith'})

    requests.post(config.url+r'auth/login/v2', params={'email' :'name6@example.com', 'password':'hello2123'}) #auth_login_v1('name6@example.com', 'hello2123')

    #create 2 channels
    channel_id_1= requests.post(config.url+r'channels/create/v2', json={'token':user1_id['token'], 'name':"General", 'is_public':True})#channels_create_v2(user1_id['token'], "General", True)

    time_2 = int(time.time())
    stats_2 = requests.get(config.url+r'users/stats/v1', params={'token':user1_id['token']}).json() #users_stats_v1(user1_id['token'])

    assert (stats_2['channels_exist'][-1]['num_channels_exist']) == 1
    assert approx_eq(time_2, stats_2['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_2['dms_exist'][-1]['num_dms_exist']) == 0
    assert approx_eq(time_2, stats_2['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_2['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_2, stats_2['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_2['utilization_rate']) == 1/6

    requests.post(config.url+r'channels/create/v2', params={'token':user2_id['token'], 'name':"Discussion", 'is_public':True})  #channels_create_v2(user2_id['token'], "Discussion", True)
    time_3 = int(time.time())
    stats_3 = requests.get(config.url+r'users/stats/v1', params={'token':user1_id['token']})  #users_stats_v1(user1_id['token'])

    assert (stats_3['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_3, stats_3['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_3['dms_exist'][-1]['num_dms_exist']) == 0
    assert approx_eq(time_3, stats_3['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_3['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_3, stats_3['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_3['utilization_rate']) == 1/3
    
    #create one dm
    dm_id_1  = requests.post(config.url+r'dm/create/v1', params={'token' :user2_id['token'], 'u_ids': [user1_id['auth_user_id']]})  #dm_create_v1(user2_id['token'], [user1_id['auth_user_id']])
    time_4 = int(time.time())
    stats_4 = requests.get(config.url+r'users/stats/v1', params={'token':user1_id['token']})   #users_stats_v1(user1_id['token'])

    assert (stats_4['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_4, stats_4['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_4['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_4, stats_4['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_4['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_4, stats_4['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_4['utilization_rate']) == 1/3


    #user3 joins channel 1, utlization_rate will change
    #channel_join_v1(user3_id['token'],channel_id_1['channel_id'])
    requests.post(config.url+r'channels/join/v2', params={'token':user3_id['token'], 'channel_id':channel_id_1['channel_id']})
    time_5 = int(time.time())
    stats_5 = requests.get(config.url+r'users/stats/v1', params={'token':user1_id['token']}) #users_stats_v1(user1_id['token'])
    assert (stats_5['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_5, stats_5['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_5['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_5, stats_5['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_5['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_5, stats_5['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_5['utilization_rate']) == 1/2

    
    #user1 send messages in both channels and dms
    message_id_1 = requests.post(config.url+r'message/send/v2', params={'token' :user1_id['token'], 'channel_id':channel_id_1['channel_id'], 'message': "hi"}) #message_send_v1(user1_id['token'], channel_id_1['channel_id'], "hi")
    time_5 = int(time.time())
    stats_5 = requests.get(config.url+r'users/stats/v1', params={'token':user1_id['token']})  #users_stats_v1(user1_id['token'])

    assert (stats_5['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_5, stats_5['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_5['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_5, stats_5['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_5['messages_exist'][-1]['num_messages_exist']) == 1
    assert approx_eq(time_5, stats_5['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_5['utilization_rate']) == 1/2

    requests.post(config.url+r'message/senddm/v1', params={'token' :user2_id['token'], 'message':"Hello", 'dm_id': dm_id_1['dm_id'] })  #message_senddm_v1(user2_id['token'], "Hello", dm_id_1['dm_id'])
    time_6 = int(time.time())
    stats_6 = requests.get(config.url+r'users/stats/v1', params={'token':user1_id['token']}) #users_stats_v1(user1_id['token'])

    assert (stats_6['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_6, stats_6['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_6['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_6, stats_6['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_6['messages_exist'][-1]['num_messages_exist']) == 2
    assert approx_eq(time_6, stats_6['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_6['utilization_rate']) == 1/2


    #check if the number of messages decrease
    #message_remove_v1(user1_id['token'], message_id_1['message_id'])
    requests.post(config.url+r'message/remove/v1', params={'token' :user1_id['token'], 'message_id':message_id_1['message_id']})
    time_7 = int(time.time())
    stats_7 = requests.get(config.url+r'users/stats/v1', params={'token':user1_id['token']}) #users_stats_v1(user1_id['token'])

    assert (stats_7['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_7, stats_7['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_7['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_7, stats_7['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_7['messages_exist'][-1]['num_messages_exist']) == 1
    assert approx_eq(time_7, stats_7['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_7['utilization_rate']) == 1/2
    
