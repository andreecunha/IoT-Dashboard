# TCP client

import sys
import socket

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Waiting for connection response')


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host server> <port>")
    sys.exit(1)

host, port = sys.argv[1:3]

try:
    ClientSocket.connect((host, int(port)))
except socket.error as e:
    print(str(e))
res = ClientSocket.recv(1024)
while True:
    Input = input('Input: ')
    if Input=="exit":
        break
    ClientSocket.send(str.encode(Input))
    res = ClientSocket.recv(1024)
    print(res.decode('utf-8'))
ClientSocket.close()
