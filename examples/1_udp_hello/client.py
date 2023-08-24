import socket
import sys

socketTypes = {
    "TCP": socket.SOCK_STREAM,
    "UDP": socket.SOCK_DGRAM
}

def create_client_socket(ip, port, type="TCP"):
    client = socket.socket(socket.AF_INET, socketTypes[type])
    client.connect((ip, port))
    return client

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <ip> <port>")
        sys.exit(1)

    SERVER_IP = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])

    sock = create_client_socket(SERVER_IP, SERVER_PORT, "UDP")
    sock.send(b"Hello world")

    data, addr = sock.recvfrom(1024)
    print(f"[SERVER] {data.decode()}")

    sock.close()

if __name__ == "__main__":
    main()
