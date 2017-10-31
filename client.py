#!usr/bin/env python

#import curses
import socket
import sys
from timeit import default_timer as timer
from time import sleep

# set up tcp connection settings
SRV_IP = "127.0.0.1" #change this
TCP_PORT = 5005
BUFFER_SIZE = 1024
ID = "Test"

# output function
def output (data, time):
    global iter
    err = 0
    win.clear()
    
    # handle error event
    if data != -1 and time != -1:
        response = averageMachine(time)
        highest = highestRes(time)
        lowest = lowestRes(time)
        graphMachine()
        message = data.decode("UTF-8")
    else:
        err = -1
        averageMachine(err)
        graphMachine()
        message = "error"
        response = "error"
        highest = str(high)
        lowest = str(low)
    
    # write infor to cli
    win.addstr("\n")
    win.addstr("Connected to: %s\n" % SRV_IP)
    win.addstr("Message num: %s\n" % message)
    win.addstr("Response time: %s\n" % str(time))
    win.addstr("Average: %s\n" % response)
    win.addstr("Highest: %s\n" % highest)
    win.addstr("Lowest: %s\n" % lowest)
    win.addstr("Errors: %s\n" % str(errors))
    win.addstr("\n")
    win.addstr("Press ESC to stop.\n")
    win.refresh()
    
    # press escape key to stop app
    if win.getch() == 27:
        curses.endwin()
        iter = numMessages-1

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
        graph.append([" "] * len(averageTimeList))
        
    # populate 2D list with plot points for graph"
    count=0  
    for i in averageTimeList:
        temp = i * 100
        temp = int(round(temp, 1))
        
        if temp > 10:
            temp = 10
        
        if i != -1:
            graph[10-temp][count] = "*"
        else: 
           for i in range(0,11):
              graph[i][count] = "#"
        
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
            if col != "#":
                win.addstr(str(col))
            else:
                win.addstr(str(col), curses.color_pair(1))
        win.addstr("\n")
        count -= 1
        
    # finish off
    win.addstr("    ")
    for i in range(avScope+1):
        win.addstr("-")
    win.addstr("\n")

# main
def main():
    # connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SRV_IP, TCP_PORT))
    s.settimeout(2.0)

    # invoke curses
    win = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    win.nodelay(1)

    iter = 1            # init iter
    numMessages = -1 # sets how many loops to do, -1 is inifinite
    pauseTime = 0.1  # in seconds, sets rate at which client polls server

    # set scope for determining rolling average response time
    avScope = 100

    # initilise list used for calculating average response time
    averageTimeList = []

    # highest and lowest response times
    high = 0
    low = 1

    # error counts
    errors = 0

    s.send(bytes(ID, "UTF-8"))
    data = s.recv(BUFFER_SIZE)
    UDP_PORT = int(data)
    print(UDP_PORT)

    usock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

    while iter != numMessages:
        # time how long it takes to get a response after send a message to the server
    
        start = timer()
        usock.sendto(bytes(str(iter), "UTF-8"), (SRV_IP, UDP_PORT))
    
        # try to receive a response packet from server
        try:
            data = s.recv(BUFFER_SIZE)
            end = timer()
        # if no response in defined timeout, handle accordingly
        except socket.timeout:
            end = timer()
            data = b'0'

        # write output to cli
        if data.decode("UTF-8") == str(iter):
            output(data, (end - start)) 
        else:
            output(-1, -1)
            errors += 1
            iter -= 1
        
        iter += 1
        sleep(pauseTime)

    usock.sendto(bytes("CLOSE", "UTF-8"), (SRV_IP, UDP_PORT))      
    # close connection to server
    usock.close()
    s.close()

    print ("Closed connection.")

    # close curses
    curses.endwin()

if __name__ == "__main__":
    main()