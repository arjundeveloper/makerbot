# All rights reserved 2017
# By Lucas Tan for Robotics and Maker Academy, Singapore Polytechnic

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import bytes
from future import standard_library
standard_library.install_aliases()
from builtins import object
import socket
import sys
import py_compile
import multiprocessing
import threading
import sys
import megapi
from time import sleep
from tcpserver import myThread

HOST, PORT = "0.0.0.0", 5555
CONNECT = "127.0.0.1"
HEADER = "def run(lf, x, y, z, dist, motor)"
lf = "00"
ds = 0

class Motor(object):
    def __init__(self, megapi):
        self.bot = megapi
        print(self.bot)
    
    def turn_right(self, speed):
        self.bot.motorRun(megapi.M1, speed)
        self.bot.motorRun(megapi.M2, 0)

    def turn_left(self, speed):
        self.bot.motorRun(megapi.M1, 0)
        self.bot.motorRun(megapi.M2, speed)

    def forward(self, speed):
        self.bot.motorRun(megapi.M1, speed)
        self.bot.motorRun(megapi.M2, speed)

    def m1(self, speed):
        self.bot.motorRun(megapi.M1, speed)

    def m2(self, speed):
        self.bot.motorRun(megapi.M2, speed)

def glfImpl(v):
    num = int(v)
    global ns
    if num == 0.0:
        ns.lf = "00"
    elif num == 1.0:
        ns.lf = "01"
    elif num == 2.0:
        ns.lf = "10"
    elif num == 3.0:
        ns.lf = "11"
    #print(lf)

def dsImpl(v):
    global ns
    ns.ds = float(v)
    #print(ds)

def get_linefollow():
    global bot
    bot.lineFollowerRead(4, glfImpl)

def get_dist():
    global bot
    bot.ultrasonicSensorRead(6, dsImpl)
	
class runThread(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self._stop = multiprocessing.Event()
        self.motor = Motor(bot)
        #start bot
    def run(self):
        while self._stop.is_set() is False:
            launcher(self.motor)
    def stopthread(self, timeout=None):
        self._stop.set()
        multiprocessing.Process.join(self, timeout)
    def checkStop(self):
        return self._stop.is_set()

def launcher(motor):
    get_linefollow()
    get_dist()
    import execute
    reload(execute)
    execute.run(ns.lf, 127, 127, 127, ns.ds, motor)
    
class dataThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        #start bot
    def run(self):
        while self._stop.is_set() is False:
            loop_data()
    def stopthread(self, timeout=None):
        self._stop.set()
        threading.Thread.join(self, timeout)
    def checkStop(self):
        return self._stop.is_set()

def loop_data():
    get_linefollow()
    get_dist()
    global ns
    send("lf:" + str(ns.lf) + "-ds:" + str(ns.ds))
    sleep(0.5)
    
def send(data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((CONNECT, PORT))        
        sock.sendall(bytes(data, "utf-8"))
        print("Sent:     {}".format(data))
        sock.close()
    except Exception as e:
        print("Couldn't connect!")
        print(e)

def stop():
    runWorker.stopthread()
    runWorker.join()
    info_loop.stopthread()
    info_loop.join()

def start():
    global runWorker
    runWorker = runThread()
    runWorker.start()
    global info_loop
    info_loop = dataThread()
    info_loop.start()

def callback(ip, string):
    print(string)
    if string.startswith("req"):
        stop()
        #stop_player
    elif string.startswith("prog"):
        text = string.replace("\n", "\n    ").replace("prog", HEADER, 1)
        with open("execute.py", "w") as f:
            f.write(text)
        try:
            py_compile.compile("execute.py", doraise=True)
            start()
        except py_compile.PyCompileError as e:
            send(e.msg)
    else:
        print(string)
    #program player
    #start player

with open("connect.txt", "r") as f:
    data = f.read()
    CONNECT = str(data)
    print("Server is at " + CONNECT)
thread = myThread(HOST, 5556)
thread.regcallback(callback)
try:
    if __name__ == "__main__":
        thread.start()
        manager = multiprocessing.Manager()
        global ns
        ns = manager.Namespace()
        ns.lf = "00"
        ns.ds = 0
        global bot
        bot = megapi.MegaPi()
        bot.start('/dev/ttyUSB0')
        global runWorker
        runWorker = runThread()
        global info_loop
        info_loop = dataThread()

except KeyboardInterrupt:
    thread.stopthread()
    thread.join()
    stop()
    sys.exit(0)
