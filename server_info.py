import nacl.utils
from nacl.public import PrivateKey, Box

server_public_key_file = 'server_public_key.txt'
server_private_key_file = 'server_private_key.txt'

def get_public_key() -> bytes:
    with open(server_public_key_file,'rb') as file:
        return file.read()

def get_private_key() -> bytes:
    with open(server_private_key_file,'rb') as file:
        return file.read()

def main():
    sec_key = PrivateKey.generate()
    pub_key = sec_key.public_key

    with open(server_private_key_file,'wb') as secfile, open(server_public_key_file,'wb') as pubfile:
        secfile.write(sec_key.encode())
        pubfile.write(pub_key.encode())

    print('Private key:\t',get_private_key())
    print('Public key:\t',get_public_key())

if __name__ == '__main__':
    main()