import socket
import threading
import sys
import random

def create_client_chat_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_port = None
    while not client_port:
        port = random.randint(10000, 20000)
        try:
            sock.bind(("0.0.0.0", port))
            client_port = port
            print("Bound on port", client_port)
        except:
            pass
    
    return sock

def receive(sock):
    while True:
        data, addr = sock.recvfrom(2000)
        msg = data.decode('utf-8')
        print(msg)

def send(ip, port, name, sock):
    sock.sendto(f"{name} has joined the chat!".encode('utf-8'), (ip, port))
    while True:
        msg = input()
        sock.sendto(f"[{name}]: {msg}".encode('utf-8'), (ip, port))

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(1)
        
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    
    sock = create_client_chat_socket()
    name = input("Enter your name: ")

    threading.Thread(target=receive, args=(sock, )).start()
    threading.Thread(target=send, args=(server_ip, server_port, name, sock)).start()

if __name__ == "__main__":
    main()
