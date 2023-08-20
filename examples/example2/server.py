import socket
import sys
import threading

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <port>")
    sys.exit(1)

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = int(sys.argv[1])
HEADER_SIZE_BODY_LEN = 10
HEADER_SIZE_NAME_LEN = 30

def appendHeaders(message, name):
    return bytes(f"{len(message):<{HEADER_SIZE_BODY_LEN}}" + f"{name:<{HEADER_SIZE_NAME_LEN}}" + message, "utf-8")

def receiveMessage(conn, length):
    msg = conn.recv(length)
    if not msg:
        raise Exception("Connection closed")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))

def handleConnection(conn, addr):
    while True:
        try:
            msgSize = int(conn.recv(HEADER_SIZE_BODY_LEN).decode())
            name = conn.recv(HEADER_SIZE_NAME_LEN).decode().rstrip('\x00').strip()
            msg = conn.recv(msgSize).decode()
        except Exception as e:
            print(f"Error: {e}")
            break

        print(f"[{name}] {msg}!")

        response = f"{name} said: {msg}"
        response = appendHeaders(response, "SERVER")
        conn.send(response)

    conn.close()
    print(f"Closed connection from {addr}")


def acceptConnections():
    server.listen()
    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")
    while True:
        conn, addr = server.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handleConnection, args=(conn, addr)).start()


acceptConnections()
