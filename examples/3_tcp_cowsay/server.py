import socket
import sys
import threading
import headers
import cowsay

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <port>")
    sys.exit(1)

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = int(sys.argv[1])

def receiveMessage(conn, length):
    msg = conn.recv(length)
    if not msg:
        raise Exception("Connection closed")
    return msg

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_IP, SERVER_PORT))

def handleConnection(conn, addr):
    while True:
        try:
            msgSize = int.from_bytes(receiveMessage(conn, headers.HEADER_LEN))
            content = b""
            while len(content) < msgSize:
                content += receiveMessage(conn, msgSize - len(content))
                                          
            content = content.decode('utf-8')
        except Exception as e:
            print(f"Error: {e}")
            break

        response = cowsay.get_output_string("cow", content)
        print(response)
        response = headers.appendHeaders(response)
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
