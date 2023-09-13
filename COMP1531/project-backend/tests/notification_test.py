import pytest
from src.other import clear_v1, notifications_get_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v1
from src.message import message_send_v1, message_senddm_v1
from src.channel import channel_invite_v1
from src.data import get_users, get_channels
from src.dm import dm_create_v1

@pytest.fixture
def clear_data():
    clear_v1()

@pytest.fixture
def a_user():
    yield auth_register_v1('name@example.com', 'password123', 'John', 'Smith')

@pytest.fixture
def another_user():
    yield auth_register_v1('example@name.com', '123abc', 'Sarah', 'Chan')

def test_channel_message_notif(clear_data, a_user, another_user):
    user_list = get_users()
    channel_list = get_channels()
    a_user_handle = user_list[str(a_user['auth_user_id'])]['handle_str']
    another_user_handle = user_list[str(another_user['auth_user_id'])]['handle_str']

    channel = channels_create_v2(a_user['token'], 'general', True)
    channel_list = get_channels()
    channel_name = channel_list[str(channel['channel_id'])]['name']
    channel_invite_v1(a_user['token'], channel['channel_id'], another_user['auth_user_id'])
    message_send_v1(a_user['token'], channel['channel_id'], f"@{another_user_handle}")

    notif_list = notifications_get_v1(another_user['token'])
    assert(notif_list['notifications'][0]['channel_id'] == channel['channel_id'])
    assert(notif_list['notifications'][0]['dm_id'] == -1)
    assert(notif_list['notifications'][0]['notification_message'] == f"{a_user_handle} added you to {channel_name}")
    assert(notif_list['notifications'][1]['channel_id'] == channel['channel_id'])
    assert(notif_list['notifications'][1]['dm_id'] == -1)
    assert(notif_list['notifications'][1]['notification_message'] == f"{a_user_handle} tagged you in {channel_name}: @{another_user_handle}")

def test_dm_message_notif(clear_data, a_user, another_user):
    user_list = get_users()
    a_user_handle = user_list[str(a_user['auth_user_id'])]['handle_str']
    another_user_handle = user_list[str(another_user['auth_user_id'])]['handle_str']

    dm = dm_create_v1(a_user['token'], [another_user['auth_user_id']])
    message_senddm_v1(a_user['token'], f"@{another_user_handle}", dm['dm_id'])

    notif_list = notifications_get_v1(another_user['token'])
    assert(notif_list['notifications'][0]['channel_id'] == -1)
    assert(notif_list['notifications'][0]['dm_id'] == dm['dm_id'])
    assert(notif_list['notifications'][0]['notification_message'] == f"{a_user_handle} added you to {dm['dm_name']}")
    assert(notif_list['notifications'][1]['channel_id'] == -1)
    assert(notif_list['notifications'][1]['dm_id'] == dm['dm_id'])
    assert(notif_list['notifications'][1]['notification_message'] == f"{a_user_handle} tagged you in {dm['dm_name']}: @{another_user_handle}")

def test_mixed_all_notif(clear_data, a_user, another_user):
    user_list = get_users()
    
    a_user_handle = user_list[str(a_user['auth_user_id'])]['handle_str']
    another_user_handle = user_list[str(another_user['auth_user_id'])]['handle_str']

    channel = channels_create_v2(a_user['token'], 'general', True)
    channel_list = get_channels()
    channel_name = channel_list[str(channel['channel_id'])]['name']
    channel_invite_v1(a_user['token'], channel['channel_id'], another_user['auth_user_id'])
    message_send_v1(a_user['token'], channel['channel_id'], f"@{another_user_handle}")

    dm = dm_create_v1(a_user['token'], [another_user['auth_user_id']])
    message_senddm_v1(a_user['token'], f"@{another_user_handle}", dm['dm_id'])
    notif_list = notifications_get_v1(another_user['token'])
    print(notif_list)
    assert(notif_list['notifications'][0]['channel_id'] == channel['channel_id'])
    assert(notif_list['notifications'][0]['dm_id'] == -1)
    assert(notif_list['notifications'][0]['notification_message'] == f"{a_user_handle} added you to {channel_name}")
    assert(notif_list['notifications'][1]['channel_id'] == channel['channel_id'])
    assert(notif_list['notifications'][1]['dm_id'] == -1)
    assert(notif_list['notifications'][1]['notification_message'] == f"{a_user_handle} tagged you in {channel_name}: @{another_user_handle}")
    assert(notif_list['notifications'][2]['channel_id'] == -1)
    assert(notif_list['notifications'][2]['dm_id'] == dm['dm_id'])
    assert(notif_list['notifications'][2]['notification_message'] == f"{a_user_handle} added you to {dm['dm_name']}")
    assert(notif_list['notifications'][3]['channel_id'] == -1)
    assert(notif_list['notifications'][3]['dm_id'] == dm['dm_id'])
    assert(notif_list['notifications'][3]['notification_message'] == f"{a_user_handle} tagged you in {dm['dm_name']}: @{another_user_handle}")

def test_none(clear_data, a_user):
    notif_list = notifications_get_v1(a_user['token'])
    assert(len(notif_list['notifications']) == 0)

