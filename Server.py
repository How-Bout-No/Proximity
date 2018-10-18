import pickle
import socket
import sys
import threading
import time

if len(sys.argv) > 1:
    ip = sys.argv[1]
    port = sys.argv[2]
    servername = sys.argv[3].replace(';', ' ')
else:
    ip = '0.0.0.0'
    port = 60501
    servername = "Anonymous Server"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip, int(port))
print("# Proximity Server v1.2.1\n")
print(f"\nHosting '{servername}' on '%s' port '%s'\n" % server_address)
try:
    sock.bind(server_address)
except OSError:
    print("\n\nError starting server!\nIs a server instance already running?")
    time.sleep(5)
    sys.exit()

clients = {}
connections = []

sock.listen(10)


def get_new(conn, addr):
    global clients
    while not conn._closed:
        data = conn.recv(256)
        try:
            pickle.loads(data)
        except:
            data = data.decode()
            print(data)
            data = data.encode('utf-8')
            for conne in connections:
                conne[0].sendall(data)
        else:
            if (conn, addr) in connections:
                connections.remove((conn, addr))
            for x in connections:
                lst = [';;', str(clients[conn[1]] + ' has left the server'),
                       '\n'.join(clients[c[1]] for c in connections),
                       servername]
                conn[0].send(pickle.dumps(lst))
            print(clients[addr] + ' has left the server')
            try:
                clients[addr]
            except:
                pass
            else:
                del clients[addr]
            conn.close()


while True:
    connection, addr = sock.accept()
    data = connection.recv(256)
    init = pickle.loads(data)
    connections.append((connection, addr))
    for conn in connections:
        clients[conn[1]] = init[1]
    for conn in connections:
        print(clients)
        lst = ['::', str(init[1] + ' has joined the server'), '\n'.join(clients[c[1]] for c in connections), servername]
        conn[0].send(pickle.dumps(lst))
        print(init[1] + ' has joined the server')
    threading.Thread(target=get_new, args=(connection, addr)).start()
