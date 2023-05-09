import sys
import socket
from threading import Thread
import database
import message_types

# TODO flesh out parse_message function to include other message types
#   add integration with database.py to check for usernames

def remove_start_and_end(data):
    if data[0:5] == b'start' and data[-3:] == b'end':
        return data[5:-3]
    else:
        print('Head and tail missing from message')

def add_start_and_end(encrypted):
    # input should be encoded
    return 'start'.encode() + encrypted + 'end'.encode()

def parse_message_from_client(data):
    message = remove_start_and_end(data)
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
            password = message[17:].decode()
            print(username, password)
            result = database.validate_user(username, password)
            return message_types.VALIDATE_USER + str(result).encode()

        case _:
            return 'Invalid message type received from client'.encode()

def client_thread(connection, address):
    BUFFER_SIZE = 1024
    with connection:
        print(f"Connected by {address}")
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
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