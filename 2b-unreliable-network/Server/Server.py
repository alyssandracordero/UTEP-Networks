#Alyssandra M. Cordero - Reliable File Transfer using UDP (Server)
import os
import socket
import packet, udt, timer
import threading, time

# Sends file using GBN
def gbn(sock):
    WINDOW_SIZE = 8
    c = 0 #packet count
    base = 0
    #for starting a timer: time = timer.Timer(5)

    # Opening file and sending data
    with open(file_name, "rb") as file:
        for i in range(WINDOW_SIZE):
            data = file.read(1024)
            print(data)
            if not (data):
                break
            # Send files
            pack = packet.make(c, data)
            local_buff.append((pack,c))
            c += 1 # Update c
            # Loop while c isn't file_size
            while c <= file_size:
                # Set delay
                time.sleep(2)
                with lock:
                    for i in local_buff:
                        udt.send(i[0], sock, CLIENT_ADDR)
                for i in range(base):
                    data = file.read(1024)
                    if not (data):
                        break
                    # Send files
                    pack = packet.make(c, data)
                    local_buff.append(pack,c)
                    c += 1 # Update c
    with lock:
        # Send files
        pack = packet.make(c, "END".encode())
        local_buff.append(pack)
        udt.send(pack, sock, CLIENT_ADDR)

# Sends file using SR
def sr(sock, conn, file_name):
    # Opening file and sending data
    with open(file_name, "rb") as file:
        c = 0
        # Window size
        N = 4
        curr_window = 0
        threads = []

        # loop while c isn't file_size
        while c <= file_size:
            while curr_window < N:
                data = file.read(1024)

# If user does not specify, use default
def regular(sock, conn, file_name):
    # Opening file and sending data
    with open(file_name, "rb") as file:
        c = 0

        # loop while c isn't file_size
        while c <= file_size:
            data = file.read(1024)
            if not (data):
                break
            conn.sendall(data)
            c += len(data)

# Start connection
port = input("Listening at port #:")
port = int(port)
CLIENT_ADDR = ('10.0.0.21', port)
SERVER_ADDR = ('10.0.0.20',port)
file_name = 'readme.txt'
# Choose protocol GBN or SR
protocol = input("Protocol to use (GBN/SR): ")

# loop to keep accepting connections
while True:
    print("Listening for connection at :", port, "...")

    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(CLIENT_ADDR)
    # This helps accept another connection

    # Accepting the connection
    #conn, addr = sock.accept()
    print("Connection accepted from: 10.0.0.21")
    lock = threading.Lock()
    base = 0
    local_buff = []
    window = []
    # File details
    #file_name = conn.recv(1024).decode()
    file_size = len(file_name)

    # Sending file using either protocol
    if protocol == "GBN":
        gbns = threading.Thread(target=gbn(sock), args=())
        time.sleep(2)
        gbns.start()
        
    elif protocol == "SR":
        srs = threading.Thread(target=sr(sock), args=())
        srs.start()
        time.sleep(2)
        srr = threading.Thread(target=sr(sock), args=())
        srr.start()
    else:
        regular(sock, conn, file_name)

    print("Transfer Complete!")

    sock.close()
    print("Connection closed, see you later!")
