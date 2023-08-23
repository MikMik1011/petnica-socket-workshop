import socket
import sys
import threading
import contents
import cowsay
from PIL import Image
import deeppyer
import asyncio
import io
from tempfile import TemporaryFile

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

async def deepfry(img):
    img_stream = io.BytesIO(img)
    image = Image.open(img_stream)
    return await deeppyer.deepfry(image, flares=False)


async def handleTextMessage(conn, content):
    msg = content["content"]
    name = content["name"]
    animal = content["animal"]
    
    try:
        response = cowsay.get_output_string(animal, f"[{name}]: {msg}")
    except Exception as e:
        response = f"Error: {e}"

    print(response)
    
    response = contents.pack(response, "text", "SERVER")
    conn.sendall(response)

async def handleImageMessage(conn, content):
    img = content["content"]
    name = content["name"]
    print(f"[{name}] sent an image!")

    image = await deepfry(img)

    with TemporaryFile() as f:
        image.save(f, format="PNG")
        f.seek(0)
        img = f.read()
    
    response = contents.pack(img, "image", "SERVER")
    conn.sendall(response)
    image.show()
    

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
                                          
            content = contents.unpack(content)
        except Exception as e:
            print(f"Error: {e}")
            break

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(contentTypeHandlers[content["type"]](conn, content))

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
