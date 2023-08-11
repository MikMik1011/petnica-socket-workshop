import socket
import sys
import threading

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <port>")
    sys.exit(1)

def encodeHeader(message, name):
    header = str(len(message)).encode()
    header += b'\x00\x69\x00'
    header += name[:64 - len(header)].encode()
    header += b"\x00" * (64 - len(header))

    return header

def decodeHeader(header):
    data = header.split(b'\x00\x69\x00')
    msgSize = int(data[0].decode())
    name = data[1].decode().rstrip('\x00')
    return msgSize, name

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))


def handleConnection(conn, addr):
    while True:
        header = conn.recv(64)
        if not header:
            break

        msgSize, name = decodeHeader(header)
        msg = conn.recv(msgSize).decode()

        print(f"[{name}] {msg}!")

        response = f"{name} said: {msg}"
        responseHeader = encodeHeader(response, "SERVER")
        conn.send(responseHeader)
        conn.send(response.encode())

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
