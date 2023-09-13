from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_create_v2
from src.standup import standup_active_v1, standup_send_v1, standup_start_v1
from src.channel import channel_details_v1, channel_messages_v1, channel_invite_v1

import pytest
import time


OKAY = 200
INPUT = 400
ACCESS = 403

@pytest.fixture
def clear_data():
    clear_v1()
    return

@pytest.fixture
def user_and_channel(clear_data):
    user = auth_register_v1('name@example.com','password123','John','Smith')
    channel = channels_create_v2(user['token'],'general',True)
    return [user, channel]

@pytest.fixture
def second_user():
    return auth_register_v1('example@name.com','ILOVEUNSW','Kane','Harry')

## Standup Start ##
    ## valid
def test_valid_start(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    time_now = time.time()
    response = standup_start_v1(user.get('token'), channel.get('channel_id'), 20)
    assert response.get('time_finish') > time_now

    ## invalid channel_id
def test_invalid_channel_id(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel_id = 0
    while True:
        try:
            channel_details_v1(user.get("token"), channel_id)
        except InputError:
            break
        channel_id += 1

    with pytest.raises(InputError):
        standup_start_v1(user.get("token"), channel_id, 20)
    

    ## standup already active
def test_already_active(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    standup_start_v1(user.get("token"), channel.get("channel_id"), 20)
    with pytest.raises(InputError):
        standup_start_v1(user.get("token"), channel.get("channel_id"), 20)

    ## authorised user not in channel
def test_user_not_in_channel(clear_data, user_and_channel, second_user):
    channel = user_and_channel[1]
    with pytest.raises(AccessError):
        standup_start_v1(second_user.get("token"), channel.get("channel_id"), 20)
def test_invalid_duration(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    with pytest.raises(InputError):
        standup_start_v1(user.get("token"), channel.get("channel_id"), -1)
## Standup Active ##
    ## valid - active
def test_is_active_valid(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    standup_start_v1(user.get("token"), channel.get("channel_id"), 5)
    assert (standup_active_v1(user.get("token"), channel.get("channel_id")))
    ## valid - not active
def test_is_not_active_valid(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    assert not standup_active_v1(user.get("token"), channel.get("channel_id"))['is_active']
    ## channel ID is not valid
def test_invalid_channel_id_active(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel_id = 0
    while True:
        try:
            channel_details_v1(user.get("token"), channel_id)
        except InputError:
            break
        channel_id += 1
    with pytest.raises(InputError):
        standup_active_v1(user.get("token"), channel_id)
## Standup Send ##
    ## valid - one message - same user
def test_valid_one_message(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    standup_start_v1(user.get("token"), channel.get("channel_id"), 5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    standup_send_v1(user.get("token"), channel.get("channel_id"), "Hello World!")
    time.sleep(5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages'][1:]) == 1

    ## valid - one message - different user
def test_valid_one_message_other(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    channel_invite_v1(user.get("token"), channel.get("channel_id"), second_user.get("auth_user_id"))
    standup_start_v1(user.get("token"), channel.get("channel_id"), 5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    standup_send_v1(second_user.get("token"), channel.get("channel_id"), "Hello World!")
    time.sleep(5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 1

    ## valid - multiple messages
def test_valid_multiple_message(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    standup_start_v1(user.get("token"), channel.get("channel_id"), 5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    standup_send_v1(user.get("token"), channel.get("channel_id"), "Hello World!")
    standup_send_v1(user.get("token"), channel.get("channel_id"), "Hello World!")
    standup_send_v1(user.get("token"), channel.get("channel_id"), "Hello World!")
    time.sleep(5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 1

    ## invalid channel
def test_invalid_channel_send(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    standup_start_v1(user.get("token"), channel.get("channel_id"), 5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    channel_id = 0
    while True:
        try:
            channel_details_v1(user.get("token"), channel_id)
        except InputError:
            break
        channel_id += 1
    with pytest.raises(InputError):
        standup_send_v1(user.get("token"), channel_id, "Hello World!")

    ## message length >1000
def test_invalid_too_long(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    standup_start_v1(user.get("token"), channel.get("channel_id"), 5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    with pytest.raises(InputError):
        standup_send_v1(user.get("token"), channel.get("channel_id"), "A"*1001)
    
    ## no active standup
def test_no_active_standup(clear_data, user_and_channel):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    with pytest.raises(InputError):
        standup_send_v1(user.get("token"), channel.get("channel_id"), "Hello World!")

    ## auth user is not a part of the channel
def test_invalid_user_send(clear_data, user_and_channel, second_user):
    user = user_and_channel[0]
    channel = user_and_channel[1]
    standup_start_v1(user.get("token"), channel.get("channel_id"), 5)
    message_list = channel_messages_v1(user.get("token"), channel.get("channel_id"), 0)
    assert len(message_list['messages']) == 0 # since cleared, no messages should be sent
    with pytest.raises(AccessError):
        standup_send_v1(second_user.get("token"), channel.get("channel_id"), "Hello World!")
