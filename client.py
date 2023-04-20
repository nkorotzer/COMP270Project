import sys
import socket

def main():
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
            
            s.sendall(msg.encode())
            data = s.recv(1024)
                
            print(f"Received {data.decode()}")
        sys.exit()
	
	
if __name__ == "__main__":
	main()