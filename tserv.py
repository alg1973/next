#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = ""
hostPort = 10000

class therm_server(BaseHTTPRequestHandler):
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
