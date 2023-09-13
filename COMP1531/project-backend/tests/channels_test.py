import pytest
from src.auth import auth_login_v1, auth_register_v1
from src.channel import channel_invite_v1
from src.channels import channels_create_v2, channels_listall_v2, channels_list_v2
from src.error import InputError
from src.other import clear_v1

# channels_list_v2 - list the channel a given user ID has access to
# channels_listall_v2 - list all channels
# channels_create_v2 - creates a new channel

def test_newchannel_valid():
    clear_v1()
    auth_register_v1('name@example.com', 'abc123', 'John', 'Smith')
    user_id = auth_login_v1('name@example.com', 'abc123')
    assert(channels_create_v2(user_id['token'], "test_1", True) == {
        'channel_id' : '1'
    })

def test_newchannel_invalid():
    clear_v1()
    auth_register_v1('name@example.com', 'abc123', 'John', 'Smith')
    user_id = auth_login_v1('name@example.com', 'abc123')
    with pytest.raises(InputError):
        channels_create_v2(user_id['token'], "thisisachannelnamethatisfartoolongsoitwillcauseanerror", True) 

def test_listall():
    clear_v1()
    auth_register_v1('name@example.com', 'abc123', 'John', 'Smith')
    user_id = auth_login_v1('name@example.com', 'abc123')
    assert(channels_listall_v2(user_id['token']) == {})
    channels_create_v2(user_id['token'], "test_1", True)
    assert(len(channels_listall_v2(user_id['token'])) == 1)
    channels_create_v2(user_id['token'], "test_2", True)
    assert(len(channels_listall_v2(user_id['token'])) == 2)

def test_list():
    clear_v1()
    auth_register_v1('name@example.com', 'abc123', 'John', 'Smith')
    user_id = auth_login_v1('name@example.com', 'abc123')
    assert(channels_list_v2(user_id['token']) == {})
    channel_id = channels_create_v2(user_id['token'], "test_1", True)
    assert(len(channels_listall_v2(user_id['token'])) == 1)

    auth_register_v1('human@example.com', 'password', 'Simon', 'Cowell')
    user_id_new = auth_login_v1('human@example.com', 'password')
    assert(channels_list_v2(user_id_new['token']) == {})
    channel_invite_v1(user_id['token'], channel_id['channel_id'], user_id_new['auth_user_id'])
    assert(len(channels_listall_v2(user_id['token'])) == 1)


