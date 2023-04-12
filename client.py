import socket
import threading
from utilities import *

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 5000

socketClient.connect((host, port))

p, q, n, phi = n_generation(28)
print("n = ", n, "p = ", p, "q = ", q )

pu, pr = keys_generation(n, phi)
print("pu = ", pu, "pr = ", pr )

sendKey(socketClient, pu, n)
# print("pu sent =", pu ,"n sent = ", n)
pu_rec, n_rec = receiveKey(socketClient)
# print("pu received =", pu_rec ,"n received = ", n_rec)


# pu_rec = 0
# n_rec = 0

def send():
    data = ""
    
    
    while(data != "!exit"):
        data = input()
        sendCipher(socketClient, pu_rec, n_rec, data)

def receive():
    msg = ""
    # global pu_rec
    # global n_rec
    
    
    while(msg != "exit"):
        msg = receiveMessage(socketClient, pr, n)
        print("=> ", msg)

t1 = threading.Thread(target = send)
t2 = threading.Thread(target = receive)

t1.start()
t2.start()

t1.join()
t2.join()

    