#Alyssandra M. Cordero - Reliable File Transfer using UDP (Client)
import socket
import packet, udt, timer

#GBN receive functionality
def gbn_rcv(sock, size): #takes sock and size
    while True:
        # Receive packages
        try:
            pack, sender_addr = udt.recv(sock)
            ack_num, data = packet.extract(pack) # Extract the ack #

            # Send ack only if the rcv is not corrupted
            if ack_num != seq_num:
                ack = packet.make(seq_num,b'') # Send previous packet
                udt.send(ack, sock, sender_addr)
            else:
                ack = packet.make(ack_num,b'') # Send current ack
                udt.send(ack, sock, sender_addr)
                str = str + data # Get deliverable
                counter += len(data) # Increment counter
                seq_num += 1 # Increment seq_num + 1
                if counter >= size: # If file is sent, terminate.
                    break;
        except:
                    print('Time out error!!')
    return

#SR receive functionality
def sr_rcv(sock,size):
    send_buffer = []
    first_in_window = 0
    counter = 0
    while True:
        # Receive packages
        try:
            pack, sender_addr = udt.recv(sock)
            ack_num, data = packet.extract(pack) # Extract the ack #

            # Send ack only if the rcv is not corrupted
            if ack_num != seq_num:
                ack = packet.make(seq_num,b'') # Send previous packet
                udt.send(ack, sock, sender_addr)
            else:
                ack = packet.make(ack_num,b'') # Send current ack
                udt.send(ack, sock, sender_addr)
                str = str + data # Get deliverable
                counter += len(data) # Increment counter
                seq_num += 1 # Increment seq_num + 1
                if counter >= size: # If file is sent, terminate.
                    break;
        except:
                    print('Time out error!!')
    return

# Asking
host = input("Provided Server IP: ")
port = input("Provided Port #: ")
port = int(port)
protocol = input("Protocol to use (GBN/SR): ") # Choose protocol GBN or SR

# Sending file details
file_name = input("Asking for file: ")

# Define necessary variables
CLIENT_ADDR = (host, port) # For socket
str = ''
seq_num = 0 # For gbn receive
counter = 0

# Define sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('10.0.0.20', port))

print('waiting for file...')
if protocol == "GBN":
    gbn_rcv(sock, len(file_name))
elif protocol == "SR":
    sr_rcv(sock, len(file_name))
else:
    print('Protocol must be either GBN/SR.')
    exit()
# Finishing up
print("Received", file_name)
#sock.shutdown(socket.SHUT_RDWR)
sock.close()
print("Connection closed")
