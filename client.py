#!usr/bin/env python

import curses
import socket
import sys
from timeit import default_timer as timer
from time import sleep

# set up tcp connection settings
TCP_IP = 'xxx.xxx.xxx.xxx' #change this
TCP_PORT = 5005
BUFFER_SIZE = 1024

# connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# invoke curses
win = curses.initscr()

x = 1            # init x
numMessages = 1000 # -1 is inifinite
pauseTime = 0.2   # in seconds

# set scope for determining rolling average response time
avScope = 100
averageTimeList = []

# highest and lowest response times
high = 0
low = 1

# output function
def output (data, time):
    win.clear()
    response = averageMachine(time)
    highest = highestRes(time)
    lowest = lowestRes(time)
    graphMachine() 
    win.addstr("\n")
    win.addstr("Connected to: " + TCP_IP + "\n")
    win.addstr("Message num: " + data.decode('UTF-8') + "\n")
    win.addstr("Response time: " + str(time) + "\n")
    win.addstr("Average: " + response + "\n")
    win.addstr("Highest: " + highest + "\n")
    win.addstr("Lowest: " + lowest + "\n")
    win.refresh()

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
    graph = []
    for x in range(0,11):
        graph.append([' '] * len(averageTimeList))
        
    x=0  
    for i in averageTimeList:
        temp = i * 100
        temp = int(round(temp, 1))
        graph[10-temp][x] = '*'
        x += 1
    
    x=10    
    for row in graph:
        if x == 10:
            win.addstr(str(x) + "0|")
        else:
            win.addstr(" " + str(x) + "0|")
            
        for col in row:
            win.addstr(str(col))
        win.addstr("\n")
        x -= 1    
    win.addstr("    ----------------------------------------------------------------------------------------------------\n")

# main 
while x != numMessages:
    # time how long it takes to get a response after send a message to the server
    start = timer()
    s.send(bytes(str(x), 'UTF-8'))
    data = s.recv(BUFFER_SIZE)
    end = timer()

    # write output to cli
    output(data, (end - start))
    x += 1
    sleep(pauseTime)

# close connection to server
s.close()

print ("Closed connection.")


    
