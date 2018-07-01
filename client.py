import socket

HOST = '192.168.12.1' # you ip address
PORT = 8001
ADDR = (HOST,PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(ADDR)
    print "connect"
except socket.error as msg:
    print "Socket Error: %s" % msg

while True:
    print "1: [motor:left]"
    print "2: [sensor:ultrasonic]"
    print "3: [sensor:gas]"
    print "4: [sensor:pir]"
    print "5: []"
    print "9: exit"
    args = input()
    if args == 1:
        s.send("motor:left")
    if args == 2:
        s.send("sensor:ultrasonic")
    if args == 3:
        s.send("sensor:gas")
    if args == 4:
        s.send("sensor:pir")
    if args == 9:
        break

s.close()
