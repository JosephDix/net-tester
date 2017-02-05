#!usr/bin/env python

import curses
import socket
import sys
from timeit import default_timer as timer
from time import sleep

# set up tcp connection settings
SRV_IP = '127.0.0.1' #change this
TCP_PORT = 5005
BUFFER_SIZE = 1024

ID = "Test"

# connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SRV_IP, TCP_PORT))

# invoke curses
win = curses.initscr()
win.nodelay(1)

x = 1            # init x
numMessages = -1 # -1 is inifinite
pauseTime = 0  # in seconds

# set scope for determining rolling average response time
avScope = 100

# initilise list used for calculating average response time
averageTimeList = []

# highest and lowest response times
high = 0
low = 1

# error counts
errors = 0

# output function
def output (data, time):
    global x
    err = 0
    win.clear()
    if data != -1 and time != -1:
        response = averageMachine(time)
        highest = highestRes(time)
        lowest = lowestRes(time)
        graphMachine()
        message = data.decode('UTF-8')
    else:
        err = -1
        averageMachine(err)
        graphMachine()
        message = 'error'
        response = 'error'
        highest = str(high)
        lowest = str(low)
    
     
    win.addstr("\n")
    win.addstr("Connected to: " + SRV_IP + "\n")
    win.addstr("Message num: " + message + "\n")
    win.addstr("Response time: " + str(time) + "\n")
    win.addstr("Average: " + response + "\n")
    win.addstr("Highest: " + highest + "\n")
    win.addstr("Lowest: " + lowest + "\n")
    win.addstr("Errors: " + str(errors) + "\n")
    win.addstr("\n")
    win.addstr("Press ESC to stop.\n")
    win.refresh()
    
    if win.getch() == 27:
        curses.endwin()
        x = numMessages-1

# get the rolling average time for a response
def averageMachine (time):
    time = float("%.6f"%time)
    
    
    if len(averageTimeList) <= avScope:
        averageTimeList.append(time)
    else:
        del averageTimeList[0]
        averageTimeList.append(time)

    #graphMachine(averageTimeList)
    
    return str(sum(averageTimeList)/len(averageTimeList))

# get highest response time
def highestRes (time):
    global high
    if time > high:
        high = time
    return str(high)

# get lowest response time
def lowestRes (time):
    global low
    if time < low:
        low = time
    return str(low)

# figure this one out
def graphMachine():
    # create 2D list type object
    graph = []
    for i in range(0,11):
        graph.append([' '] * len(averageTimeList))
        
    # populate 2D list with plot points for graph"
    count=0  
    for i in averageTimeList:
        temp = i * 100
        temp = int(round(temp, 1))
        
        if i != -1:
            graph[10-temp][count] = '*'
        else: 
           for i in range(0,11):
              graph[i][count] = '#'
        
        count += 1
    
    # generate graph cli output
    
    win.addstr("Response time in ms.\n\n")
    count=10    
    for row in graph:
        if count == 10:
            win.addstr(str(count) + "0|")
        else:
            win.addstr(" " + str(count) + "0|")
            
        for col in row:
            win.addstr(str(col))
        win.addstr("\n")
        count -= 1
        
    # finish off
    win.addstr("    ")
    for i in range(avScope):
        win.addstr("-")
    win.addstr("\n")

# main


s.send(bytes(ID, 'UTF-8'))
data = s.recv(BUFFER_SIZE)
UDP_PORT = int(data)
print(UDP_PORT)

usock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while x != numMessages:
    # time how long it takes to get a response after send a message to the server
    
    start = timer()
    usock.sendto(bytes(str(x), 'UTF-8'), (SRV_IP, UDP_PORT))
    data = s.recv(BUFFER_SIZE)
    end = timer()
    
    if data.decode('UTF-8') == str(x):
        output(data, (end - start)) 
    else:
        output(-1, -1)
        errors += 1
    
    # write output to cli
    
    x += 1
    sleep(pauseTime)

usock.sendto(bytes("CLOSE", 'UTF-8'), (SRV_IP, UDP_PORT))      
# close connection to server
usock.close()
s.close()

print ("Closed connection.")

# close curses
curses.endwin()


    
