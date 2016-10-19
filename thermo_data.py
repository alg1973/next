#!/usr/bin/python 

import sys
import time
import dyndb
import serio
import tconf
import bstate
import json
import zmq

if len(sys.argv)==3:
        tty_name=sys.argv[1]
        thermo_name=sys.argv[2]
else:
        tty_name=tconf.tty
        thermo_name=tconf.thermo_name

#read boiler state file        
boiler = bstate.Boiler(thermo_name)  

# Init serial
tty=serio.Serial(tty_name)
time.sleep(3)
# Connect to Dynamodb
db=dyndb.Tempdb(tconf.url,tconf.region)


#init zmq pub channel
context = zmq.Context()
pub_channel  = context.socket(zmq.PUB)
pub_channel.bind("tcp://*:5555")

while True:
        tty.swrite("\n")
        time.sleep(0.5)
        boiler.read_state()
        values=tty.sread().split()
        if len(values) == 3:
                print time.time(),values[0],values[1],boiler.state['target'],boiler.state['heating']
                db.put_values(values[0],values[1],thermo_name,boiler.state['target'],
                        boiler.state['heating'])
                pub_channel.send_string(json.dump({'thermometer':thermo_name, 'temeprature':values[0],
                                                           'humidity':values[1]} ))
        else:
                print ("ERR read invalid data from serial: '")
                print values
        time.sleep(tconf.therm_rate)
tty.sclose()


