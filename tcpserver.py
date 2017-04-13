# All rights reserved 2017
# By Lucas Tan for Robotics and Maker Academy, Singapore Polytechnic

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import str
from future import standard_library
standard_library.install_aliases()
import threading		
import socketserver

def default_callback(ip, string):
    print(ip)
    print(string)

callback = default_callback
#returns an IP and a raw string

dict = {"127.0.0.1": "none"}

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        dict[self.client_address[0]] = self.data.decode("utf-8")
        callback(self.client_address[0], dict[self.client_address[0]])

class myThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.threadID = 5
        self.host = host
        self.port = port
        self.server = socketserver.TCPServer((self.host, self.port), MyTCPHandler)
    def run(self)	:
        print("Listening for connections on " + self.host +":" + str(self.port))
        self.server.serve_forever()
    def stopthread(self):
        print("stopping")
        self.server.shutdown()
        print("stopped")
        
    def regcallback(self, cb):
        global callback
        callback = cb

