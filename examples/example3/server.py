import socket
import sys
import threading
import contents
from PIL import Image
import io

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
server.bind((SERVER_IP, SERVER_PORT))

def handleTextMessage(conn, content):
    msg = content["content"]
    name = content["name"]
    print(f"[{name}] {msg}!")

    response = f"{name} said: {msg}"
    response = contents.pack(response, "text", "SERVER")
    conn.sendall(response)

def handleImageMessage(conn, content):
    img = content["content"]
    name = content["name"]
    print(f"[{name}] sent an image!")

    response = f"{name} sent an image!"
    response = contents.pack(response, "text", "SERVER")
    conn.sendall(response)

    img_stream = io.BytesIO(img)
    image = Image.open(img_stream)
    image.show(title=f"{name}'s image")

contentTypeHandlers = {
    "text": handleTextMessage,
    "image": handleImageMessage
}

def handleConnection(conn, addr):
    while True:
        try:
            msgSize = int(receiveMessage(conn, contents.HEADER_SIZE_BODY_LEN).decode())
            content = b""
            while len(content) < msgSize:
                content += receiveMessage(conn, msgSize - len(content))
                                          
            print(len(content))
            content = contents.unpack(content)
        except Exception as e:
            print(f"Error: {e}")
            break
        
        contentTypeHandlers[content["type"]](conn, content)

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
