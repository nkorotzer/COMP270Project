import sys
import socket
from threading import Thread
import database
import message_types
import encrypt
import server_info

def remove_start_and_end(data):
    if data[0:5] == b'start' and data[-3:] == b'end':
        return data[5:-3]
    else:
        print('Head and tail missing from message')

def add_start_and_end(encrypted):
    # input should be encoded
    return 'start'.encode() + encrypted + 'end'.encode()

def decrypt_outer_packet(username, ctext):
    user_public_key = database.get_user_pub_key(username)
    server_private_key = server_info.get_private_key()
    return encrypt.decrypt_text(user_public_key, server_private_key, ctext)

def encrypt_outer_packet(username, ptext):
    user_public_key = database.get_user_pub_key(username)
    server_private_key = server_info.get_private_key()
    return encrypt.encrypt_text(user_public_key, server_private_key, ptext)

def parse_message_from_client(data):
    message = remove_start_and_end(data)
    print('message:\t',message)
    message_type = message[0:1]

    match message_type:
        case message_types.CHECK_USER:
            username = message[1:].decode()
            print('received username: ',username)
            if database.does_user_exist(username):
                return message_types.CHECK_USER + 'yes'.encode()
            else:
                return message_types.CHECK_USER + 'no'.encode()
            
        case message_types.CREATE_USER:
            username = message[1:17].decode()
            password = message[17:118]
            pub_key = message[118:]
            result = database.add_user(username, password, pub_key).encode()
            return message_types.CREATE_USER + result
        
        case message_types.VALIDATE_USER:
            username = message[1:17].decode()
            password = decrypt_outer_packet(username,message[17:]).decode()
            print(username, password)
            result = database.validate_user(username, password)
            encrypted = encrypt_outer_packet(username,str(result).encode())
            return message_types.VALIDATE_USER + encrypted

        case _:
            return 'Invalid message type received from client'.encode()

def client_thread(connection, address):
    BUFFER_SIZE = 1024
    with connection:
        print(f"Connected by {address}")
        data = b''
        while True:
            block = connection.recv(BUFFER_SIZE)
            data += block
            if b'end' in block:
                break
            
        return_msg = parse_message_from_client(data)
        return_msg = add_start_and_end(return_msg)
        connection.sendall(return_msg)
    print(f'Closing connection with {address}')

def listen_on_socket(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
        except:
            print("binding error, closing...")
            sys.exit()
        
        s.listen(5)
        print(f'Now listening on {host}:{port}')

        while True:
            conn, addr = s.accept()
            conn.settimeout(60)
            thr = Thread(target=client_thread, args=(conn,addr))
            thr.start()

def main():
    HOST = "127.0.0.1"
    PORT = 65432

    con, cur = database.connect_to_database(database.db_name)
    database.create_user_table(cur)


    listen_on_socket(HOST, PORT)

            

if __name__ == "__main__":
	main()