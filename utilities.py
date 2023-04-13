from Crypto.Util import number
import random
import numpy as np
import sympy as sp
import math
import json



###########################################
# map and demap each char to its number
###########################################
def map(char):
    if ord(char) > 96 and ord(char) < 123:
        return ord(char) - 87
    elif ord(char) > 47 and ord(char) < 58:
        return ord(char) - 48
    else: return 36

def demap(num):
    if num < 10:
        return chr(num + 48)
    elif num < 36:
        return chr(num + 87)
    else: return chr(32)
    



###########################################
# encode message of 5 charcters to int and decode the message using equation provided
###########################################
def decoding(number):
    list = []
    sum = 0
    for i in range(5):
        num = int((number % 37**(i+1) - sum ) / 37**i)
        sum = sum + num * 37**i
        list.append(demap(num))
    return "".join(list[::-1])

def encoding(list):
    sum = 0
    for i in range(5):
        sum = sum + map(list[i])*(37**(4-i))
    return sum


###########################################
# generate encryption key from n and phi(n)
###########################################
def keys_generation(phi_n):
    public_key = random.randint(2,phi_n)
    while sp.gcd(public_key,phi_n) != 1:
        public_key=random.randint(2,phi_n) 

    private_key=sp.mod_inverse(public_key,phi_n)

    return public_key, private_key
    


###########################################
# generate two large primes q and p then get n and phi(n)
###########################################
def n_generation(n_bits):
    p = number.getPrime(n_bits // 2)
    q = number.getPrime(n_bits // 2)
    while p == q:
        q = number.getPrime(n_bits // 2)
        
    return p, q, p*q , (p-1)*(q-1)




###########################################
# sending encrypted packets one by one and receive the message
###########################################
def sendCipher(socket, pu, n, data):
    while len(data)%5 != 0:
            data = data + ' '    
        
    socket.send(str(len(data)/5).encode())

    for i in range(0, len(data), 5):
        m = encoding(data[i:i+5])
        cipher = pow(m,pu,n)
        socket.send(str(cipher).encode())
  

def receiveMessage(socket, pr, n):
    len = int(float(socket.recv(2048).decode()))

    mes = ""
    for i in range(len):
        cipher = int(float(socket.recv(2048).decode()))
        m = pow(cipher,pr,n)
        mes += decoding(m)
        
    return mes



###########################################
# send and receive the public key first
###########################################
def sendKey(socket, pu, n):
    msg = [pu, n]
    socket.send(json.dumps(msg).encode())


def receiveKey(socket):
    pu_rec, n_rec = json.loads(socket.recv(2048).decode())
    return pu_rec, n_rec

