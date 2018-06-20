import queue
import socket
import sys
import threading
import time
import traceback
from datetime import datetime
import pickle

ip = sys.argv[1]
port = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip, int(port))
print("# Proximity Server v1.1.0\n")
print("\nHosting server on '%s' port '%s'\n" % server_address)
sock.bind(server_address)

clients = []

while True:
    data, addr = sock.recvfrom(256)
    chost, cip = addr
    try:
        data = pickle.loads(data)
        if data[0] == '$inituser':
            sock.sendto(pickle.dumps(data), addr)
            clients.append((chost, cip))
            print(clients)
            for client in clients:
                lst = ['::', str(data[1] + ' has joined the server')]
                sock.sendto(pickle.dumps(lst), client)
                print(data[1] + ' has joined the server')
        elif data[0] == '$cc':
            clients.remove((chost, cip))
            print(clients)
            for client in clients:
                lst = [';;', str(data[1] + ' has left the server')]
                sock.sendto(pickle.dumps(lst), client)
                print(data[1] + ' has joined the server')
    except:
        data = data.decode()
        print(data)
        data = data.encode('utf-8')
        for client in clients:
            try:
                sock.sendto(data, client)
            except:
                print(traceback.format_exc())
