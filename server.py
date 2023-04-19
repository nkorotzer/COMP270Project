import socket

def main():
    HOST = "127.0.0.1"
    PORT = 65432
    s.bind((HOST, PORT))
    s.listen()
    
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

if __name__ == "__main__":
	main()