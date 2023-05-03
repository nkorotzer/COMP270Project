import nacl.pwhash

userinfo_file = 'userinfo.txt'

def create_username():
    while True:
        username = input('Enter username (8-16 characters): ')
        if len(username) < 8:
            print(f'{username} is too short, extend to at least 8 characters')
        elif len(username) > 16:
            print(f'{username} is too long, please shorten to at most 16 characters')
        else:
            return username
        
def create_password():
    password = input('Enter Password: ')
    pword = nacl.pwhash.scrypt.str(password.encode())
    return pword

def validate_user():
    while True:
        username = input('Enter username: ')
        password = input('Enter password: ')
        pword = nacl.pwhash.scrypt.str(password.encode())
        
        with open(userinfo_file,'r') as file:
            print(file.readlines)
            for line in file.readlines():
                info = line.split()
                if info[0] != username:
                    continue
                else:
                    if info[1] == pword:
                        return True



def main():
    while True:
        response = input('Log in (l) or create new account (c): ')
        if response.lower() not in 'lc':
            print('Invalid option')
        else:
            break

    if response.lower() == 'l':
        # returning user
        if validate_user():
            print('Logged in')

    elif response.lower() == 'c':
        # new user
        username = create_username()
        password = create_password()
        with open(userinfo_file,'w') as file:
            file.write(username)
            file.write(' ')
            file.write(password.decode())
            file.write('\n')


if __name__ == '__main__':
    main()