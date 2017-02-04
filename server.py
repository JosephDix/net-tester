#!/usr/bin/env python

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

    def __init__(self,conn,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.cconn = conn
        print "[+] New server socket thread started for " + self.ip + ":" + str(self.port)

    def run(self):
        while True :
            self.data = self.cconn.recv(BUFFER_SIZE)
            if not self.data: break
            print "Received data from " + self.ip + ":" + str(self.port) + " :", self.data
            self.cconn.send(self.data)  # echo
        self.cconn.close()
        print "Connection from " + self.ip + ":" + str(self.port) + " closed."

TCP_IP = '0.0.0.0'
TCP_PORT = 5005
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    s.listen(5)
    print ("Waiting for connections on " + str(TCP_PORT))
    (conn, (ip,port)) = s.accept()
    newthread = ClientThread(conn,ip,port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
