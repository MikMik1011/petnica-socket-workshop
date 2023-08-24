import socket
import threading
import sys

clients = []
unsent_messages = []

def receive(sock):
    while True:
        data, addr = sock.recvfrom(2000)
        msg = data.decode()
        print(addr, msg)
        if addr not in clients:
            clients.append(addr)

        unsent_messages.append(data)


def broadcast(sock):
    while True:
        if len(unsent_messages) > 0:
            data = unsent_messages.pop(0)
            for client in clients:
                try:
                    sock.sendto(data, client)
                except:
                    clients.remove(client)
                    unsent_messages.append(f"[SERVER] Goodbye {client}!".encode())

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <port>")
        sys.exit(1)

    SERVER_IP = socket.gethostbyname(socket.gethostname())
    SERVER_PORT = int(sys.argv[1])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")

    threading.Thread(target=receive, args=(sock, )).start()
    threading.Thread(target=broadcast, args=(sock, )).start()

if __name__ == "__main__":
    main()

