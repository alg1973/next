#!/usr/bin/python
import time
import zmq

context = zmq.Context()
command = context.socket(zmq.REP) # Command channel
command.bind("tcp://*:5555")

temperature = context.socket(zmq.SUB) #Temperature channel
temperature.connect("tcp://*:5556")
temperature.setsockopt(zmq.SUBSCRIBE, b"10001")

# Initialize poll set
poller = zmq.Poller()
poller.register(command, zmq.POLLIN)
poller.register(temperature, zmq.POLLIN)

# Process messages from both sockets
# We prioritize traffic from the command task
while True:

    try:
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break

    if command in socks:
        msg = command.recv()
        # process task

    if temperature in socks:
        msg = temperature.recv()
        # process weather update
    
    # Process any waiting tasks
    while True:
        try:
            msg = command.recv(zmq.DONTWAIT)
        except zmq.Again:
            break
        print ("Get command Message", msg)
       

    # Process any waiting weather updates
    while True:
        try:
            msg = subscriber.recv(zmq.DONTWAIT)
        except zmq.Again:
            break
        print ("Get temperature message", msg)
        # process weather update

    # No activity, so sleep for 1 msec
    time.sleep(0.001)
   
