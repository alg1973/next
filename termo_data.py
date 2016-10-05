#!/usr/bin/python 

import sys
import time
import dyndb
import serio
import tconf

if len(sys.argv)==2:
        tty_name=sys.argv[1]
else:
        tty_name=tconf.tty

f=serio.Serial(tty_name)
time.sleep(3)
db=dyndb.Tempdb(tconf.url,tconf.region)
while 1:
        f.swrite("\n")
        time.sleep(0.5)
        ch=f.sread()
	values=ch.split()
	if len(values) == 3:
		db.put_values(float(values[0]),float(values[1]))
		print ("good read and write: "+ch)
	else:
		print ("read invalid data from serial: '")
		print ch
		print "'\n"
        time.sleep(5)
f.sclose()


