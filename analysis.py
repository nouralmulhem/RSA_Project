import math
import sympy as sp
import time
import random
from Crypto.Util import number
from utilities import *
import matplotlib.pyplot as plt
from attack import *


def encrypt(data, pu, n):
    ciphers = []
    while len(data)%5 != 0:
            data = data + ' '    
        
    for i in range(0, len(data), 5):
        m = encoding(data[i:i+5])
        ciphers.append(pow(m,pu,n))

    return ciphers


def decrypt(pr, n, ciphers):
    mes = ""
    for c in ciphers:
        m = pow(c,pr,n)
        mes += decoding(m)
        
    return mes


n_bits = list(range(28, 51))
enc_time = []
dec_time = []
attack_time = []
message = "hello alice this is a message by bob, this is a very long message provided by me to tell you nothing important but to get an accurate analysis of my code, now i am trying to make it longer so i can get better estimate of time"

for bit in n_bits:
    p, q, n, phi = n_generation(bit)
    pu, pr = keys_generation(phi)
    
    start = time.time() * 1000
    ciphers = encrypt(message, pu, n)
    end = time.time() * 1000
    
    enc_time.append(end - start)
    
    start = time.time() * 1000
    msg = decrypt(pr, n, ciphers)
    end = time.time() * 1000
    
    dec_time.append(end - start)
    
    print("number of bits = ", bit)
    
    start = time.time() * 1000
    attack(pu, n)
    end = time.time() * 1000
    
    attack_time.append(end - start)

print("#################################################################")
print("#################################################################")
print("enc time = ", enc_time)
print("#################################################################")
print("#################################################################")
print("dec time = ", dec_time)
print("#################################################################")
print("#################################################################")
print("attck time = ", attack_time)


x_break=np.linspace(28, 51, 51-28)

plt.plot(x_break,enc_time)
plt.xlabel('n_bits')
plt.ylabel('time')
plt.show()

plt.plot(x_break,dec_time)
plt.xlabel('n_bits')
plt.ylabel('time')
plt.show()

plt.plot(x_break,attack_time)
plt.xlabel('n_bits')
plt.ylabel('time')
plt.show()