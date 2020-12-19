#!/usr/bin/python

import requests
import time
import os
import sys

if len(sys.argv)>0:
    os.chdir(os.path.dirname(sys.argv[0]))

try:
    r = requests.get("http://192.168.8.250/")
except:
    print ("IO error connecting to term server")
    sys.exit(1)

if r.status_code != 200:
    print ("the http status is not 200 '{0}'".format(r.status_code))
    sys.exit(1)

lines = r.text.splitlines()
if len(lines) < 1:
    print ("got empty text")
    sys.exit(1)

while len(lines)>0 and not lines[0]:
    lines.pop(0)

data = lines[0].split()
if len(data)<1:
    data.append( -127 )
with open("./term.log", "a") as wlog:
    wlog.write("{0} {1}\n".format(int(time.time()), float(data[0])))

with open("./term.last","w") as termstamp:
    termstamp.write("{0} {1}".format(int(time.time()), float(data[0])))

print ("{0} {1}".format(int(time.time()), float(data[0])))

