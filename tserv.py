#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import tconf
from re import match as re_match
import sys
import os
import time
import dyndb
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import graph
import boiler

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def show_therm(wserv, minutes, thermo_name):    
    db=dyndb.Tempdb(tconf.url,tconf.region)
    if minutes is None:
        minutes = 60
    if thermo_name is None:
        thermo_name=tconf.thermo_name
        
    response = db.thermo_get_minutes(minutes,thermo_name)
    wserv.wfile.write("<h1>Temperature data</h1><p><table border=1>")
    wserv.wfile.write("<th>Date</th><th>T1</th><th>T2</th><th>Target T</th><th>mode</th><th>Boiler</th>")
    cmdmap = { 2: 'Night', 1: 'Day', 0: 'Off', 3: 'Undef'}
    bmap = { 1: '+', 0: '-', 2: 'Undef' }
    for i in reversed(response['Items']):
        wserv.wfile.write("<tr><td>{0}</td><td>{1}</td> <td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>"
                          .format(time.strftime("%d.%m %H:%M:%S",time.localtime(float(i['GetDate']))),
                                  float(i.get('val1', -1)),
                                  float(i.get('val2', -1)), int(i.get('target',-1)),
                                  cmdmap.get(int(i.get('heating',-1)),3),
                                  bmap.get(int(i.get('boiler_state',-1)),2)).encode(encoding='UTF-8'))
        
        print(time.ctime(float(i['GetDate'])),'temp1',float(i.get('val1', -1)), 'temp2', float(i.get('val2', -1)),
              'target temp',int(i.get('target',-1)),'heating cmd',int(i.get('heating',-1)),
              'boiler state', int(i.get('boiler_state',-1)))
    wserv.wfile.write("</table>")


hostName = "0.0.0.0"
hostPort = 10003
serv_therm_file = tconf.state_prefix + '/therm.data'

def is_float(n):
    try:
        return float(n)
    except ValueError:
        return -255
    
def is_term(s):
    if re_match("^[0-9a-zA-Z]+$", s) is None:
        return False
    return True
    

class therm_server(BaseHTTPRequestHandler):
    def __init__(self, a, b, c):
        self.data_file = open(serv_therm_file, "a")
        self.ticks = time.time()
        self.pid = os.getpid()
        BaseHTTPRequestHandler.__init__(self, a, b, c)

    def do_GET(self):
        self.send_response(200)
        i=self.path.find('?')
        if i == -1:
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("<html><head><title>Wrong request.</title></head>".encode(encoding='UTF-8'))
            self.wfile.write("<p>Path is invalid: {0}</p>".format(self.path).encode(encoding='UTF-8'))
            self.wfile.write("</body></html>".encode(encoding='UTF-8'))
        else:
            params = dict([p.split('=') for p in self.path[i+1:].split('&')])
            print (params)
            if 'target' in params and 'mode' in params:
                boiler.set_boiler('dbw', int(params['target']), params['mode']);
                params['s'] = 1
                params['m'] = 600
            if 's' in params and 'm' in params:
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("<html><head><title>Thermo page</title></head>".encode(encoding='UTF-8'))
                self.wfile.write('<p><a="/?s=1&m=1200">Refresh</a>'.encode(encoding='UTF-8'))
                self.wfile.write('<p><form><label for="target">Target Temperature:</label>'.encode(encoding='UTF-8'))
                
                self.wfile.write('<input type=text id="target" name="target" value="10">'.encode(encoding='UTF-8'))
                self.wfile.write('&nbsp;[<input type="radio" id="nt" name="mode" value="night">'.encode(encoding='UTF-8'))
                self.wfile.write('<label for="nt">Night</label>'.encode(encoding='UTF-8'))
                self.wfile.write('<input type="radio" id="day" name="mode" value="day">'.encode(encoding='UTF-8'))
                self.wfile.write('<label for="day">Whole Day</label>]'.encode(encoding='UTF-8'))
                self.wfile.write('&nbsp;<input type="submit" value="Set"><br><hr></form>'.encode(encoding='UTF-8'))
                self.wfile.write('<p><img src="?i=1&m='.encode(encoding='UTF-8'))
                self.wfile.write(str(int(params['m'])).encode(encoding='UTF-8'))
                self.wfile.write('"><p><hr><p>'.encode(encoding='UTF-8'))
                self.wfile.write(boiler.set_boiler('read').encode(encoding='UTF-8'))
                self.wfile.write('<hr>'.encode(encoding='UTF-8'))
                show_therm(self, int(params['m']), None)
            elif 'i' in params and 'm' in params:
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.ticks =+ 1;
                fl_name = "/tmp/img_"+str(self.pid)+str(self.ticks)+".png"
                graph.do_graph(int(params['m']), fl_name)
                with open(fl_name, 'r') as file:
                    self.wfile.write(file.read())
                try:
                    os.remove(fl_name)
                except OSError as error:
                    print(error)
                    print("File path can not be removed")
            else:           
                if 't' in params and 'v' in params:
                    if is_term(params['t']):
                        self.data_file.write("{0} {1} {2}".format(time.time(), params['t'], is_float(params['v']) ))
                        self.data_file.flush()
                    else:
                        print ("thermometer param is wrong {0}".format(params['t']))
                else:
                    print ("There aren't 't' and 'v' in request")
                self.wfile.write("<html><head><title>Got request.</title></head>".encode(encoding='UTF-8'))
                self.wfile.write("<p>Path is : {0}</p>".format(self.path).encode(encoding='UTF-8'))
                self.wfile.write('<p><a="/?s=1&m=1200">Refresh</a>'.encode(encoding='UTF-8'))
                self.wfile.write("</body></html>".encode(encoding='UTF-8'))

            
t_server = HTTPServer((hostName, hostPort), therm_server)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    t_server.serve_forever()
except KeyboardInterrupt:
    pass

t_server.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
