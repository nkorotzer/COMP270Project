import sys
import socket
import nacl.secret
import nacl.utils
from nacl.public import PrivateKey, Box

def encrypt_message(plaintext, box):
    return box.encrypt(plaintext.encode())

def add_start_and_end(encrypted):
     return 'start'.encode() + encrypted + 'end'.encode()

def prep_message(plaintext, box):
     return add_start_and_end(encrypted=encrypt_message(plaintext=plaintext, box=box))

def main():
    secretKey = PrivateKey.generate()
    publicKey = secretKey.public_key
    clientBox = Box(private_key=secretKey, public_key=publicKey)

    HOST = "127.0.0.1"
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        try:
            s.connect((HOST,PORT))
        except:
            print('Error connecting, closing...')
            sys.exit()

        print(f'Connected to {HOST}:{PORT}')
        while(True):
            msg = input('Write to server: ')
            if msg == "exit" or not msg:
                print('Closing connection...')
                break
            
            msg = prep_message(plaintext=msg,box=clientBox)

            s.sendall(msg)
            data = s.recv(1024)
                
            print(f"Received {data}")
            if data[0:5] == b'start' and data[-3:] == b'end':
                ret = data[5:-3]
            else:
                print('Head and tail missing from message')

            print('encrypted message:\t',ret)
            print('decrypted message:\t',clientBox.decrypt(ret).decode())
                 
        sys.exit()
	
	
if __name__ == "__main__":
	main()