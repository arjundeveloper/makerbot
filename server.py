# All rights reserved 2017
# By Lucas Tan for Robotics and Maker Academy, Singapore Polytechnic

import gi
gi.require_version('Gtk', '3.0')
#gi.require_version('WebKit2', '4.0') 
#from gi.repository import WebKit2
from gi.repository import GObject
from gi.repository import Gtk
from enum import Enum
from tcpserver import myThread
import subprocess
import socket

GObject.threads_init()

class LabelWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Platform Client")
        self.set_default_size(800, 600)
        
        self.grid = Gtk.VBox()
        self.add(self.grid)
        self.grid.set_homogeneous(False)

        self.top_box = Gtk.HBox()
        self.iplabel = Gtk.Label("IP of RPi: ")
        self.top_box.pack_start(self.iplabel, False, False, 0)
        self.ip_box = Gtk.Entry()
        self.top_box.pack_end(self.ip_box, True, True, 0)
        self.grid.pack_start(self.top_box, False, False, 0)

        self.box = Gtk.HBox()
        #self.bro = WebKit2.WebView()
        #self.bro.load_uri("http://192.168.0.102:8081")
        #bro.load_uri("http://192.168.0.104")
        self.bro = Gtk.TextView()
        self.buffer = self.bro.get_buffer()
        windowToAdd = Gtk.ScrolledWindow()
        windowToAdd.add(self.bro)
        self.grid.pack_start(windowToAdd, True, True, 0)
      
        self.label = Gtk.Label("Data")
        self.box.add(self.label)

        self.open_button = Gtk.Button.new_with_label("Open file")
        self.open_button.connect("clicked", self.open_file)
        self.box.pack_end(self.open_button, False, False, 0)

        self.bot_upload_button = Gtk.Button.new_with_label("Upload to robot and start program")
        self.bot_upload_button.connect("clicked", self.upload)
        self.box.pack_end(self.bot_upload_button, False, False, 0)
        #upload to robot
        
        self.button = Gtk.Button.new_with_label("Stop program")
        self.button.connect("clicked", self.button_click)
        self.box.pack_end(self.button, False, False, 0)

        self.grid.pack_end(self.box, False, False, 0)
        #label2 = Gtk.Label("More data")
        #self.box.add(label2)

    def upload(self, button):
        text = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
        self.send("prog:\n" + text)

    def button_click(self, button):
        self.send("request")

    def open_file(self, button):
        dialog = Gtk.FileChooserDialog("Select file", self, Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filter_any = Gtk.FileFilter()
        filter_any.set_name("All files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print ("Selected file " + dialog.get_filename())
            with open(dialog.get_filename(), 'r') as f:
                 data = f.read()
                 self.buffer.set_text(data)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancelled")
        dialog.destroy()

        #read file
    def send(self, data):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip_box.get_text(), 5556))        
            sock.sendall(bytes(data, "utf-8"))
            print("Sent:     {}".format(data))
            sock.close()
        except ConnectionRefusedError:
            print("Couldn't connect!")

window = LabelWindow()  

def callback(ip, string):
    output = "{} wrote\n".format(ip)

    splitout = string.split("-")
    for result in splitout:
        output = "".join((output, result, "\n"))
        window.label.set_text(output)
    #window.grid.pack_end(label1)
    #window.show_all()



thread = myThread("0.0.0.0", 5555)
thread.regcallback(callback)

def quit(self):
    thread.stopthread()
    Gtk.main_quit()
      
window.connect("destroy", quit)
window.show_all()

if __name__ == "__main__":
    thread.start()
Gtk.main()

