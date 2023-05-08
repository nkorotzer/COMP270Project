import nacl.pwhash
import client
from nacl.public import PrivateKey

# TODO convert code to interact with server instead of local files
#   


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
    password = input('Enter Password: ')
    pword = nacl.pwhash.scrypt.str(password.encode())
    # print(f'password \'{pword}\' length is {len(pword)}')
    return pword

def does_user_exist(username):
    # with open(userinfo_file,'r') as file:
    #     for line in file.readlines():
    #         file_username = line.split()[0]
    #         if username == file_username:
    #             return True
    #     print('Username not found')
    #     return False
    return client.message_does_user_exist(username)
    
def check_password(password, username):
    with open(userinfo_file,'r') as file:
        for line in file.readlines():
            file_username = line.split()[0]
            file_password = line.split()[1]
            if username == file_username:
                try:
                    nacl.pwhash.scrypt.verify(file_password.encode(), password.encode())
                except:
                    print(f'Password for {username} incorrect')
                    return False
                return True
        print('Username not Found (while checking password)')
        return False

def validate_user():
    # check user's username and password
    while True:
        username = input('Enter username: ')
        password = input('Enter password: ')
        # pword = nacl.pwhash.scrypt.str(password.encode())
        
        if does_user_exist(username):
            if check_password(password, username):
                print(f'Logged in, welcome {username}!')
                return True
            else:
                print('Password incorrect')
                return False
        else:
            print(f'User with username \'{username}\' does not exist')
            return False

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
                if validate_user():
                    print('menu TBD')
                else:
                    print('Login failed')

            case 'c':
                # new user
                create_user()

                # with open(userinfo_file,'a') as file:
                #     file.write(username)
                #     file.write(' ')
                #     file.write(password.decode())
                #     file.write('\n')

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