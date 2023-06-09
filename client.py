import sys
import socket
import nacl.secret
import nacl.utils
from nacl.public import PrivateKey, Box
import message_types

# TODO 
#   Message encryption
#   User messaging

HOST = "127.0.0.1"
PORT = 65432

# Packet head and tail
# Outer box: encrypted with server public key
# Inner box: encrypted with recipient public key


def encrypt_message(plaintext, box):
    return box.encrypt(plaintext.encode())

def add_start_and_end(encrypted):
    # input should be encoded
    return 'start'.encode() + encrypted + 'end'.encode()

def remove_start_and_end(data):
    if data[0:5] == b'start' and data[-3:] == b'end':
        return data[5:-3]
    else:
        print('Head and tail missing from message')

def prep_message(plaintext: str, box):
    # pass in decoded plaintext, function will handle encoding, encryption, and packet forming
    return add_start_and_end(encrypted=encrypt_message(plaintext=plaintext, box=box))

def message_does_user_exist(username: str) -> bool:
    # sends packet to server to check if a user with the given username already exists
    message = message_types.CHECK_USER + username.encode()
    response = send_message_to_server(message)
    if isinstance(response,str):
        print('Invalid response received from server, closing...')
        sys.exit()
    else:
        return response

def message_create_user(username, password, pub_key):
    # sends packet to server to create a user in user table
    message = message_types.CREATE_USER + username.encode() + password + pub_key.encode()
    response = send_message_to_server(message)
    return response

def message_validate_user(username: str, password: bytes):
    # sends packet to server to validate user credentials
    message = message_types.VALIDATE_USER + username.encode() + password
    response = send_message_to_server(message)
    return response

def message_get_user_pub_key(sender: str, encrypted_target: bytes):
    # sends message to server to request a user's public key
    message = message_types.GET_PUBLIC_KEY + sender.encode() + encrypted_target
    response = send_message_to_server(message)
    return response

def message_send_message(sender: str, encrypted_data:bytes):
    # sends message to server to add message to recipient database
    message = message_types.SEND_MESSAGE + sender.encode() + encrypted_data
    response = send_message_to_server(message)
    return response

def message_read_all_messages(username: str):
    # sends message to server to request inbox for a user
    message = message_types.READ_ALL_MESSAGES + username.encode()
    response = send_message_to_server(message)
    return response

def send_message_to_server(message: bytes):
    # pass in encoded message to send to server
    # return the response from the server
    BUFFER_SIZE = 1024
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        try:
            s.connect((HOST,PORT))
        except:
            print('Error connecting, closing... (double check that server is running)')
            sys.exit()

        # print(f'Connected to {HOST}:{PORT}')

        msg = add_start_and_end(message)
        s.sendall(msg)
        
        data = b''
        while True:
            block = s.recv(BUFFER_SIZE)
            data += block
            if b'end' in block:
                break
            
        response = parse_response_from_server(data)
    return response

def parse_response_from_server(data):
    # print('parsing received message:\t', data)
    message = remove_start_and_end(data)
    message_type = message[0:1]

    match message_type:
        case message_types.CHECK_USER:
            response = message[1:].decode()
            # print('response:\t',response)
            if response == 'yes':
                return True
            else:
                return False
            
        case message_types.CREATE_USER:
            response = message[1:].decode()
            if response == 'success':
                return True
            else:
                return False
            
        case message_types.VALIDATE_USER:
            return message[1:]
        
        case message_types.GET_PUBLIC_KEY:
            return message[1:]
        
        case message_types.SEND_MESSAGE:
            return message[1:]
        
        case message_types.READ_ALL_MESSAGES:
            return message[1:]

        case _:
            return 'Invalid message type received from server'

def main():
    secretKey = PrivateKey.generate()
    publicKey = secretKey.public_key
    clientBox = Box(private_key=secretKey, public_key=publicKey)


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
            
            ret = remove_start_and_end(data)

            if not ret:
                print('Error parsing returned packet')
            else:
                print('encrypted message:\t',ret)
                print('decrypted message:\t',clientBox.decrypt(ret).decode())
                    
        sys.exit()
	
	
if __name__ == "__main__":
	main()