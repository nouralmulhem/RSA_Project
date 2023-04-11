from Crypto.Util import number
import random
import numpy as np
import sympy as sp
import math


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
        



# ##########################################
# # divide message into 5 char chunks and encode each 5 charcters and perform encoding (then check if encoding is right by decoding the message again)
# ###########################################
# def crypting(text, pu, n):
#     while len(text)%5 != 0:
#         text = text + ' '
#     chunks = [PowMod(encoding(text[i:i+5]),pu,n) for i in range(0, len(text), 5)]
#     return chunks
    



###########################################
# generate encryption key from q and p
###########################################
def keys_generation(n, phi_n):
    e=random.randint(2,phi_n)
    while sp.gcd(e,phi_n) != 1:
        e=random.randint(2,phi_n) 

    # c = PowMod(ori_m,e,n)

    d=sp.mod_inverse(e,phi_n)

    # m = PowMod(c,d,n)
    
    # print(decoding(ori_m),decoding(m))
    return e, d
    

def n_generation():
    def rand_prime():
        while True:
            p = random.randrange(9001, 10000, 2)
            if all(p % n != 0 for n in range(3, int((p ** 0.5) + 1), 2)):
                return p

    p = rand_prime()
    q = rand_prime()
    while p == q:
        q = rand_prime()
    return p*q , (p-1)*(q-1)
