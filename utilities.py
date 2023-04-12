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
# calc power mod number for large numbers
###########################################
def PowMod(a, n, mod): 
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    else:
        b = PowMod(a, n // 2, mod)
        b = b * b % mod
        if n % 2 == 0:
          return b
        else:
          return b * a % mod
        


###########################################
# generate encryption key from n and phi(n)
###########################################
def keys_generation(n, phi_n):
    e=random.randint(2,phi_n)
    while sp.gcd(e,phi_n) != 1:
        e=random.randint(2,phi_n) 

    d=sp.mod_inverse(e,phi_n)

    return e, d
    


###########################################
# generate two large primes q and p then get n and phi(n)
###########################################
def n_generation(n_bits):
    p = number.getPrime(n_bits // 2)
    q = number.getPrime(n_bits // 2)
    while p == q:
        q = number.getPrime(n_bits // 2)
        
    return p, q, p*q , (p-1)*(q-1)


def isPrime(n):
      
    # Corner case
    if n <= 1 :
        return False
  
    # check from 2 to n-1
    for i in range(2, n):
        if n % i == 0:
            return False
  
    return True

list = []
def printPrime(n):
    for i in range(2, n + 1):
        if isPrime(i):
            list.append(i)
# printPrime(226791289 // 2)

###########################################
# attack plain-cipher pairs
###########################################
def attack(plain, cipher, n, pu):
    for x in list:
        for y in list:
            new_n = x*y
            if cipher == PowMod(plain, pu, new_n):
                return x, y, sp.mod_inverse(pu,(x-1)*(y-1)), new_n

# x, y, pr, n = attack(encoding("hello"), 20265125, 226791289, 142671923)
# print("n = ", n)


def sendCipher(socket, pu, n, data):
    while len(data)%5 != 0:
            data = data + ' '    
        
    socket.send(str(len(data)/5).encode())

    for i in range(0, len(data), 5):
        m = encoding(data[i:i+5])
        cipher = PowMod(m,pu,n)
        socket.send(str(cipher).encode())
        

def receiveMessage(socket, pr, n):
    len = int(float(socket.recv(1024).decode()))

    mes = ""
    for i in range(len):
        cipher = int(float(socket.recv(1024).decode()))
        m = PowMod(cipher,pr,n)
        mes += decoding(m)
        
    return mes

def sendKey(socket, pu, n):
    msg = [pu, n]
    socket.send(json.dumps(msg).encode())

def receiveKey(socket):
    pu_rec, n_rec = json.loads(socket.recv(1024).decode())
    return pu_rec, n_rec

