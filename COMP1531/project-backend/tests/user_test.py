import pytest
import datetime
from src.auth import auth_register_v1, auth_login_v1
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1, user_stats_v1, users_stats_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1, message_senddm_v1
from src.channel import channel_leave_v1, channel_removeowner_v1, channel_addowner_v1, channel_join_v1, channel_messages_v1, channel_invite_v1
from src.dm import dm_create_v1, dm_messages_v1, dm_invite_v1
from src.channels import channels_create_v2
from src.error import InputError
from src.other import clear_v1
from src.data import get_stats, get_users
import time

@pytest.fixture
def first_user():
    clear_v1()
    auth_register_v1('authname@example.com', 'abc123', 'John', 'Smith')
    user1_id = auth_login_v1('authname@example.com', 'abc123')
    yield user1_id
    
@pytest.fixture
def second_user():
    auth_register_v1('hellothere@example.com', 'abc123', 'Joanne', 'Smith')
    user2_id = auth_login_v1('hellothere@example.com', 'abc123')
    yield user2_id


def approx_eq(a, b, margin):
    return abs(a-b) < margin

##USER PROFILE#########################################################################

#User with u_id is not a valid user
def test_profile_invalid_user(first_user):
    with pytest.raises(InputError):
        user_profile_v1(first_user['token'], 'blah')
    

def test_profile_valid(first_user, second_user):
    result = user_profile_v1(second_user['token'], first_user['auth_user_id'])
    assert(result == { 'user': {
            'u_id': '1',
            'email': 'authname@example.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'johnsmith',
        } }
    )

## USER PROFILE SET NAME##############################################################
#name_first is not between 1 and 50 characters
def test_setname_invalid_first(first_user):
    with pytest.raises(InputError):
        user_profile_setname_v1(first_user['token'], "Qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwer", "Smith")


#name_last is not between 1 and 50 characters
def test_setname_invalid_last(first_user):
    with pytest.raises(InputError):
        user_profile_setname_v1(first_user['token'], "John", "Qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwer")


def test_setname_valid(first_user, second_user):
    user_profile_setname_v1(first_user['token'], 'Celine', 'Choo')
    result = user_profile_v1(second_user['token'], first_user['auth_user_id'])
    assert(result == {'user': {
            'u_id': '1',
            'email': 'authname@example.com',
            'name_first': 'Celine',
            'name_last': 'Choo',
            'handle_str': 'johnsmith',
        } }
    )

##USER PROFILE SET EMAIL#################################################
#email is not of valid email format
def test_setemail_invalid_format(first_user):
    with pytest.raises(InputError):
        user_profile_setemail_v1(first_user['token'], 'ankitrai326.com')


#email is already being used
def test_setemail_invalid_inuse(first_user, second_user):
    with pytest.raises(InputError):
        user_profile_setemail_v1(second_user['token'], 'authname@example.com')


def test_setemail_valid(first_user, second_user):
    user_profile_setemail_v1(first_user['token'], 'celinechoolingling@example.com')
    result = user_profile_v1(second_user['token'], first_user['auth_user_id'])
    assert(result == { 'user': {
            'u_id': '1',
            'email': 'celinechoolingling@example.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'johnsmith',
        } }
    )

##USER PROFILE SET HANDLE#####################################################
def test_sethandle_valid(first_user, second_user):
    user_profile_sethandle_v1(first_user['token'], 'pizzaparty')
    result = user_profile_v1(second_user['token'], first_user['auth_user_id'])
    assert(result == { 'user': {
            'u_id': '1',
            'email': 'authname@example.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'pizzaparty',
        } }
    )

def test_sethandle_invalid_short(first_user):
    with pytest.raises(InputError):
        user_profile_sethandle_v1(first_user['token'], 'hi')


def test_sethandle_invalid_long(first_user):
    with pytest.raises(InputError):
        user_profile_sethandle_v1(first_user['token'], 'thisisdefinitelywaywaytoolong')
    

def test_sethandle_invalid_inuse(first_user, second_user):
    with pytest.raises(InputError):
        user_profile_sethandle_v1(second_user['token'], 'johnsmith')
    
   
##USER_STATS_V1#####################################################


