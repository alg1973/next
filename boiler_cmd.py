#!/usr/bin/python

import tconf
import bstate
import sys
import dyndb


if len(sys.argv)==3:
	target=int(sys.argv[1])
	heating=int(sys.argv[2])
elif len(sys.argv)==4:
	target=int(sys.argv[1])
	heating=int(sys.argv[2])
    thermo_name=sys.argv[3]
else:
	target=100
	heating=0
    thermo_name=tconf.thermo_name


b=bstate.Boiler(thermo_name)
print b.write_state(target,heating)
print b.read_state()
