**ITERATION 1**

CHANNEL RULES:
    - When a channel is created, the user creating it automatically becomes an owner member.
    - When a new user is created, the user is not part of any channels. 
    - The user will not be able to join the channel again if they are already part of the target channel.

INPUTS:
    - The user's input will always be the correct data type.
    - Input of first_name and last_name only contain alphabets in lower-case and upper-case, hyphens and whitespaces. 
    - Conditions for correct inputs is set in functions already.

LOGISTICS:
    - The message_id, auth_user_id, channel_id starts off at 1 and increases by 1 whenever a new object is created. 
    - The u_id for each user is a positive integer.
    - Never exceeds the memory the server can take.
USERS:
    - Assume that when a user is created for the first time, they are set to be an owner
SEARCH:
    - Assume that search function is not case sensetive

     

**ITERATION 2**

message/edit/v2
- after a message is edited, the sequence of messages does not get changed in notifications
    - eg. message was indexed 5, after editting, message is still indexed 5.

dm/create/v1
- the name of the dm is a list of the user handles. we assumed that the dm name does not change after being first created, regardless of changes in members of dm
    - eg. if Dm originally has user1 and user2 and dm name is 'user1,user2', if user3 is then added to the DM, the dm name does not change.

dm/list/v1
- we assume that the dms dictionary that is returned is of the format {dm: [#list of dms]}

dm/details/v1
- we assume that the return members is a list of members' full names where their first name is appended to their last as a string.

auth/login/v2
- we assume that the user will not login again after already being logged in

standup/start/v1
- assuming that the time_finish value is a datetime object
- length > 0


