import nacl.pwhash
import client

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
    print(f'password \'{pword}\' length is {len(pword)}')
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
            
def login_menu():
    # get user input
    while True:
        response = input('Log in (l) or create new account (c): ')
        if response.lower() not in 'lc':
            print('Invalid option')
        else:
            break

    if response.lower() == 'l':
        # returning user
        if validate_user():
            print('menu TBD')

    elif response.lower() == 'c':
        # new user
        while True:
            username = create_username()
            orig = username.strip('_')
            print(f'user name is {username}, length is {len(username)}, removing underscores is {orig}')
            password = create_password()
            if does_user_exist(username):
                print(f'\'{username}\' is already taken')
            else:
                break
        with open(userinfo_file,'a') as file:
            file.write(username)
            file.write(' ')
            file.write(password.decode())
            file.write('\n')
    return

def main():
    while True:
        answer = input('Enter e to exit, or another key to continue: ')
        if answer.lower() == 'e':
            break
        else:
            login_menu()

if __name__ == '__main__':
    main()