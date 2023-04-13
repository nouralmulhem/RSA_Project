
def primeFactors(n):
    list = []
    
    # we cant have a prime factor of n = 2 as range of primes is very large

    # cant be  a prime less than root two the number
    base = int(math.sqrt(n))
    for i in range(3,base+1,2):
         
        while n % i== 0:
            list.append(i),
            n = n / i
             
    if n > 2:
        list.append(int(n))
        
    return list

# print(primeFactors(38607194709303653))

def attack(pu, n):
    p, q = primeFactors(n)
    pr = sp.mod_inverse(pu,(p-1)*(q-1))
    return pr

attack()