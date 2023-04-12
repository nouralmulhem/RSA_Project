import socket
import threading
from utilities import *

socketClient = socket.socket()

host = socket.gethostname()
port = 5000

socketClient.connect((host, port))

p, q, n, phi = n_generation(28)
print("n = ", n, "p = ", p, "q = ", q )

pu, pr = keys_generation(n, phi)
print("pu = ", pu, "pr = ", pr )

pu_rec = 0
n_rec = 0

def send():
    data = ""
    socketClient.send(str(pu).encode())
    socketClient.send(str(n).encode())
    
    while(data != "!exit"):
        data = input()
        
        while len(data)%5 != 0:
            data = data + ' '    
            
        socketClient.send(str(len(data)/5).encode())

        for i in range(0, len(data), 5):
            m = encoding(data[i:i+5])
            cipher = PowMod(m,pu_rec,n_rec)
            print(cipher)
            socketClient.send(str(cipher).encode())

def receive():
    data = ""
    global pu_rec
    pu_rec = int(socketClient.recv(1024).decode())
    global n_rec
    n_rec = int(socketClient.recv(1024).decode())
    print("pu server =", pu_rec ,"n = ", n_rec)
    while(data != "exit"):
        len = int(float(socketClient.recv(1024).decode()))

        mes = ""
        for i in range(len):
            cipher = int(float(socketClient.recv(1024).decode()))
            m = PowMod(cipher,pr,n)
            mes += decoding(m)
            
        print("=> ",mes)

t1 = threading.Thread(target = send)
t2 = threading.Thread(target = receive)

t1.start()
t2.start()

t1.join()
t2.join()

    