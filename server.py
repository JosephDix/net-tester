#!/usr/bin/env python

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

UDP_IP = "0.0.0.0"
TCP_IP = '0.0.0.0'
TCP_PORT = 5005
BUFFER_SIZE = 20

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

    def __init__(self,conn,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.UDP_PORT = port
        self.tconn = conn

        self.uconn = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.uconn.bind((UDP_IP, self.UDP_PORT))

        print "[+] New server socket thread started for " + self.ip + ":" + str(self.port)

    def run(self):
        self.data = self.tconn.recv(BUFFER_SIZE)
        print "Received data from " + self.ip + ":" + str(self.port) + " - ", self.data
        self.tconn.send(str(self.UDP_PORT))  # echo

        while True:
            self.udata, self.addr = self.uconn.recvfrom(BUFFER_SIZE)
            if self.udata.decode('UTF-8') == "CLOSE": break
            #print "Recieved data from " + self.addr[0] + ":" + str(self.addr[1]) + " - " + self.udata.decode('UTF-8')
            self.tconn.send(self.udata)  # echo

        self.uconn.close()
        self.tconn.close()
        print "Connection from " + self.ip + ":" + str(self.port) + " closed."

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((TCP_IP, TCP_PORT))
threads = []

# Server listen for connection loop
while True:
    sock.listen(5)
    print "Waiting for connections on " + str(TCP_PORT)
    (conn, (ip,port)) = sock.accept()
    newthread = ClientThread(conn,ip,port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
