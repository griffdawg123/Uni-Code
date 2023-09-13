#Code that tests auth_login_v1 and auth_register_v1 to ensure that 
#the project brief is met. 
#Created by Angus Wang (z5257803) and Benson Chan (z5349371)

import pytest
from src.auth import auth_login_v1, auth_register_v1, auth_passwordreset_reset_v1, auth_passwordreset_request_v1
from src.other import clear_v1
from src.error import InputError
from src.data import decode_token
from src.user import user_profile_v1

regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"

@pytest.fixture
def user_reg_info():
    clear_v1()
    return ('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    
def test_login_register(user_reg_info):
    clear_v1()
    token_1 = auth_register_v1(*user_reg_info)
    token_2 = auth_login_v1('validemail@gmail.com', '123abc!@#')
    data_1 = decode_token(token_1['token'])
    data_2 = decode_token(token_2['token'])
    assert str(data_1['auth_user_id']) == str(data_2['auth_user_id'])
    assert str(data_1['session_id']) != str(data_2['session_id'])

import re    
# def test_register_invalid_email():
#     clear_v1()
#     if(re.search(regex, 'email')):
#         print ("", auth_user_id)
        
#     else:
#         print ("InputError")
        
#     # if __name__ == '__main__' :
    
#     #     email = "validemail@gmail.com"
#     #     test_register_invalid_email(email)
        
#     #     email = "123abc!@#"
#     #     test_register_invalid_email(email)
        
#     #     email = "Hayden"
#     #     test_register_invalid_email(email)
        
#     #     email = "Everest"
#     #     test_register_invalid_email(email)

# def test_login_invalid_email():
#     clear_v1()
#     if(re.search(regex, 'email')):
#         print ("", auth_user_id)
        
#     else:
#         print ("InputError")
        
#     if __name__ == '__main__' :
    
#         email = "validemail@gmail.com"
#         test_register_invalid_email(email)
        
#         email = "123abc!@#"
#         test_register_invalid_email(email)
        
#         email = "Hayden"
#         test_register_invalid_email(email)
        
#         email = "Everest"
#         test_register_invalid_email(email)
        
#def test_login_email_not_registered():

#def test_login_incorrect_password():   

    
#def test_register_email_used():
#    clear_v1()
#    with pytest.raises(InputError)
#        auth_register_v1('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
#        assert  


#def test_invalid_password():

       
#def test_register_invalid_first_name():
#    clear_v1()
#    auth_register_v1('validemail@gmail.com', 'abc123!@#', 'thisnamewillbeinvalidasitwillbeoverfiftycharacterslongwhichisbad', 'name_last')
#   user_id = auth_login_v1('validemail@gmail.com', 'abc123!@#')
#    with pytest.raises(InputError) as e:
#        assert(auth_register_v1(user_id, 'thisnamewillbeinvalidasitwillbeoverfiftycharacterslongwhichisbad', 'name_last', True == e))

#def test_register_invalid_first_name():
#    clear_v1()
#   auth_register_v1('validemail@gmail.com', 'abc123!@#', 'thisnamewillbeinvalidasitwillbeoverfiftycharacterslongwhichisbad', 'name_last')
#    auth_register_v1('name_first', 'name_last', 'validemail@gmail.com', 
#    if len(name_first) >= 50:
#        print(InputError)

def test_names():
    clear_v1()
    #first name is empty
    with pytest.raises(InputError):
        auth_register_v1('validemail@gmail.com', 'abc123!@#', '', 'name_last')
        
    #last name is empty
    with pytest.raises(InputError):
        auth_register_v1('validemail@gmail.com', 'abc123!@#', 'John', '')
        
    #first name is too long
    with pytest.raises(InputError):
        auth_register_v1('validemail@gmail.com', 'abc123!@#', 'thisnamewillbeinvalidasitwillbeoverfiftycharacterslongwhichisbad', 'name_last')
    
    #last name is too long
    with pytest.raises(InputError):
        auth_register_v1('validemail@gmail.com', 'abc123!@#', 'John', 'thisnamewillbeinvalidasitwillbeoverfiftycharacterslongwhichisbad')

# def test_handle_name():
#     #same handle_str
#     user_id = auth_register_v1('johnsmith@gmail.com', 'abc123!@#', 'John', 'Smith')
#     assert(users[user_id]['handle_str'] == 'johnsmith0')
#     #handle_str more than 20 characters
#     user_id = auth_register_v1('johnsmith@gmail.com', 'abc123!@#', 'John', 'Smith1234567891011')
#     assert(users[user_id]['handle_str'] == 'johnsmith1234567891011')
    
def test_password():
    clear_v1()
    #password is too short
    with pytest.raises(InputError):
        auth_register_v1('johnsmith@gmail.com', 'a', 'John', 'Smith')
        
def test_email_used():
    clear_v1()
    #password is already registered
    auth_register_v1('johnsmith@gmail.com', 'abc123!@#', 'John', 'Smith')
    with pytest.raises(InputError):
        auth_register_v1('johnsmith@gmail.com', 'password', 'Joan', 'Lane')
    
def test_incorrect_password():
    clear_v1()
    #log in with incorrect password
    auth_register_v1('elmo@sesame.street', 'abc123!@#', 'John', 'Smith')
    with pytest.raises(InputError):
        auth_login_v1('elmo@sesame.street', 'abc123!')
    
def test_email_not_registered():
    #email not registered
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('bensonchan@gmail.com', 'abc123@!3')

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def user():
    return auth_register_v1("name@example.com","password123","Smith","John")

# valid password change
def test_password_changed_valid(clear, user):
    reset_code = auth_passwordreset_request_v1("name@example.com")
    auth_passwordreset_reset_v1(reset_code,  "ILoveUNSW")
    auth_login_v1("name@example.com", "ILoveUNSW")
    # no error raised so password reset worked

# invalid code
def test_password_change_invalid_code(clear, user):
    auth_passwordreset_request_v1("name@example.com")
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1("Invalid Code My Guy",  "ILoveUNSW")

# invalid new password
def test_password_change_invalid_password(clear, user):
    reset_code = auth_passwordreset_request_v1("name@example.com")
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(reset_code,  "short")