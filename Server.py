import queue
import socket
import sys
import threading
import time

ip = sys.argv[1]
port = sys.argv[2]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, int(port))
print("# Proximity Server v1.0.0\n")
print("\nHosting server on '%s' port '%s'\n" % server_address)
sock.bind(server_address)

clients = []

while True:
    data, addr = sock.recvfrom(512)
    chost, cip = addr
    data = data.decode()
    print(data)
    if (data[0:2] == '<i') and (data[-2:] == 'p>'):
        chost = data[2:-2]
        clients.append((chost, cip))
        print(clients)
    elif (data[0:2] == '<c') and (data[-2:] == 'c>'):
        chost = data[2:-2]
        clients.remove((chost, cip))
        print(clients)
    else:
        data = data.encode('utf-8')
        for client in clients:
            sock.sendto(data, client)
