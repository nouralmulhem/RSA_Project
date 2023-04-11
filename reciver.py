# Import socket module
import socket   
from utilities import *         
 
# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect
port = 12345               
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))

n, phi = n_generation()

pu, pr = keys_generation(n, phi)

s.send(str(pu).encode())
s.send(str(n).encode())

len = int(float(s.recv(1024).decode()))

list = []
mes = ""
for i in range(len):
    cipher = int(float(s.recv(1024).decode()))
    m = PowMod(cipher,pr,n)
    mes += decoding(m)
    
print(mes)

# close the connection
s.close()  