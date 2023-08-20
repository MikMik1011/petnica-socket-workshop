import socket
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <ip> <port>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
HEADER_SIZE_BODY_LEN = 10
HEADER_SIZE_NAME_LEN = 30

def appendHeaders(message, name):
    return bytes(f"{len(message):<{HEADER_SIZE_BODY_LEN}}" + f"{name[:HEADER_SIZE_NAME_LEN].ljust(HEADER_SIZE_NAME_LEN)}" + message, "utf-8")

def receiveMessage(conn, length):
    msg = conn.recv(length)
    if not msg:
        raise Exception("Connection closed")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = input("Enter your name: ")
sock.connect((SERVER_IP, SERVER_PORT))
try:
    while True:
        msg = input("Enter your message: ")
        msg = appendHeaders(msg, username)
        sock.send(msg)

        try:
            msgSize = int(sock.recv(HEADER_SIZE_BODY_LEN).decode())
            name = sock.recv(HEADER_SIZE_NAME_LEN).decode().rstrip('\x00').strip()
            msg = sock.recv(msgSize).decode()
        except Exception as e:
            print(f"Error: {e}")
            break

        print(f"[{name}] {msg}!")

except KeyboardInterrupt:
    sock.close()
    exit()
