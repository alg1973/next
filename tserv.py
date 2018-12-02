#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import tconf
from re import match as re_match

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
        BaseHTTPRequestHandler.__init__(self, a, b, c)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        i=self.path.find('?')
        if i == -1: 
            self.wfile.write("<html><head><title>Wrong request.</title></head>".encode(encoding='UTF-8'))
            self.wfile.write("<p>Path is invalid: {0}</p>".format(self.path).encode(encoding='UTF-8'))
            self.wfile.write("</body></html>".encode(encoding='UTF-8'))
        else:
            params = dict([p.split('=') for p in self.path[i+1:].split('&')])
            print (params)
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
            self.wfile.write("</body></html>".encode(encoding='UTF-8'))

            
t_server = HTTPServer((hostName, hostPort), therm_server)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    t_server.serve_forever()
except KeyboardInterrupt:
    pass

t_server.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
