import pytest
import requests
import json
import time
from src.auth import auth_login_v1, auth_register_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1, message_senddm_v1, message_pin_v1, message_unpin_v1, message_unreact_v1, message_react_v1
from src.channel import channel_leave_v1, channel_removeowner_v1, channel_addowner_v1, channel_join_v1, channel_messages_v1
from src.dm import dm_create_v1
from src.data import get_messages
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_share_v1, message_senddm_v1, message_sendlater_v1, message_sendlaterdm_v1
from src.channel import channel_leave_v1, channel_removeowner_v1, channel_addowner_v1, channel_join_v1, channel_messages_v1
from src.dm import dm_create_v1, dm_messages_v1
@pytest.fixture
def user_id():
    #creates a user to be used for the tests
    clear_v1()
    auth_register_v1('john@example.com', 'password123', 'John', 'Smith')
    user_id = auth_login_v1('john@example.com', 'password123')
    yield user_id['token']

@pytest.fixture
def user2_id():
    #creates a user to be used for the tests
    auth_register_v1('joanne@example.com', 'password123', 'Joanne', 'Smith')
    user2_id = auth_login_v1('joanne@example.com', 'password123')
    yield user2_id

@pytest.fixture
def channel_id(user_id):
    #creates a channel to be used for the tests when needed
    #always the first channel one dreams
    channel_id = channels_create_v2(user_id, "General", True)
    return channel_id['channel_id']

##MESSAGE_SEND_V1_TESTS##################################################################

#test if message sends works in a channel
def test_send_message_valid(user_id, channel_id):
    assert(message_send_v1(user_id, channel_id, "Hello world!") == {
        'message_id' : 0
    })

#test if InputError is raised if message > 1000 characters
def test_send_message_invalid_message(user_id, channel_id):
    invalid_message = "Iloveunsw<3."*100
    with pytest.raises(InputError):
        message_send_v1(user_id, channel_id, invalid_message) 

#test if AccessError is raised if user is not part of the channel but is trying to 
#send a message    
def test_send_message_invalid_user(user_id, user2_id, channel_id):
    #user2_id tries to send a message in channel_id  but is not part of it
    with pytest.raises(AccessError):
        message_send_v1(user2_id['token'], channel_id, "Hello world!" ) 

##MESSAGE_EDIT_V1_TESTS##################################################################

#test if InputError is raised if message > 1000 characters
def test_message_edit_invalid_message(user_id, channel_id):

    #create a meassage which is to be edited
    message_id = message_send_v1(user_id, channel_id, "Hello world!")
    invalid_message = "Iloveunsw<3."*100 
    with pytest.raises(InputError):
        message_edit_v1(user_id, message_id['message_id'], invalid_message)

#test if InputError is raised if user wants to edit a message that has been deleted
def test_message_edit_message_id_invalid(user_id, channel_id):

    #create a meassage which is to be deleted
    message_id = message_send_v1(user_id, channel_id, "Hello world!") 

    #delete message
    message_remove_v1(user_id, message_id['message_id'])
    with pytest.raises(InputError):
        message_edit_v1(user_id, message_id['message_id'], "Hi!")

#test if AccessError is raised if another user wants to edit a message 
#the user did not send 
def test_message_edit_invalid_user(user_id, user2_id, channel_id):
    #second user joins the channel
    channel_join_v1(user2_id['token'], channel_id)

    #user_id sends a message in the channel
    message_id = message_send_v1(user_id, channel_id, "Hello world!")

    #user2_id tries to edit the message
    with pytest.raises(AccessError):
        message_edit_v1(user2_id['token'], message_id['message_id'], "Hi!")

#test if AccessError is raised if another user tries edit the message 
#but is also not a owner of the channel or Dreams
def test_message_edit_not_owner(user_id, user2_id, channel_id):

    #user_id is the owner of the channel and Dreams
    #user_id sends a message in channel_id
    message_id = message_send_v1(user_id, channel_id, "Hello world!") 

    #user2_id joins the channel but is only a member
    channel_join_v1(user2_id['token'], channel_id)

    #user2_id tries to edit the message
    with pytest.raises(AccessError):
        message_edit_v1(user2_id['token'], message_id['message_id'], "Hi!")

