import math
#based on october spec doc
#algorithm 1 parse B* ->Rnq
KYBER_VARIABLES={
    "n": 256,
    "n'":9,
    "q":3329
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

def CBD(B:bytearray):
    #alorithm 2
    #input byte array of length 64n
    #output f polynomial in Rq
    bits=BytesToBits(B)
    f_polynomial=[0 for i in range(256)]
    for i in range(256):
        sum_a=0
        sum_b=0
        for j in range(KYBER_VARIABLES.get("n")):
            sum_a+=bits[2*i*KYBER_VARIABLES.get("n")]+j
            sum_b+=bits[2*i*KYBER_VARIABLES.get("n")]+KYBER_VARIABLES.get("n")+j
        f_polynomial[i]=sum_a-sum_b
    return f_polynomial






