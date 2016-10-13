#!/usr/bin/python 

import sys
import time
import dyndb
import serio
import tconf
import bstate

if len(sys.argv)==3:
        tty_name=sys.argv[1]
        thermo_name=sys.argv[2]
else:
        tty_name=tconf.tty
        thermo_name=tconf.thermo_name

boiler = bstate.Boiler(thermo_name)  


f=serio.Serial(tty_name)
time.sleep(3)
db=dyndb.Tempdb(tconf.url,tconf.region)
while 1:
        f.swrite("\n")
        time.sleep(0.5)
        boiler.read_state()
        values=f.sread().split()
        if len(values) == 3:
                print time.time(),values[0],values[1],boiler.state['target'],boiler.state['heating']
                db.put_values(values[0],values[1],thermo_name,boiler.state['target'],
                        boiler.state['heating'])
        else:
                print ("ERR read invalid data from serial: '")
                print values
        time.sleep(tconf.therm_rate)
f.sclose()


