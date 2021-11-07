#!/usr/bin/python
from __future__ import print_function

import tconf
import bstate
import sys
import dyndb
import time

def usage():
    	print ("usage: boiler <cmd> [<target_temperature> <heating> [<thermo_name>]]",file=sys.stderr)
	print ("              <cmd> - sync, loop, local, dbw, read",file=sys.stderr)
        print ("              <heating> - 'night': maintain target at night only",file=sys.stderr)
        print ("                          'day': maintain target all day long",file=sys.stderr)
        print ("                          'stop': bolier is off",file=sys.stderr)


def db2local(b, db):
    response=db.get_cmd(b.boiler_name,b.boiler_name)
    if response.has_key('Item'):
    	i=response['Item']
    	if b.state['target']!=float(i.get('target',-1)) or  b.state['heating']!=int(i.get('heating',-1)):
            print (b.write_state(float(i.get('target',-1)),int(i.get('heating',-1))))
    else:
        print ("No boiler '{0}' state change in cloud".format(b.boiler_name),file=sys.stderr)
	sys.exit(1)
    return b.state
	
cmdmap = { 'night' : 2, 'day': 1, 'stop': 0}

def set_boiler(cmd, target=None, heating_s=None, thermo_name=None):
        if thermo_name is None:
                thermo_name=tconf.thermo_name
        b=bstate.Boiler(thermo_name) #Assume thermo_name always equal to boiler_name
        db=dyndb.Tempdb(tconf.url,tconf.region)
        heating = cmdmap.get(heating_s, -1)
        ret_s = ''
        
        if cmd=='sync': #update local state from db
                db2local(b,db)
        elif cmd=='loop': #sync local state from db in loop
                while 1:
                        db2local(b,db)
	                sys.sleep(tconf.therm_rate*1.5)
        elif cmd=='local': #write values to local state file only
                print (b.write_state(target,heating))
        elif cmd=='dbw': #write values to db and locally
                response=db.thermo_cmd(target,heating,b.boiler_name,b.boiler_name)
                print (b.write_state(target,heating))
        elif cmd=='read':
                print ('Local file: ', b.read_state())
                print ('Boiler: ', b.boiler_name )
                response=db.get_cmd(b.boiler_name,b.boiler_name)
                if response.has_key('Item'):
    	                i=response['Item']	
    	                ret_s = "Remote command: target: '{1}', is heating: '{2}', updated at '{0}'".format(
			        time.ctime(float(i['utime'])),float(i.get('target',-1)),
                	        int(i.get('heating',-1)))
                        print (ret_s)
                else:
                        ret_s = "No boiler '{0}' targets in cloud".format(b.boiler_name)
                        print (ret_s, file=sys.stderr)
        else:
                print ('Unknown command: ', cmd,file=sys.stderr)
                raise Exception('Unknown command')
        return ret_s


if __name__ == "__main__":
        if len(sys.argv)<2:
                usage();
	        sys.exit(1)
        
	cmd=sys.argv[1]
        thermo_name = None
        if len(sys.argv)>3:
	        target=int(sys.argv[2])
                heating = sys.argv[3]
                if heating not in cmdmap.keys():
                        usage()
                        sys.exit(1);
                
	elif len(sys.argv)>4:
        	thermo_name=sys.argv[4]
        else:
                target=10
	        heating=0
	        print ('Using default values: target=',target,', heating=',heating)
        set_boiler(cmd, target, heating, thermo_name)

	


