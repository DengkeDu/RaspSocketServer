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

def onGas(a):
    socket_child[0].sendall("gas:"+str(a))

def onPir(a):
    socket_child[0].sendall("pir:"+str(a))

socket_child = []

class Handler(BaseRequestHandler):
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
                if 'motor' in data:
                    cmd = data.split(":")[1]
                    if 'left' in cmd:
                        bot.motorRun(1,0)
                        bot.motorRun(2,30)
                        print cmd
                    if 'right' in cmd:
                        bot.motorRun(1,30)
                        bot.motorRun(2,0)
                        print cmd
                    if 'forward' in cmd:
                        bot.motorRun(1,30)
                        bot.motorRun(2,30)
                        print cmd
                    if 'back' in cmd:
                        bot.motorRun(1,-30)
                        bot.motorRun(2,-30)
                        print cmd
                    if 'stop' in cmd:
                        bot.motorRun(1,0)
                        bot.motorRun(2,0)
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
                    elif 'gas' in cmd:
                        pid = os.fork()
                        if pid == 0:
                            while 1:
                                sleep(0.1)
                                bot.gasSensorRead(7,onGas)
                        else:
                            self.ProcessListSensor.append(pid)
                            print pid
                    elif 'pir' in cmd:
                        pid = os.fork()
                        if pid == 0:
                            while 1:
                                sleep(0.1)
                                bot.pirMotionSensorRead(8,onPir)
                        else:
                            self.ProcessListSensor.append(pid)
                            print pid
            else:
                print 'close'
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

