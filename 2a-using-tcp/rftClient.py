"""
Assignment 2 - Reliable file transfer
Client recieves the files over the socket connection
@author Alyssandra M. Cordero
"""
import socket

SIZE = 1024

# Starting/creating TCP socket
host = input("Provide server IP: ")
port = input("Port #: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establishing connection with the socket:
try:
    sock.connect((host, int(port)))
    print("Connected Successfully")
except:
    print("Unable to connect")
    exit(0)  # End program

# Process of receiving the data
file_name = input("File Name:")
sock.send(file_name.encode())
file_name = sock.recv(SIZE).decode()
sock.send("Ack".encode())  # SEND ACK
file_size = sock.recv(SIZE).decode()

# Opening and writing to file.
with open(file_name, "wb") as file:
    c = 0
    while c <= int(file_name):
        data = sock.recv(SIZE)
        if not (data):
            break
        file.write(data)
        c += len(data)

# Closing the socket...
sock.close()