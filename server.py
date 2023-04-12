import socket
import threading
from utilities import *

socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 5000

socketServer.bind((host, port))

# we are listening to two clients at a time
socketServer.listen(2)

# get connection with two clients
conn1, address1 = socketServer.accept()
conn2, address2 = socketServer.accept()

# this function send data from one client to another using the connections of both
# clients obtained before
def send(fromConnection, toConnection):
    while(True):
        data = fromConnection.recv(1024).decode()
        toConnection.send(data.encode())

t1 = threading.Thread(target = send, args = (conn1, conn2))
t2 = threading.Thread(target = send, args = (conn2, conn1))

t1.start()
t2.start()

t1.join()
t2.join()

conn1.close()
conn2.close()
