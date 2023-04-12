import socket
import threading
from utilities import *

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 1234

socketClient.connect((host, port))

p, q, n, phi = n_generation(28)
print("n = ", n, "p = ", p, "q = ", q )

pu, pr = keys_generation(phi)
print("pu = ", pu, "pr = ", pr )

sendKey(socketClient, pu, n)
pu_rec, n_rec = receiveKey(socketClient)

def send():
    data = ""
    while(data != "!exit"):
        data = input()
        sendCipher(socketClient, pu_rec, n_rec, data)

def receive():
    msg = ""
    while(msg != "exit"):
        msg = receiveMessage(socketClient, pr, n)
        print("=> ", msg, flush=True)

t1 = threading.Thread(target = send)
t2 = threading.Thread(target = receive)

t1.start()
t2.start()

t1.join()
t2.join()

    