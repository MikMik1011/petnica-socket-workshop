import socket
import sys
import contents
from PIL import Image
import io

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <ip> <port>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

def receive_message(conn, length):
    msg = conn.recv(length)
    if not msg:
        raise Exception("Connection closed")
    return msg
    
def handleTextContent(content):
    msg = content["content"]
    print(msg)

def handleImageContent(content):
    img = content["content"]
    image = Image.open(io.BytesIO(img))
    image.show()

contentTypeHandlers = {
    "text": handleTextContent,
    "image": handleImageContent
}


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = input("Enter your name: ")
sock.connect((SERVER_IP, SERVER_PORT))
try:
    while True:
        contentType = input("Enter content type (text/image): ")
        content = None
        if contentType == "text":
            msg = input("Enter your message: ")
            animal = input("Enter animal: ")
            content = contents.pack(msg, "text", username, animal)

        elif contentType == "image":
            path = input("Enter image path: ")
            with open(path, "rb") as f:
                img = f.read()
            content = contents.pack(img, "image", username)

        else:
            print("Invalid content type")
            continue

        sock.sendall(content)

        try:
            msgSize = int.from_bytes(receive_message(sock, contents.HEADER_LEN))   
            content = b""
            while len(content) < msgSize:
                content += receive_message(sock, msgSize - len(content))
            content = contents.unpack(content)
        except Exception as e:
            print(f"Error: {e}")
            break
        
        contentTypeHandlers[content["type"]](content)

except KeyboardInterrupt:
    sock.close()
    exit()
