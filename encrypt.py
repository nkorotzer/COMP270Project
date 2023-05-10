# from Crypto.Protocol.KDF import scrypt
# from Crypto.Random import get_random_bytes

import nacl.pwhash
from nacl.public import Box
import nacl.exceptions

def get_box(pub_key, sec_key):
    return Box(sec_key, pub_key)

def encrypt_text(pub_key, sec_key, ptext):
    box = get_box(pub_key, sec_key)
    return box.encrypt(ptext)

def decrypt_text(pub_key, sec_key, ctext):
    box = get_box(pub_key, sec_key)
    return box.encrypt(ctext)

def main():
    # following example from https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html#scrypt-func
    password = input('Enter Password: ')
    # salt = get_random_bytes(16)
    # key = scrypt(password, salt, key_len=16, N=2**14, r=8, p=1)
    # print(key)

    pword = nacl.pwhash.scrypt.str(password.encode())
    print(pword)

if __name__ == "__main__":
    main()