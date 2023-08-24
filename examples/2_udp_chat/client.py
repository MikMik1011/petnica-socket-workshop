import socket
import threading
import sys
import random

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_port = None
while not client_port:
    port = random.randint(10000, 20000)
    try:
        sock.bind((server_ip, port))
        client_port = port
    except:
        pass

name = input("Enter your name: ")

def receive():
    while True:
        data, addr = sock.recvfrom(2000)
        msg = data.decode()
        print(msg)

def send():
    while True:
        msg = input()
        sock.sendto(f"[{name}]: {msg}".encode(), (server_ip, server_port))

threading.Thread(target=receive).start()
threading.Thread(target=send).start()