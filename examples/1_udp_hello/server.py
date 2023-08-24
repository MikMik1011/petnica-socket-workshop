import socket
import sys
import threading

socket_types = {
    "TCP": socket.SOCK_STREAM,
    "UDP": socket.SOCK_DGRAM
}

def create_server_socket(ip, port):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server.bind((ip, port))
    return server

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <port>")
        sys.exit(1)

    server_port = int(sys.argv[1])
    server_ip = socket.gethostbyname(socket.gethostname())

    server = create_server_socket(server_ip, server_port)
    print(f"Listening on {server_ip}:{server_port}")

    while True:
        data, addr = server.recvfrom(1024)
        data = data.decode('utf-8')
        print(f"[{addr[0]}] {data}")
        server.sendto(f"{data} i tebi, {addr[0]}!".encode('utf-8'), addr)

if __name__ == "__main__":
    main()