##MESSAGE_REMOVE_V1_TESTS##################################################################

#test to delete message for channel
def test_message_remove_channel(user_id, channel_id):

    #send a message in the channel
    message_id = message_send_v1(user_id, channel_id, "Hello world!") 

    #delete the message 
    message_remove_v1(user_id, message_id['message_id'])
    messages = get_messages()
    assert(str(message_id['message_id']) not in list(messages.keys()))

#test to delete message for dm
def test_message_remove_dm(user_id, user2_id):
    #create a dm_id with user_id and user2_id
    dm_id = dm_create_v1(user_id, [user2_id['auth_user_id']])

    #send the message in the dm
    message_id = message_senddm_v1(user_id, "Hello world!", dm_id['dm_id']) 

    #delete the message
    message_remove_v1(user_id, message_id['message_id'])
    messages = get_messages()
    assert(str(message_id['message_id']) not in list(messages.keys()))


#test if InputError is raised if user tries to delete an already deleted message
def test_message_remove_inputerror(user_id, channel_id):

    #send the first message in the channel
    message_id = message_send_v1(user_id, channel_id, "Hello world!") 
    
    #delete the message in that channel
    message_remove_v1(user_id, message_id['message_id'])
    with pytest.raises(InputError):
        message_remove_v1(user_id, message_id['message_id'])

#test if AccessError is raised if user2 tries to delete a message user2 did not send
def test_message_remove_invalid_user(user_id, user2_id, channel_id):
    #sends first message in the channel
    message_id = message_send_v1(user_id, channel_id, "Hello world!") 
    with pytest.raises(AccessError):
        message_remove_v1(user2_id['token'], message_id['message_id'])

#tests if AccessError is raised if user2 (not an owner) tries to delete a message
def test_message_remove_not_owner(user_id, user2_id, channel_id):
    #user_id is the owner of the channel and Dreams
    message_id = message_send_v1(user_id, channel_id, "Hello world!") 
    #user2_id joins the channel and is only a member
    channel_join_v1(user2_id['token'], channel_id)
    with pytest.raises(AccessError):
        message_remove_v1(user2_id['token'], message_id['message_id'])

##MESSAGE_SHARE_V1_TESTS##################################################################

#test for sharing a message in a channel
def test_share_message_valid_channel(user_id, channel_id):
    #create a second channel to share og_message and new message to
    channel2_id = channels_create_v2(user_id, "Study1", True)
    #create a message_id and call is og_message_id - first message in Dreams
    og_message_id = message_send_v1(user_id, channel_id, "Hello world!")
    #so now sharing this first message to channel2_id, add on message is "Bye", share_message_id = 2 
    #since it is the second message in Dreams
    assert(message_share_v1(user_id, og_message_id['message_id'], "Bye", channel2_id['channel_id'], -1) == {
        'shared_message_id' : 1
    })

#test for sharing a message in a dm
def test_share_message_valid_dms(user_id, user2_id):
    #create 3rd user for dms
    auth_register_v1('name3@example.com', 'user2121', 'Nicole', 'Chen')
    user3_id = auth_login_v1('name3@example.com', 'user2121')

    #create 2 dms which user_id is a part of for both
    dm_id = dm_create_v1(user_id, [user2_id['auth_user_id']])
    dm2_id = dm_create_v1(user_id, [user3_id['auth_user_id']])

    #create a message_id and call is og_message_id - first message in Dreams in a dm
    og_message_id = message_senddm_v1(user_id, "Hello world!", dm_id['dm_id'])

    #user_id shares a the og_message from dm_id to dm2_id. the shared_message_id = 2 
    #since it is the second message on teams
    assert(message_share_v1(user_id, og_message_id['message_id'], "Bye!", -1, dm2_id['dm_id']) == {
        'shared_message_id' : 1
    })

