import socket

def main():
    HOST = "127.0.0.1"
    PORT = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(b"Hi Server")
        data = s.recv(1024)
        
    print(f"Received {data!r}")
	
	
if __name__ == "__main__":
	main()