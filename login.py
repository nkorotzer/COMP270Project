import nacl.pwhash
import client
import server_info
import encrypt
from nacl.public import PrivateKey

userinfo_file = 'userinfo.txt'
USERNAME_LENGTH = 16

def create_username():
    while True:
        username = input('Enter username (8-16 characters): ')
        if len(username) < 8:
            print(f'{username} is too short, extend to at least 8 characters')
        elif len(username) > 16:
            print(f'{username} is too long, please shorten to at most 16 characters')
        elif '_' in username:
            print('\'_\' character is not allowed in usernames')
        else:
            return username.ljust(USERNAME_LENGTH,'_')
        
def create_password():
    # returns 101-byte long password
    password = input('Enter Password: ')
    pword = nacl.pwhash.scrypt.str(password.encode())
    return pword

def does_user_exist(username):
    return client.message_does_user_exist(username)
    
def check_password(username, password):
    user_sec_key = get_user_private_key(username)
    server_pub_key = get_server_public_key()
    encrypted = encrypt.encrypt_text(server_pub_key,user_sec_key,password.encode())
    response = client.message_validate_user(username, encrypted)
    result = encrypt.decrypt_text(server_pub_key,user_sec_key,response).decode()
    if result == "True":
        return True
    else:
        return False

def validate_user():
    # check user's username and password
    username = input('Enter username: ')
    password = input('Enter password: ')
    
    username = username.ljust(USERNAME_LENGTH,'_')

    if does_user_exist(username):
        if check_password(username, password):
            
            return True, username
        else:
            print('Password incorrect')
            return False, ''
    else:
        print(f'User with username \'{username}\' does not exist')
        return False, ''

def store_private_key(username, sec_key):
    fileName = f'{username}.txt'
    with open(fileName,'wb') as file:
        file.write(sec_key.encode())

def get_user_private_key(username):
    # returns the private key bytes
    orig = username.strip('_')
    fileName = f'{orig}.txt'
    with open(fileName,'rb') as file:
        return file.read()

def get_server_public_key():
    # returns the public key bytes
    return server_info.get_public_key()

def create_user():
    # loop until a valid username is entered
    while True:
        username = create_username()
        orig = username.strip('_')
        if does_user_exist(username):
            print(f'Username \'{orig}\' is already taken')
        else:
            break
        
    password = create_password()

    sec_key = PrivateKey.generate()
    pub_key = sec_key.public_key
    store_private_key(orig, sec_key)

    client.message_create_user(username, password, pub_key)

def get_user_menu_choice():
    valid_choices = 'sre'
    while True:
        response = input('Send message (s), read inbox (r), or exit (e): ')
        if response.lower() not in valid_choices:
            print('Invalid option')
        else:
            return response.lower()

def user_menu(username):
    orig = username.strip('_')
    print(f'Logged in, welcome {orig}!')

    while True:
        # get user input
        choice = get_user_menu_choice()

        match choice:
            case 's':
                print('Sending TBD')
                return
            case 'r':
                print('Reading TBD')
                return
            case 'e':
                print('Logging out...')
                return
            case _:
                print('Invalid menu choice, logging out')
                return

def get_login_menu_choice():
    valid_choices = 'lce'
    while True:
        response = input('Log in (l), create new account (c), or exit (e): ')
        if response.lower() not in valid_choices:
            print('Invalid option')
        else:
            return response.lower()

def login_menu():
    while True:
        # get user input
        choice = get_login_menu_choice()

        match choice:
            case 'l':
                # returning user
                validated, username = validate_user()
                if validated:
                    user_menu(username)
                else:
                    print('Login failed')

            case 'c':
                # new user
                create_user()

            case 'e':
                # exit program
                print('Closing program...')
                return
            case _:
                print('Invalid menu option, closing...')
                return

def main():
    login_menu()

if __name__ == '__main__':
    main()