def test_user_stats_valid():

    clear_v1()

    
    auth_register_v1('authname@example.com', 'abc123', 'John', 'Smith')
    user1_id = auth_login_v1('authname@example.com', 'abc123')
    time_1 = int(time.time())
    stats_1 = user_stats_v1(user1_id['token'])

    assert (stats_1['channels_joined'][-1]['num_channels_joined']) == 0
    assert approx_eq(time_1, stats_1['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_1['dms_joined'][-1]['num_dms_joined']) == 0
    assert approx_eq(time_1, stats_1['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_1['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_1, stats_1['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_1['involvement_rate']) == 0

    #create other users -- 2 ,3 ,4
    auth_register_v1('examplename@example.com', 'abcd1234', 'Joanna', 'Smith')
    user2_id = auth_login_v1('examplename@example.com', 'abcd1234')

    
    auth_register_v1('name3@example.com', 'user2123', 'Nicole', 'Chen')
    user3_id = auth_login_v1('name3@example.com', 'user2123')

    auth_register_v1('name4@example.com', 'users2123', 'Celine', 'Choo')
    user4_id = auth_login_v1('name4@example.com', 'users2123')

    #create 2 channels
    channel_id_1= channels_create_v2(user1_id['token'], "General", True)
    channel_id_2 = channels_create_v2(user2_id['token'], "Discussion", True)
    time_2 = int(time.time())
    stats_2 = user_stats_v1(user1_id['token'])

    assert (stats_2['channels_joined'][-1]['num_channels_joined']) == 1
    assert approx_eq(time_2, stats_2['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_2['dms_joined'][-1]['num_dms_joined']) == 0
    assert approx_eq(time_2, stats_2['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_2['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_2, stats_2['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_2['involvement_rate']) == 1/2
    
    
    #create 2 dms
    dm_id_1 = dm_create_v1(user3_id['token'], [user4_id['auth_user_id']])
    dm_create_v1(user2_id['token'], [user3_id['auth_user_id']])

    
    #user1 joins channel 2
    channel_join_v1(user1_id['token'],channel_id_2['channel_id'])
    time_3 = int(time.time())
    stats_3 = user_stats_v1(user1_id['token'])

    assert (stats_3['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_3, stats_3['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_3['dms_joined'][-1]['num_dms_joined']) == 0
    assert approx_eq(time_3, stats_3['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_3['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_3, stats_3['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_3['involvement_rate']) == 1/2

    #user1 joins dm 1
    dm_invite_v1(user3_id['token'], dm_id_1['dm_id'], user1_id['auth_user_id'])
    time_4 = int(time.time())
    stats_4 = user_stats_v1(user1_id['token'])

    assert (stats_4['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_4, stats_4['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_4['dms_joined'][-1]['num_dms_joined']) == 1
    assert approx_eq(time_4, stats_4['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_4['messages_sent'][-1]['num_messages_sent']) == 0
    assert approx_eq(time_4, stats_4['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_4['involvement_rate']) == 3/4
    
    message_senddm_v1(user3_id['token'], "Hello", dm_id_1['dm_id'])

    #user1 sends a message to channel_id_1
    message_id_2 = message_send_v1(user1_id['token'], channel_id_1['channel_id'], "hi")
    time_5 = int(time.time())
    stats_5 = user_stats_v1(user1_id['token'])
    assert (stats_5['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_5, stats_5['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_5['dms_joined'][-1]['num_dms_joined']) == 1
    assert approx_eq(time_5, stats_5['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_5['messages_sent'][-1]['num_messages_sent']) == 1
    assert approx_eq(time_5, stats_5['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_5['involvement_rate']) == 2/3
    
    

    #check if the number of messages sent by user1 does affect involvement rate
    message_remove_v1(user1_id['token'], message_id_2['message_id'])
    time_6 = int(time.time())
    stats_6 = user_stats_v1(user1_id['token'])
    assert (stats_6['channels_joined'][-1]['num_channels_joined']) == 2
    assert approx_eq(time_6, stats_6['channels_joined'][-1]['time_stamp'], 2)
    assert (stats_6['dms_joined'][-1]['num_dms_joined']) == 1
    assert approx_eq(time_6, stats_6['dms_joined'][-1]['time_stamp'], 2)
    assert (stats_6['messages_sent'][-1]['num_messages_sent']) == 1
    assert approx_eq(time_6, stats_6['messages_sent'][-1]['time_stamp'], 2)
    assert (stats_6['involvement_rate']) == 4/5



##USERS_STATS_V1#####################################################

def test_users_stats_valid():
    clear_v1()

    auth_register_v1('authname@example.com', 'abc123', 'John', 'Smith')
    user1_id = auth_login_v1('authname@example.com', 'abc123')
    time_1 = int(time.time())
    stats_1 = users_stats_v1(user1_id['token'])

    assert (stats_1['channels_exist'][-1]['num_channels_exist']) == 0
    assert approx_eq(time_1, stats_1['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_1['dms_exist'][-1]['num_dms_exist']) == 0
    assert approx_eq(time_1, stats_1['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_1['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_1, stats_1['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_1['utilization_rate']) == 0

    #creating other users 2, 3, 4, 5, 6
    auth_register_v1('examplename@example.com', 'abcd1234', 'Joanna', 'Smith')
    user2_id = auth_login_v1('examplename@example.com', 'abcd1234')

    
    auth_register_v1('name3@example.com', 'user2123', 'Nicole', 'Chen')
    user3_id = auth_login_v1('name3@example.com', 'user2123')

    auth_register_v1('name4@example.com', 'users2123', 'Celine', 'Choo')
    auth_login_v1('name4@example.com', 'users2123')


    auth_register_v1('name5@example.com', 'hi2123', 'Griffin', 'Doyle')
    auth_login_v1('name5@example.com', 'hi2123')

    auth_register_v1('name6@example.com', 'hello2123', 'Karen', 'Smith')
    auth_login_v1('name6@example.com', 'hello2123')

    #create 2 channels
    channel_id_1= channels_create_v2(user1_id['token'], "General", True)
    time_2 = int(time.time())
    stats_2 = users_stats_v1(user1_id['token'])

    assert (stats_2['channels_exist'][-1]['num_channels_exist']) == 1
    assert approx_eq(time_2, stats_2['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_2['dms_exist'][-1]['num_dms_exist']) == 0
    assert approx_eq(time_2, stats_2['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_2['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_2, stats_2['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_2['utilization_rate']) == 1/6

    channels_create_v2(user2_id['token'], "Discussion", True)
    time_3 = int(time.time())
    stats_3 = users_stats_v1(user1_id['token'])

    assert (stats_3['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_3, stats_3['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_3['dms_exist'][-1]['num_dms_exist']) == 0
    assert approx_eq(time_3, stats_3['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_3['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_3, stats_3['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_3['utilization_rate']) == 1/3
    
    #create one dm
    dm_id_1 = dm_create_v1(user2_id['token'], [user1_id['auth_user_id']])
    time_4 = int(time.time())
    stats_4 = users_stats_v1(user1_id['token'])

    assert (stats_4['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_4, stats_4['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_4['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_4, stats_4['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_4['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_4, stats_4['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_4['utilization_rate']) == 1/3


    #user3 joins channel 1, utlization_rate will change
    channel_join_v1(user3_id['token'],channel_id_1['channel_id'])
    time_5 = int(time.time())
    stats_5 = users_stats_v1(user1_id['token'])
    assert (stats_5['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_5, stats_5['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_5['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_5, stats_5['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_5['messages_exist'][-1]['num_messages_exist']) == 0
    assert approx_eq(time_5, stats_5['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_5['utilization_rate']) == 1/2

    
    #user1 send messages in both channels and dms
    message_id_1 = message_send_v1(user1_id['token'], channel_id_1['channel_id'], "hi")
    time_5 = int(time.time())
    stats_5 = users_stats_v1(user1_id['token'])

    assert (stats_5['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_5, stats_5['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_5['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_5, stats_5['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_5['messages_exist'][-1]['num_messages_exist']) == 1
    assert approx_eq(time_5, stats_5['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_5['utilization_rate']) == 1/2

    message_senddm_v1(user2_id['token'], "Hello", dm_id_1['dm_id'])
    time_6 = int(time.time())
    stats_6 = users_stats_v1(user1_id['token'])

    assert (stats_6['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_6, stats_6['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_6['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_6, stats_6['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_6['messages_exist'][-1]['num_messages_exist']) == 2
    assert approx_eq(time_6, stats_6['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_6['utilization_rate']) == 1/2


    #check if the number of messages decrease
    message_remove_v1(user1_id['token'], message_id_1['message_id'])
    time_7 = int(time.time())
    stats_7 = users_stats_v1(user1_id['token'])

    assert (stats_7['channels_exist'][-1]['num_channels_exist']) == 2
    assert approx_eq(time_7, stats_7['channels_exist'][-1]['time_stamp'], 2)
    assert (stats_7['dms_exist'][-1]['num_dms_exist']) == 1
    assert approx_eq(time_7, stats_7['dms_exist'][-1]['time_stamp'], 2)
    assert (stats_7['messages_exist'][-1]['num_messages_exist']) == 1
    assert approx_eq(time_7, stats_7['messages_exist'][-1]['time_stamp'], 2)
    assert (stats_7['utilization_rate']) == 1/2
