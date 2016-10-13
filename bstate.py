#!/usr/bin/python

import json
import tempfile
import tconf
import os
import errno

class Boiler:
        def __init__(self, name):
                self.boiler_name=name
                self.state= { 'target' : 100, 'heating' : 0 }
                self.state_file=tconf.state_prefix+'/' + self.boiler_name + '.state'


        def read_state(self,skip_file=False):
                if not skip_file:
                        with open(self.state_file,'r') as f:
                                self.state=json.load(f)
                return self.state

        def write_state(self,new_target=100,new_heating=0):
            self.state['target']=new_target
            self.state['heating']=new_heating
            for i in range(3):
                try:
                    with tempfile.NamedTemporaryFile(mode='w',delete=False) as f:
                        json.dump(self.state,f)
                        try:
                            os.remove(self.state_file)
                        except OSError as e:
                            # Ignore 'No such file or directory
                            if e.errno!=errno.ENOENT:
                                raise
                        os.rename(f.name,self.state_file)
                except IOError as e:
                    print "I/O error({0}): {1}".format(e.errno, e.strerror)
                except OSError as e:
                    print "OS error({0}): {1}".format(e.errno, e.strerror)
#                except:
#                    print "Unknown error writing/renaming boiler state file... retrying"
            return self.state


#b=Boiler("InsideHall")
#print b.state
#print b.read_state(skip_file=True)
#print b.write_state(25,-1)
#print b.read_state()
#print b.read_state(skip_file=True)


