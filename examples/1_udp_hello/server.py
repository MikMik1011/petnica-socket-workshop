import socket
import sys
import threading

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <port>")
    sys.exit(1)

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_IP, SERVER_PORT))
print(f"Listening on {SERVER_IP}:{SERVER_PORT}")


while True:
    data, addr = server.recvfrom(1024)
    data = data.decode()
    print(f"[{addr[0]}] {data}")
    server.sendto(f"{data} i tebi, {addr[0]}!".encode(), addr)

