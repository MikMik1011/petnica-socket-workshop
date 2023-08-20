import socket
import sys
import contents
from PIL import Image

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <ip> <port>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

def receiveMessage(conn, length):
    msg = conn.recv(length)
    if not msg:
        raise Exception("Connection closed")
    return msg
    
def handleTextMessage(content):
    msg = content["content"]
    name = content["name"]
    print(f"[{name}] {msg}!")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = input("Enter your name: ")
sock.connect((SERVER_IP, SERVER_PORT))
try:
    while True:
        contentType = input("Enter content type (text/image): ")
        content = None
        if contentType == "text":
            msg = input("Enter your message: ")
            content = contents.pack(msg, "text", username)

        elif contentType == "image":
            path = input("Enter image path: ")
            with open(path, "rb") as f:
                img = f.read()
            content = contents.pack(img, "image", username)

        else:
            print("Invalid content type")
            continue

        sock.send(content)

        try:
            msgSize = int(receiveMessage(sock, contents.HEADER_SIZE_BODY_LEN).decode())   
            content = receiveMessage(sock, msgSize)
            content = contents.unpack(content)
        except Exception as e:
            print(f"Error: {e}")
            break
        
        handleTextMessage(content)

except KeyboardInterrupt:
    sock.close()
    exit()
