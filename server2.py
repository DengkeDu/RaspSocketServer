import os
import signal
import socket
from SocketServer import BaseRequestHandler,ThreadingTCPServer
import threading
import subprocess
from multiprocessing import Process
from megapi import *

def onRead(a):
    socket_child[0].sendall("ultrasonic:"+str(a))

socket_child = []

class Handler(BaseRequestHandler):
    ProcessListVideo = []
    ProcessListSensor = []
    def onRead1(a):
        print str(a)
    def handle(self):
        socket_child.append(self.request)
        address,pid = self.client_address
        print('%s connected!' % address)
        while True:
            try:
                data = self.request.recv(BUF_SIZE)
            except socket.error, e:
                print e
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
                    self.ProcessListVideo.append(child)
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
                if 'sensor' in data:
                    cmd = data.split(":")[1]
                    if 'ultrasonic' in cmd:
                        pid = os.fork()
                        if pid == 0:
                            while 1:
                                sleep(0.1)
                                bot.ultrasonicSensorRead(6,onRead)
                        else:
                            self.ProcessListSensor.append(pid)
                            print pid
            else:
                print 'close'
                for i in self.ProcessListVideo:
                    i.kill()
                for i in self.ProcessListSensor:
                    os.kill(i,signal.SIGKILL)
                for i in socket_child:
                    socket_child.remove(i)
                break

if __name__  == '__main__':
    bot = MegaPi()
    bot.start('/dev/ttyS0')
    BUF_SIZE = 1024
    HOST = ''
    PORT = 8001
    ADDR = (HOST,PORT)
    server = ThreadingTCPServer(ADDR,Handler)
    print 'listening'
    server.serve_forever()
    print(server)

