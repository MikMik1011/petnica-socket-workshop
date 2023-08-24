import socket
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <ip> <port>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.connect((SERVER_IP, SERVER_PORT))
sock.send(b"Hello world")

data, addr = sock.recvfrom(1024)
print(f"[SERVER] {data.decode()}")

sock.close()
