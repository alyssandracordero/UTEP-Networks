"""
Assignment 2 - Reliable file transfer
Server sends the file over the socket connection
@author Alyssandra M. Cordero
"""
import os
import socket

SIZE = 1024

# Starting/creating TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = input('Listening at port #:')
port = int(port)
sock.bind(('10.0.0.21', port))
sock.listen(5)

# Accept the connection from the client.
client, addr = sock.accept()

# Getting the file details for client.
file_name = client.recv(SIZE).decode()
file_size = os.path.getsize(file_name)

# Send file details
client.send(file_name.encode())
client.recv(SIZE).decode()
client.send(str(file_size).encode())

# Open - decompose  and send the file
# File you recieve
with open(file_name, "rb") as file:
    c = 0
    while c <= file_size:
        data = file.read(SIZE)
        if not (data):
            break
        client.sendall(data)
        c += len(data)

print("Transfered Successfully!")
# Closing the socket...
sock.close()