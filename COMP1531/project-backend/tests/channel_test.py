import pytest
from src.data import get_channels, get_users, data_clear, decode_token
from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1, channel_details_v1, channel_messages_v1, channel_join_v1, channel_leave_v1, channel_removeowner_v1, channel_addowner_v1
from src.channels import channels_create_v2, channels_list_v2
from src.message import message_send_v1
from src.other import clear_v1

##FIXTURES#####################################################################
#creates users to be used in the following tests

@pytest.fixture
def first_user():
    clear_v1()
    auth_register_v1('authname@example.com', 'abc123', 'John', 'Smith')
    user1_id = auth_login_v1('authname@example.com', 'abc123')
    return user1_id['token']
    
@pytest.fixture
def second_user():  
    auth_register_v1('name@example.com', 'user123', 'Joanne', 'Smith')
    user2_id = auth_login_v1('name@example.com', 'user123')
    return user2_id['auth_user_id']

@pytest.fixture
def third_user():
    auth_register_v1('name3@example.com', 'user3123', 'Celine', 'Smith')
    user3_id = auth_login_v1('name3@example.com', 'user3123')
    return user3_id


##CHANNEL INVITE################################################################################

def test_invite_invalid_channel(first_user, second_user):
    #test function
    with pytest.raises(InputError):
        channel_invite_v1(first_user, 'nonexistent', second_user)

def test_invite_invalid_auth_user(first_user, second_user, third_user):
    #create users and channel
    channel_id = channels_create_v2(third_user['token'], "new_channel", True)
    #test function
    with pytest.raises(AccessError):
        channel_invite_v1(first_user, channel_id['channel_id'], second_user)


def test_invite_invalid_user(first_user):
    channel_id = channels_create_v2(first_user, "new_channel", True)
    #test function
    with pytest.raises(InputError):
        channel_invite_v1(first_user, channel_id['channel_id'], 100)


def test_invite_valid(first_user, third_user):
    channel_id = channels_create_v2(first_user, "general", True)
    #check that everything comes out right
    channel_invite_v1(first_user, channel_id['channel_id'], third_user['auth_user_id'])
    assert(str(channel_id['channel_id']) in list(channels_list_v2(third_user['token']).keys()))
    

##CHANNEL DETAILS####################################################################

def test_details_invalid_channel(first_user):
    #test function
    with pytest.raises(InputError):
        channel_details_v1(first_user, 'nonexistent')

def test_details_invalid_auth_user(first_user, third_user):
    channel_id = channels_create_v2(first_user, "chatting", True)
    #test function
    with pytest.raises(AccessError):
        channel_details_v1(third_user['token'], channel_id['channel_id'])   

def test_details_valid(first_user, third_user):
    users = get_users()
    channel_id = channels_create_v2(third_user['token'], "memes",True)
    #check everything works
    assert(channel_details_v1(third_user['token'], channel_id['channel_id']) == {
        'name': "memes",
        'is_public': True,
        'owner_members': [users[str(third_user['auth_user_id'])]],
        'all_members': [users[str(third_user['auth_user_id'])]]
    })

##CHANNEL JOIN###########################################################################
def test_join_valid(first_user):
    channel_id = channels_create_v2(first_user, "memes",True)
    channel_join_v1(first_user,channel_id['channel_id'])
    #check user is inside
    assert(str(channel_id['channel_id']) in list(channels_list_v2(first_user).keys()))

def test_join_invalid_channel_nonexistent(first_user):
    #test function
    with pytest.raises(InputError):
        channel_join_v1(first_user, 500)
    
##when channel is private
def test_join_invalid_channel_private(first_user, third_user):
    channel_id = channels_create_v2(first_user, "new_channel", False)
    ##testing function
    with pytest.raises(AccessError):
        channel_join_v1(third_user['token'], channel_id['channel_id'])
        

##CHANNEL MESSAGES###############################################################################

def test_messages_invalid_channel(first_user):###unsure abt this test
    with pytest.raises(InputError):
        channel_messages_v1(first_user, 'nope', 0)


def test_messages_invalid_index(first_user):
#start is greater than the total number of messages in the channel
    #do smth w start idk - make it greater than total number of messages
    channel_id = channels_create_v2(first_user, "new_channel", True)
    message_send_v1(first_user, channel_id['channel_id'], 'hi hoya')
    with pytest.raises(InputError):
        channel_messages_v1(first_user, channel_id['channel_id'], 5)


def test_messages_invalid_authuser(first_user, third_user):
    channel_id = channels_create_v2(first_user, "new_channel", True)
    with pytest.raises(AccessError):
        channel_messages_v1(third_user['token'], channel_id['channel_id'], 0)

def test_messages_valid_50(first_user):
    #test 50 messages
    #user1 creates channel & is owner
    channel_id = channels_create_v2(first_user, "new_channel", True)
    #user1 sends 60 messages
    for _ in range(60):
        message_send_v1(first_user, channel_id['channel_id'], 'hi hoya')
    
    result = channel_messages_v1(first_user, channel_id['channel_id'], 0)
    assert(len(result['messages']) == 50 and result['start'] == 0 and result['end'] == 50)


