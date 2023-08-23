import socket
import sys
import headers

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = input("Enter your name: ")
sock.connect((SERVER_IP, SERVER_PORT))
try:
    while True:
        msg = input("Enter your message: ")
        msg = headers.appendHeaders(msg, username)
        sock.send(msg)

        try:
            msgSize = int.from_bytes(receiveMessage(sock, headers.HEADER_LEN))
            name = receiveMessage(sock, headers.NAME_LEN).decode().rstrip('\x00').strip()
            msg = b''
            while len(msg) < msgSize:
                msg += receiveMessage(sock, msgSize - len(msg))
            msg = msg.decode()

        except Exception as e:
            print(f"Error: {e}")
            break

        print(msg)

except KeyboardInterrupt:
    sock.close()
    exit()
