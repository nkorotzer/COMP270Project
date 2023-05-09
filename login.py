import nacl.pwhash
import client
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
    return client.message_validate_user(username, password)

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
    fileName = f'{username}.txt'
    with open(fileName,'rb') as file:
        return file.read()

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

def user_menu(username):
    orig = username.strip('_')
    print(f'Logged in, welcome {orig}!')
    print('menu TBD')

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