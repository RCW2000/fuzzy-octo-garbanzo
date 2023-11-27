import random
import math
import numpy as np


def isPrime(num:int)->bool:
    if(num<1 or num==1):
        p= False
    elif num==2 or num==3:
        p=True
    else:
        for i in range(2,int(num/2)+1):
            
            if(num%i==0):
                p=False
                break
            else:
                p= True
    #print(p)
    return p

def RandomPrimes(bitsize:int)->(int,int):
    p=0
    q=0
    while(p==q):
        while(isPrime(p)==False):
            p=random.getrandbits(bitsize)
        while(isPrime(q)==False):
            q=random.getrandbits(bitsize)
    return (p,q)

def gcd(a:int,b:int)->(int,int,int):
   d=max(a,b)
   c=min(a,b)
   r1=d
   r2=c
   u1=0
   v1=1
   u2=1
   v2=0
   while r2 !=0:
       q=int(r1/r2)
       r3=r1
       u3=u1
       v3=v1
       r1=r2 
       u1=u2 
       v1=v2
       r2=r3-q*r2
       u2=u3-q*u2
       v2=v3-q*v2
   return (r1,u1,v1)

def FindInverseMod(pub_exp:int,modulus:int):
    gdiv,x,y=gcd(pub_exp,modulus)
    if(gdiv!=1):
        return False
    else:
        sec_exp=(x%modulus+modulus)%modulus
        return sec_exp
        
def isCoprime( modulus:int,pub_exp:int):
    gdiv,x,y=gcd(modulus,pub_exp)
    if(gdiv==1):
        return True
    else:
        return False
    
def GenPrimes(end:int)->list:
    #based on sieve of erastophanies
    primes=[]
    for i in range(end):
        if i<2:
            primes.append(0)
        else:
            primes.append(i)

    flag=False
    num=2
    while(flag==False and num<len(primes)):
        flag=True
        for i in range(len(primes)):
            if i==num or primes[i]==0:
                continue
            elif(i%num==0):
                primes[i]=0
                flag=False
        num=num+1
    return [i for i in primes if i !=0]
            

def isPimePow(num:int):
    primes=GenPrimes(num)
    for i in primes:
         if num % i == 0:
            c = 0
            while num % i == 0:
                num//= i
                c += 1
            if num == 1:
                return (True, i)
            else:
                return False



