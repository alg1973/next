#!/usr/bin/python

import tconf
import bstate
import sys
import dyndb


thermo_name=tconf.thermo_name
if len(sys.argv)>2:
	target=int(sys.argv[1])
	heating=int(sys.argv[2])
	if len(sys.argv)>3:
        	thermo_name=sys.argv[3]
else:
	target=100
	heating=0


b=bstate.Boiler(thermo_name)
db=dyndb.Tempdb(tconf.url,tconf.region)
response=db.thermo_cmd(target,heating,b.boiler_name,thermo_name)
print response
print b.write_state(target,heating)
print b.read_state()