#test if AccessError is raised if user 2 is trying to share a message to a channel
#they are not a part of
def test_share_message_invalid(user_id, user2_id, channel_id):
    #user2_id is part of channel_id
    channel_join_v1(user2_id['token'], channel_id)
    #user2_id is not part of channel2_id
    channel2_id = channels_create_v2(user_id, "Study1", True)
    
    #create a message_id and call is og_message_id - first message in Dreams
    og_message_id = message_send_v1(user2_id['token'], channel_id, "Hello world!")
    #raise AccessError as user2_id is not part of channel2_id but is trying to share a message there
    with pytest.raises(AccessError):
        message_share_v1(user2_id['token'], og_message_id['message_id'], "Hi", channel2_id['channel_id'], -1) 
    
 ##MESSAGE_SENDDM_V1_TESTS##################################################################   

#test if messages can be sent on dms  
def test_senddm_message_valid(user_id, user2_id):
    #send a dm message on dm_id
    #will be the first message in Dreams
    dm_id = dm_create_v1(user_id, [user2_id['auth_user_id']])
    assert(message_senddm_v1(user_id, "Hello!", dm_id['dm_id'] ) == {
        'message_id' : 0
    })

#test if InputError is raised when message > 1000 characters
def test_senddm_message_invalid_message(user_id, user2_id):
    
    invalid_message = "Iloveunsw<3."*100
    dm_id = dm_create_v1(user_id, [user2_id['auth_user_id']])
    with pytest.raises(InputError):
        message_senddm_v1(user_id, invalid_message, dm_id['dm_id']) 

#test if AccessError is raised when user3 tries to send a message to dm_id when user3 is 
#not part of dm_id
def test_senddm_message_invalid_user(user_id, user2_id):
    auth_register_v1('name3@example.com', 'user2123', 'Nicole', 'Chen')
    user3_id = auth_login_v1('name3@example.com', 'user2123')
    dm_id = dm_create_v1(user_id, [user2_id['auth_user_id']])
    with pytest.raises(AccessError):
        message_senddm_v1(user3_id['token'], "Hi", dm_id['dm_id']) 


##MESSAGE_REACT_V1_TESTS#####################################################################################################################
#args: token, message_id, react_id
def test_react_invalid_message_id(user_id):
    with pytest.raises(InputError):
        message_react_v1(user_id, 895297, 1)


def test_react_invalid_react_id(user_id, channel_id):
    #The only valid react ID the frontend has is 1
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    with pytest.raises(InputError):
        message_react_v1(user_id, message_id, 536457675)


def test_react_invalid_already_reacted(user_id, channel_id):
    #message_id already contains an active React with ID react_id from the authorised user
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_react_v1(user_id, message_id['message_id'], 1)
    with pytest.raises(InputError):
        message_react_v1(user_id, message_id['message_id'], 1)


def test_react_invalid_authuser(user_id, user2_id, channel_id):
    #user is not a member of the channel or DM that the message is within
    #channel_id is created by user_id
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    with pytest.raises(AccessError):
        message_react_v1(user2_id['token'], message_id['message_id'], 1)


def test_react_invalid_spec(user_id, user2_id, channel_id):
    #tests is_this-user_reacted, invalid case
    channel_join_v1(user2_id['token'], channel_id) 
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_react_v1(user_id, message_id['message_id'], 1)
    ##check it actually worked
    messages = channel_messages_v1(user2_id['token'], channel_id, 0)
    assert not (messages['messages'][0]['reacts'][0]['is_this_user_reacted'])


def test_react_valid(user_id, user2_id, channel_id):
    channel_join_v1(user2_id['token'], channel_id) 
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_react_v1(user2_id['token'], message_id['message_id'], 1)
    ##check it actually worked
    messages = channel_messages_v1(user2_id['token'], channel_id, 0)
    assert (messages['messages'][0]['reacts'][0]['is_this_user_reacted'])


