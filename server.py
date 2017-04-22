import socket
import os

mysocket = socket.socket()
host = socket.gethostbyname(socket.getfqdn())
port = 9876

if host == "127.0.1.1":
    import commands
    host = commands.getoutput("hostname -I")
print "host = " + host

#Prevent socket.error: [Errno 98] Address already in use
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

mysocket.bind((host, port))

mysocket.listen(5)

c, addr = mysocket.accept()

os.system('gpio mode 7 out')


while True:

    data = c.recv(1024)
    data = data.replace("\r\n", '') #remove new line character
    inputStr = "Received " + data + " from " + addr[0]
    print inputStr
    #c.send("Hello from Raspberry Pi!\nYou sent: " + data + "\nfrom: " + addr[0] + "\n")

    if data == "On":
        os.system('gpio write 7 1')
        c.send("Garage is Open\n")

    if data == "Off":
        os.system('gpio write 7 0')
        c.send("Garage is Closed\n")

    if data == "Quit": break

c.send("Server stopped\n")
print "Server stopped"
c.close()
