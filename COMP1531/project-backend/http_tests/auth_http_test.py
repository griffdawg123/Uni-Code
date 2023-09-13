#Tests written by Angus Wang z5257803
import pytest
import requests
import json
from src import config
from src import error

@pytest.fixture
def clear_data():
    requests.delete(config.url+'clear/v2')

@pytest.fixture
def user():
    return requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples123', 'name_first':'Pizza', 'name_last':'Party'}).json()
    
def test_login_register_single(clear_data, user):
    # response = requests.post(config.url+r'auth/register/v2', json={
    #     'email': 'valid@gmail.com',
    #     'password': 'apples123',
    #     'name_first': 'Pizza',
    #     'name_last': 'Party',
    # })
    payload_reg = user #response.json()
    
    #The same user login
    response = requests.post(config.url+r'auth/login/v2', json={
        'email': 'valid@gmail.com',
        'password': 'apples123',
    })
    payload_login = response.json()
    assert payload_login['token'] != payload_reg['token']
    assert int(payload_login["auth_user_id"]) == payload_reg["auth_user_id"]
    
    #The same user logout
    response = requests.post(config.url+r'auth/logout/v1', json = {'token':payload_login['token']})
    payload_logout = response.json()
    assert payload_logout['is_success']
    
def test_names_v2(clear_data, user):
    #testing if names used to register are valid
    #testing if first_name is too short
    response = requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples123', 'name_first':'', 'name_last':'Party'})
    assert response.status_code == 400
        #testing if last_name is too short
    response = requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples123', 'name_first':'Pizza', 'name_last':''})
    assert response.status_code == 400
        #testing if first_name is too long
    response = requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples123', 'name_first':'thisnamewillbeinvalidasitwillbeoverfiftycharacterslongwhichisbad', 'name_last':'Party'})
    assert response.status_code == 400
        #testing if last_name is too long
    response = requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples123', 'name_first':'Pizza', 'name_last':'thisnamewillbeinvalidasitwillbeoverfiftycharacterslongwhichisbad'})
    assert response.status_code == 400
        
def test_password_v2(clear_data, user):
    response = requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apple', 'name_first':'', 'name_last':'Party'})
    assert response.status_code == 400
        
def test_email_valid(clear_data, user):
    response = requests.post(config.url+r'auth/register/v2', json={'email':'invalid', 'password':'apples123', 'name_first':'', 'name_last':'Party'})
    assert response.status_code == 400
        
def test_email_used_v2(clear_data, user):
    #Given a user that has already registered, raise InputError if we try to
    #create/register a new user with the same email
    requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples123', 'name_first':'Pizza', 'name_last':'Party'})
    response = requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples1234', 'name_first':'Mash', 'name_last':'Potato'})
    assert response.status_code == 400
    
def test_login_invalid_email(clear_data, user):
    response = requests.post(config.url+r'auth/login/v2', json={'email':'invalid', 'password':'apples123'})
    assert response.status_code == 400
        
def test_login_email_notreg(clear_data):
    response = requests.post(config.url+r'auth/login/v2', json={'email':'valid@gmail.com', 'password':'apples123'})
    assert response.status_code == 400
        
def test_incorrect_password(clear_data):
    requests.post(config.url+r'auth/register/v2', json={'email':'valid@gmail.com', 'password':'apples123', 'name_first':'Pizza', 'name_last':'Party'})
    response = requests.post(config.url+r'auth/login/v2', json={'email':'valid@gmail.com', 'password':'apples'})
    assert response.status_code == 400
        