##MESSAGE_UNREACT_V1_TESTS################################################################################################################################
def test_unreact_invalid_message_id(user_id, channel_id):
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_react_v1(user_id, message_id['message_id'], 1)
    with pytest.raises(InputError):
        message_unreact_v1(user_id, 895297, 1)


def test_unreact_invalid_react_id(user_id, channel_id):
    #The only valid react ID the frontend has is 1
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_react_v1(user_id, message_id['message_id'], 1)
    with pytest.raises(InputError):
        message_unreact_v1(user_id, message_id, 536457675)


def test_unreact_invalid_no_react(user_id, channel_id):
    #message_id does not contain an active react_id
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    with pytest.raises(InputError):
        message_unreact_v1(user_id, message_id['message_id'], 1)


def test_unreact_invalid_authuser(user_id, user2_id, channel_id):
    #user is not a member of the channel or DM that the message is within
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_react_v1(user_id, message_id['message_id'], 1)
    with pytest.raises(AccessError):
        message_unreact_v1(user2_id['token'], message_id['message_id'], 1)


def test_unreact_valid(user_id, user2_id, channel_id):
    channel_join_v1(user2_id['token'], channel_id)
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_react_v1(user2_id['token'], message_id['message_id'], 1)
    message_unreact_v1(user2_id['token'], message_id['message_id'], 1)
    messages = channel_messages_v1(user2_id['token'], channel_id, 0)
    assert not (messages['messages'][0]['reacts'][0]['is_this_user_reacted'])



#MESSAGE_PIN_V1_TESTS################################################################################################################################
#args: token, message_id
def test_pin_invalid_message_id(user_id):
    with pytest.raises(InputError):
        message_pin_v1(user_id, 2394720)


def test_pin_invalid_already_pinned(user_id, channel_id):
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_pin_v1(user_id, message_id['message_id'])
    with pytest.raises(InputError):
        message_pin_v1(user_id, message_id['message_id'])


def test_pin_invalid_notowner(user_id, user2_id, channel_id):
    #make user2 member but not owner
    channel_join_v1(user2_id['token'], channel_id)
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    with pytest.raises(AccessError):
        message_pin_v1(user2_id['token'], message_id['message_id'])


def test_pin_invalid_notmember(user_id, user2_id, channel_id):
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    with pytest.raises(AccessError):
        message_pin_v1(user2_id['token'], message_id['message_id'])


def test_pin_valid(user_id, channel_id):
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_pin_v1(user_id, message_id['message_id'])
    messages = channel_messages_v1(user_id, channel_id, 0)
    assert(messages['messages'][0]['is_pinned'])


##MESSAGE_UNPIN_V1_TESTS################################################################################################################################
#args: token, message_id
def test_unpin_invalid_message_id(user_id):
    with pytest.raises(InputError):
        message_unpin_v1(user_id, 2394720)


def test_unpin_invalid_not_pinned(user_id, channel_id):
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    with pytest.raises(InputError):
        message_unpin_v1(user_id, message_id['message_id'])


def test_unpin_invalid_notowner(user_id, user2_id, channel_id):
    channel_join_v1(user2_id['token'], channel_id)
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_pin_v1(user_id, message_id['message_id'])
    with pytest.raises(AccessError):
        message_unpin_v1(user2_id['token'], message_id['message_id'])


def test_unpin_invalid_notmember(user_id, user2_id, channel_id):
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_pin_v1(user_id, message_id['message_id'])
    with pytest.raises(AccessError):
        message_unpin_v1(user2_id['token'], message_id['message_id'])

def test_unpin_valid(user_id, user2_id, channel_id):
    message_id = message_send_v1(user_id, channel_id, "hi hoya")
    message_pin_v1(user_id, message_id['message_id'])
    message_unpin_v1(user_id, message_id['message_id'])
    messages = channel_messages_v1(user_id, channel_id, 0)
    assert not(messages['messages'][0]['is_pinned'])





