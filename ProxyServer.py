"""
Assignment 1 - Python-based socket program that implements a simple Web Proxy.
@author Alyssandra M. Cordero
"""
from socket import *
import sys

#Main
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
    
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024)
    print(message)
    
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")                      
        buffer = f.readlines()                        
        fileExist = "true"
        
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")            
        tcpCliSock.send("Content-Type:text/html\r\n")
        tcpCliSock.send(statusMessage.encode())             
        outputdata = ""
        while buffer:
            outputdata = outputdata + buffer
        buffer = f.readline()
        print(outputdata)
        tcpCliSock.send(outputdata.encode())    
    
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            print("Requested web page DNE in cache:", filetouse)
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)            
            hostn = filename.replace("www.","",1)         
            print(hostn)                                   
            try:
                c.connect((hostn, 80))# Connection to port 80
                # Ask port for the file
                fileobj = c.makefile('r', 0)               
                fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")  
                responseBuffer = fileobj.readlines()
                # Give the response to the client socket
                tmpFile = open("./" + filename,"wb")# Create new file
                for line in responseBuffer:                                                     
                    tmpFile.write(line);                                               
                    tcpCliSock.send(line);
            except:
                print("Illegal request")                                               
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n")                             
            tcpCliSock.send("Content-Type:text/html\r\n")
            tcpCliSock.send("\r\n")
    # Close the client and the server sockets    
    tcpCliSock.close() 
tcpSerSock.close()