import sys
import socket
from threading import Thread

def client_thread(connection, address):
    BUFFER_SIZE = 1024
    with connection:
        print(f"Connected by {address}")
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:
                break
            connection.sendall(data)
    print(f'Closing connection with {address}')

def main():
    HOST = "127.0.0.1"
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except:
            print("binding error, closing...")
            sys.exit()
        
        s.listen(5)
        print(f'Now listening on {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            conn.settimeout(60)
            thr = Thread(target=client_thread, args=(conn,addr))
            thr.start()
            

if __name__ == "__main__":
	main()