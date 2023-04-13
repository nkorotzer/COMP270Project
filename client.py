import socket

def main():
    HOST = "127.0.0.1"
    PORT = 65432
    
    while(True):
        msg = input('Write to server: ')
        if msg == "exit":
             break
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST,PORT))
            s.sendall(msg.encode())
            data = s.recv(1024)
            
        
        print(f"Received {data.decode()}")
	
	
if __name__ == "__main__":
	main()