def test_messages_valid_5(first_user):
    #test 5 messages
    #user1 creates channel & is owner
    channel_id = channels_create_v2(first_user, "new_channel", True)
    #user1 sends 5 messages
    for _ in range(5):
        message_send_v1(first_user, channel_id['channel_id'], 'hi hoya')
    
    result = channel_messages_v1(first_user, channel_id['channel_id'], 0)
    assert(len(result['messages']) == 5 and result['start'] == 0 and result['end'] == -1)

##CHANNEL ADD OWNER################################################################
def test_addowner_invalid_channel(first_user, second_user):
    #user1 tries to make user2 an owner in a channel that doesnt exist
    #test function
    with pytest.raises(InputError):
        channel_addowner_v1(first_user, 'nonexistent', second_user)

def test_addowner_invalid_user(first_user, second_user):##this test is iffy
#uid already owner of channel
    channel_id = channels_create_v2(first_user, "new_channel", True)
    channel_invite_v1(first_user, channel_id['channel_id'], second_user)
    channel_addowner_v1(first_user, channel_id['channel_id'], second_user)
    with pytest.raises(InputError):
        channel_addowner_v1(first_user, channel_id['channel_id'], second_user)

def test_addowner_invalid_authuser(first_user, third_user, second_user):
    #user3 creates channel, user1&2 become members and user 1 tries to make user 2 an owner
    #user3 is owner of dreams, therefore all others are dream members
    channel_id = channels_create_v2(third_user['token'], "new_channel", True)
    #make user 1 and 2 members
    channel_invite_v1(third_user['token'], channel_id['channel_id'], second_user)
    channel_join_v1(first_user, channel_id['channel_id'])
    #test error
    with pytest.raises(AccessError):
        channel_addowner_v1(first_user, channel_id['channel_id'], second_user)

def test_addowner_valid(first_user, second_user):
    
    #first user create channel
    channel_id = channels_create_v2(first_user, "new_channel", True)
    #have user2 invited as member
    channel_invite_v1(first_user, channel_id['channel_id'], second_user)
    #user1 makes user2 owner
    channel_addowner_v1(first_user, channel_id['channel_id'], second_user)
    #check if it worked - user2 should be an owner
    channels = get_channels()
    assert(second_user in channels[str(channel_id['channel_id'])]['owners'])
    
##CHANNEL REMOVE OWNER#########################################################
def test_removeowner_invalid_channel(first_user, second_user):
    with pytest.raises(InputError):
        channel_removeowner_v1(first_user, 'nonexistent', second_user)

def test_removeowner_invalid_user(first_user, second_user):
#uid not owner of channel 
    channels_create_v2(first_user, "new_channel", True)
    with pytest.raises(InputError):
        channel_removeowner_v1(first_user, 'nonexistent', second_user)

def test_removeowner_invalid_onlyowner(first_user, third_user):
    #owner tries to remove themselves but cant
    channel_id = channels_create_v2(third_user['token'], "new_channel", True)
    with pytest.raises(InputError):
        channel_removeowner_v1(third_user['token'], channel_id['channel_id'], third_user['auth_user_id'])

def test_removeowner_invalid_useraccess(first_user, third_user):
    #user trying to remove owner is not an owner themselves
    #user3 creates channel - is owner, is aso first to sign up for dreams so is dreams owner
    channel_id = channels_create_v2(third_user['token'], "new_channel", True)
    #user1 joins - is member
    channel_join_v1(first_user, channel_id['channel_id'])
    #user1 tries to remove user3 as owner
    with pytest.raises(AccessError):
        channel_removeowner_v1(first_user, channel_id['channel_id'], third_user['auth_user_id'])

def test_removeowner_valid(first_user, second_user):
    #first user create channel
    channel_id = channels_create_v2(first_user, "new_channel", True)
    #have user2 invited as member
    channel_invite_v1(first_user, channel_id['channel_id'], second_user)
    #user1 makes user2 owner - both owner
    channel_addowner_v1(first_user, channel_id['channel_id'], second_user)
    #user1 removes user2 as owner
    channel_removeowner_v1(first_user, channel_id['channel_id'], second_user)
    #check if it worked - user2 should be an owner
    channels = get_channels()
    assert(second_user not in channels[str(channel_id['channel_id'])]['owners'])
    
##CHANNEL LEAVE#####################################################################
def test_leave_invalid_channel(first_user):
    with pytest.raises(InputError):
        channel_leave_v1(first_user, 'nonexistent')

def test_leave_invalid_auth_user(first_user, third_user):
    channel_id = channels_create_v2(third_user['token'], "new_channel", True)
    with pytest.raises(AccessError):
        channel_leave_v1(first_user, channel_id['channel_id'])

def test_leave_valid(first_user):
    channel_id = channels_create_v2(first_user, "new_channel", True)
    channel_leave_v1(first_user, channel_id['channel_id'])
    assert(str(channel_id['channel_id']) not in channels_list_v2(first_user))
