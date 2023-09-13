import pytest
from src.data import get_channels, get_users, data_clear
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_join_v1
from src.message import message_send_v1, message_senddm_v1
from src.dm import dm_create_v1, dm_list_v1, dm_details_v1, dm_remove_v1, dm_invite_v1, dm_messages_v1, dm_leave_v1
from src.other import clear_v1
from src.user import user_profile_v1
##someone pls fix these imports, idk if theyre right


@pytest.fixture 
def first_user():
    clear_v1()
    auth_register_v1('authname@example.com', 'abc123', 'John', 'Smith')
    user1_id = auth_login_v1('authname@example.com', 'abc123')
    return user1_id

@pytest.fixture
def second_user():
    auth_register_v1('name@example.com', 'user123', 'Joanne', 'Smith')
    user2_id = auth_login_v1('name@example.com', 'user123')
    return user2_id

@pytest.fixture
def third_user():
    auth_register_v1('name3@example.com', 'user3123', 'Celine', 'Smith')
    user3_id = auth_login_v1('name3@example.com', 'user3123')
    return user3_id



##DM DETAILS#################################################################################
def test_details_valid(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    details = dm_details_v1(first_user['token'], dm['dm_id'])
    user1 = user_profile_v1(first_user['token'], first_user['auth_user_id'])
    user2 = user_profile_v1(second_user['token'], second_user['auth_user_id'])
    user3 = user_profile_v1(third_user['token'], third_user['auth_user_id'])

    dm_name = details['name']
    assert user1['user']['handle_str'] in dm_name
    assert user2['user']['handle_str'] in dm_name
    assert user3['user']['handle_str'] in dm_name
    assert len(details['members']) == 3

def test_details_invalid_authuser(first_user, second_user, third_user):
    u_ids = [third_user['auth_user_id']]
    dm = dm_create_v1(second_user['token'], u_ids)
    with pytest.raises(AccessError):
        dm_details_v1(first_user['token'], dm['dm_id'])
    
def test_details_invalid_dm_id(first_user, second_user, third_user):
    with pytest.raises(InputError):
        dm_details_v1(first_user['token'], '928314')
    
##DM LIST############################################################################################
def test_list_valid(first_user, second_user, third_user):
    #dm 1
    u_ids = [ third_user['auth_user_id']]
    dm_create_v1(first_user['token'], u_ids)
    #dm 2
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm_create_v1(first_user['token'], u_ids)
    #checking if it works
    dm_list = dm_list_v1(first_user['token'])
    assert(len(dm_list['dm']) == 2)

##DM CREATE###########################################################################################
def test_create_valid(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    details = dm_details_v1(first_user['token'], dm['dm_id'])
    #check everything worked
    user1 = user_profile_v1(first_user['token'], first_user['auth_user_id'])
    user2 = user_profile_v1(second_user['token'], second_user['auth_user_id'])
    user3 = user_profile_v1(third_user['token'], third_user['auth_user_id'])

    dm_name = details['name']
    assert user1['user']['handle_str'] in dm_name
    assert user2['user']['handle_str'] in dm_name
    assert user3['user']['handle_str'] in dm_name
    assert len(details['members']) == 3

def test_create_invalid_uid(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], '4']
    with pytest.raises(InputError):
        dm_create_v1(first_user['token'], u_ids)
    
##DM REMOVE############################################################################################
def test_remove_invalid_dm_id(first_user, second_user):
    with pytest.raises(InputError):
        dm_remove_v1(second_user['token'], '0239327497')

def test_remove_invalid_access(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    with pytest.raises(AccessError):
        dm_remove_v1(second_user['token'], dm['dm_id'])

def test_remove_valid(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    dm_remove_v1(first_user['token'], dm['dm_id'])
    dm_list = dm_list_v1(first_user['token'])
    assert(len(dm_list['dm']) == 0)

##DM INVITE#########################################################################################################
def test_invite_invalid_dm_id(first_user, second_user):
    with pytest.raises(InputError):
        dm_invite_v1(first_user['token'], '923729', second_user['auth_user_id'])

def test_invite_invalid_uid(first_user, second_user):
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    with pytest.raises(InputError):
        dm_invite_v1(first_user['token'], dm['dm_id'], '9757275')

def test_invite_invalid_auth_user(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    with pytest.raises(AccessError):
        dm_invite_v1(third_user['token'], dm['dm_id'], second_user['auth_user_id'])

def test_invite_valid(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    dm_invite_v1(first_user['token'], dm['dm_id'], third_user['auth_user_id'])
    details = dm_details_v1(first_user['token'], dm['dm_id'])
    user1 = user_profile_v1(first_user['token'], first_user['auth_user_id'])
    user2 = user_profile_v1(second_user['token'], second_user['auth_user_id'])
    user3 = user_profile_v1(third_user['token'], third_user['auth_user_id'])

    dm_name = details['name']
    assert user1['user']['handle_str'] in dm_name
    assert user2['user']['handle_str'] in dm_name
    assert user3['user']['handle_str'] not in dm_name
    assert len(details['members']) == 3

##DM LEAVE################################################################################################
def test_leave_valid(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id'], third_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    details = dm_details_v1(first_user['token'], dm['dm_id'])
    assert(len(details['members']) == 3)
    dm_leave_v1(third_user['token'], dm['dm_id'])
    details = dm_details_v1(first_user['token'], dm['dm_id'])
    assert(len(details['members']) == 2)

def test_leave_invalid_auth_user(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    with pytest.raises(AccessError):
        dm_leave_v1(third_user['token'], dm['dm_id'])

def test_leave_invalid_dm_id(first_user):
    with pytest.raises(InputError):
        dm_leave_v1(first_user['token'], '73453')

##DM MESSAGES###############################################################################################
def test_messages_invalid_auth_user(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    with pytest.raises(AccessError):
        dm_messages_v1(third_user['token'], dm['dm_id'], 0)

def test_messages_invalid_dm_id(first_user):
    with pytest.raises(InputError):
        dm_messages_v1(first_user['token'], '78324', 0)

def test_messages_invalid_index(first_user, second_user, third_user):
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    message_senddm_v1(first_user['token'], 'hi hoya', dm['dm_id'])
    with pytest.raises(AccessError):
        dm_messages_v1(third_user['token'], dm['dm_id'], 6)

def test_messages_valid_50(first_user, second_user):
    #test 50 messages
    #user1 creates channel & is owner
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    #user1 sends 60 messages
    for _ in range(60):
        message_senddm_v1(first_user['token'], 'hi hoya', dm['dm_id'])

    result = dm_messages_v1(first_user['token'], dm['dm_id'], 0)
    assert(len(result['messages']) == 50 and result['start'] == 0 and result['end'] == 50)

def test_messages_valid_5(first_user, second_user):
    #test 5 messages
    #user1 creates channel & is owner
    u_ids = [second_user['auth_user_id']]
    dm = dm_create_v1(first_user['token'], u_ids)
    #user1 sends 5 messages
    for _ in range(5):
        message_senddm_v1(first_user['token'], 'hi hoya', dm['dm_id'])

    result = dm_messages_v1(first_user['token'], dm['dm_id'], 0)
    assert(len(result['messages']) == 5 and result['start'] == 0 and result['end'] == -1)
