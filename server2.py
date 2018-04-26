import socket
from SocketServer import BaseRequestHandler,ThreadingTCPServer
import threading
import subprocess
from megapi import *

BUF_SIZE = 1024

class Handler(BaseRequestHandler):
    def handle(self):
        address,pid = self.client_address
        print('%s connected!' % address)
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data)>0:
                if 'video' in data:
                    port = data.split(':')[1]
                    cmd = "raspivid -t 9999999 -o - | nc %s %s" % (address,port)
                    print port
                    print cmd
                    global child
                    child = subprocess.Popen(cmd,shell=True)
                    ret = child.poll()
                    if ret:
                        child.kill()
                if 'motor' in data:
                    cmd = data.split(":")[1]
                    if 'left' in cmd:
                        print cmd
                    if 'right' in cmd:
                        print cmd
                    if 'forward' in cmd:
                        print cmd
                    if 'back' in cmd:
                        print cmd
                    if 'stop' in cmd:
                        print cmd
            else:
                print 'close'
                child.kill()
                break

if __name__  == '__main__':
    HOST = ''
    PORT = 8001
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print 'listening'
    server.serve_forever()
    print(server)

