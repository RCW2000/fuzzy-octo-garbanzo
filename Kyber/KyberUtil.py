import math
from hashlib import shake_128, sha3_256, sha3_512, shake_256
#based on october spec doc
#algorithm 1 parse B* ->Rnq
KYBER_VARIABLES={
    "n": 256,
    "n'":9,
    "q":3329
}
def Compress(q,x,d):
    rounded=int(round(((math.pow(2,d)/q)*x),-1))
    return modPLUS(rounded,math.pow(2,d))
def Decompress(q,x,d):
    return int(round((q/math.pow(2,d))*x),-1)
def XOF(B_star,B1,B2,length):
    input_B=B_star+B1+B2
    return shake_128(input_B).digest(length)

def PRF(s,b,length):
    B=s+b
    return shake_256(B).digest(length)

def H(B):
    return sha3_256(B).digest()

def G(B):
    out=sha3_512(B).digest()
    return out[32:],out[:32]

def KDF(B,length):
    return shake_256(B).digest(length)

KYBER512_VARIABLES={
    "k":2,
    "n1":3,
    "n2":2,
    "(du,dv)":(10,4),
    "delta":math.pow(2,-139)
}
KYBER768_VARIABLES={
    "k":3,
    "n1":2,
    "n2":2,
    "(du,dv)":(10,4),
    "delta":math.pow(2,-164)
}
KYBER1024_VARIABLES={
    "k":4,
    "n1":2,
    "n2":2,
    "(du,dv)":(11,5),
    "delta":math.pow(2,-174)
}
def modPLUS(r,a):
    for i in range(a):
        if i==r%a:
            return i

def BytesToBits(B:bytearray):
    return [((B[i/8]/math.pow(2,(i%8)))%2) for i in range(len(B))]

def Parse(B:bytearray):
    #algorithm 1
    #input byte array
    #output NTT representation (a_coefficients)
    a_coefficients=[0 for i in range(KYBER_VARIABLES.get("n"))]
    i=0
    j=0
    while j<KYBER_VARIABLES.get("n"):
        d1=B[i]+256*(modPLUS(B[i+1],16))
        d2=math.floor(B[i+1]/16)+16*B[i+2]
        if d1<KYBER_VARIABLES.get("q"):
            a_coefficients[j]=d1
            j+=1
        if d2<KYBER_VARIABLES.get("q") and j<KYBER_VARIABLES.get("n"):
            a_coefficients[j]=d2
            j+=1
        i+=3
    return a_coefficients

def CBD(B:bytearray,ETA):
    #alorithm 2
    #input byte array of length 64ETA
    #output f polynomial in Rq
    bits=BytesToBits(B)
    f_polynomial=[0 for i in range(KYBER_VARIABLES.get("n"))]
    for i in range(KYBER_VARIABLES.get("n")):
        sum_a=0
        sum_b=0
        for j in range(ETA):
            sum_a+=bits[2*i*ETA]+j
            sum_b+=bits[2*i*ETA]+ETA+j
        f_polynomial[i]=sum_a-sum_b
    return f_polynomial

def Decode(B:bytearray,L):
    #algorithm 3
    #input byte array of length 32L
    #output f polynomial in Rq
    bits=BytesToBits(B)
    f_polynomial=[0 for i in range(KYBER_VARIABLES.get("n"))]
    for i in range(KYBER_VARIABLES.get("n")):
        f_sum=0
        for j in range(L):
            f_sum+=bits[(i*L)+math.pow(j,2*j)]
        f_polynomial[i]=f_sum
    return f_polynomial

def KYBER_CPAPKE_KeyGen(k,n1):
    #algorithm 4
    #outputs public and secret key
    d=bytearray(32)
    (rho,sigma)=G(d)
    N=0
    A_matrix=[[j for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(k):
            A_matrix[i][j]=Parse(XOF(rho,bytes([j]),bytes([i]),3*KYBER_VARIABLES.get("n")))
    s=[i for i in range(k)]
    for i in range(k):
        s[i]=CBD(PRF(sigma,bytes([N]),len(sigma)+len(N)),n1)
        N+=1
    e=[i for i in range(k)]
    for i in range(k):
        e[i]=CBD(PRF(sigma,bytes([N]),len(sigma)+len(N)),n1)
        N+=1
    








