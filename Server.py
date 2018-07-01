import pickle
import socket
import sys
import traceback

if len(sys.argv) > 1:
    ip = sys.argv[1]
    port = sys.argv[2]
    servername = sys.argv[3].replace(';', ' ')
else:
    ip = '0.0.0.0'
    port = 60501
    servername = "Anonymous Server"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip, int(port))
print("# Proximity Server v1.2.0\n")
print(f"\nHosting '{servername}' on '%s' port '%s'\n" % server_address)
sock.bind(server_address)

clients = []

while True:
    data, addr = sock.recvfrom(256)
    chost, cip = addr
    try:
        data = pickle.loads(data)
        try:
            if data[0] == '$inituser':
                sock.sendto(pickle.dumps(data), addr)
                clients.append([(chost, cip), data[1]])
                print(clients)
                for client in clients:
                    lst = ['::', str(data[1] + ' has joined the server'), '\n'.join(c[1] for c in clients), servername]
                    sock.sendto(pickle.dumps(lst), client[0])
                    print(data[1] + ' has joined the server')
            elif data[0] == '$cc':
                print([(chost, cip), data[1]])
                clients.remove([(chost, cip), data[1]])
                print(clients)
                for client in clients:
                    lst = [';;', str(data[1] + ' has left the server'), '\n'.join(c[1] for c in clients), servername]
                    sock.sendto(pickle.dumps(lst), client[0])
                    print(data[1] + ' has left the server')
        except:
            pass
    except:
        data = data.decode()
        print(data)
        data = data.encode('utf-8')
        for client in clients:
            try:
                sock.sendto(data, client[0])
            except:
                print(traceback.format_exc())
