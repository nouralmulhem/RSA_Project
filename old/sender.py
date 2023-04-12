# first of all import the socket library
import socket   
from utilities import *         
 
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12346               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")  

# Establish connection with client.
c, addr = s.accept()    
print ('Got connection from', addr )

pu = int(c.recv(1024).decode())
n = int(c.recv(1024).decode())
print("pu =",pu)

 
# a forever loop until we interrupt it or
# an error occurs
text = ""
while text != "exit":
    text = input('Enter your message:')
    x = text
    
    while len(x)%5 != 0:
        x = x + ' '    
        
    c.send(str(len(x)/5).encode())

    for i in range(0, len(x), 5):
        m = encoding(x[i:i+5])
        cipher = PowMod(m,pu,n)
        print(cipher)
        c.send(str(cipher).encode())

# Close the connection with the client
c.close()