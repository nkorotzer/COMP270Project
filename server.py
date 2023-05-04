import sys
import socket
from threading import Thread
import database
import message_types

# TODO flesh out parse_message function to include other message types
#   add integration with database.py to check for usernames
#   add proper packet structure when sending messages back to client

def remove_start_and_end(data):
    if data[0:5] == b'start' and data[-3:] == b'end':
        return data[5:-3]
    else:
        print('Head and tail missing from message')

def parse_message(data):
    message = remove_start_and_end(data)

    if message[0:1] == message_types.CHECK_USER:
        print('success!')
        return 'success!'
    else:
        print(message[0])
        print(message[0:1])
    return 'bummer'

def client_thread(connection, address):
    BUFFER_SIZE = 1024
    with connection:
        print(f"Connected by {address}")
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                break

            return_msg = parse_message(data)
            connection.sendall(return_msg.encode())
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