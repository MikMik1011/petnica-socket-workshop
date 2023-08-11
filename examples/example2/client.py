import socket
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <ip> <port>")
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

SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = input("Enter your name: ")
sock.connect((SERVER_IP, SERVER_PORT))
try:
    while True:
        msg = input("Enter your message: ")
        header = encodeHeader(msg, name)
        sock.send(header)
        sock.send(msg.encode())

        header = sock.recv(64)
        if not header:
            break
        msgSize, name = decodeHeader(header)
        msg = sock.recv(msgSize)
        print(f"[{name}] {msg}")

except KeyboardInterrupt:
    sock.close()
    exit()
