import math
from hashlib import shake_128, sha3_256, sha3_512, shake_256
#based on october spec doc
#algorithm 1 parse B* ->Rnq
KYBER_VARIABLES={
    "n": 256,
    "n'":9,
    "q":3329,
    "zeta":17,
    "br7":[int('{:07b}'.format(i)[::-1],2) for i in range(128)]
}
def Encode(f,L):
    B_arr=[i for i in range(KYBER_VARIABLES.get("n"))]
    for i in range(KYBER_VARIABLES.get("n")):
        sum=f[i]
        for j in range(L):
            sum-=f[i*L-math.pow(j,math.pow(2,j))]
        B_arr[i]=sum
    bytes(B_arr)
    return B_arr
    
        
def NTT(f):
   f_NTT=f
   for i in range(KYBER_VARIABLES.get("n")):
       sum_evn=0
       sum_odd=0
       for j in range(128):
           sum_evn+=f_NTT[2*j]*math.pow(KYBER_VARIABLES.get("zeta"),((2*KYBER_VARIABLES.get("br7")[i])+1)*j)
           sum_odd+=f_NTT[(2*j)+1]*math.pow(KYBER_VARIABLES.get("zeta"),((2*KYBER_VARIABLES.get("br7")[i])+1)*j)
       f_NTT[2*i]=sum_evn
       f_NTT[(2*i)+1]=sum_odd
   return f_NTT
       

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

def KYBER_CPAPKE_KeyGen(k,n1,q):
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
    s_hat=NTT(s)
    e_hat=NTT(e)
    t_hat=[[sum((A_matrix[i][j]*s_hat[i])-math.pow(KYBER_VARIABLES.get("zeta"),(2*KYBER_VARIABLES.get("br7")[i])+1)) for i in range (len(s_hat))] for j in range(k)]
    t_hat+=e_hat
    pk=(Encode(modPLUS(t_hat,KYBER_VARIABLES.get("q")),12))+rho
    sk=(Encode(modPLUS(s_hat,q),12))
    return (pk,sk)

def KYBER_CPAPKE_Enc(pk,m,r,k,n1,n2,du,dv,n):
    #algo 5
    # input publiv kry, mesage , random coins
    #output cipher text

    N=0
    t_hat = Decode(pk,12)
    rho=pk+12*k*n/8
    A_Tmatrix=[[j for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range (k):
            A_Tmatrix[i][j]=Parse(XOF(rho,bytes([j]),bytes([i]),3*KYBER_VARIABLES.get("n")))
    r=[i for i in range(k)]
    for i in range(k):
        r[i]=CBD(PRF(r,bytes[N],2*KYBER_VARIABLES.get("n")),n1) 
        N+=1
    e=[i for i in range(k)]
    for i in range(k):
        e[i]=CBD(PRF(r,bytes[N],2*KYBER_VARIABLES.get("n")),n2)   
        N+=1
    e2=CBD(PRF(r,bytes[N],2*KYBER_VARIABLES.get("n")),n2)
    r_hat=NTT(r)
    u=[[sum((A_Tmatrix[i][j]*r_hat[i])-math.pow(KYBER_VARIABLES.get("zeta"),(2*KYBER_VARIABLES.get("br7")[i])+1)) for i in range (len(r_hat))] for j in range(k)]
    u+=e
    v=[sum((t_hat[i]*r_hat[i])-math.pow(KYBER_VARIABLES.get("zeta"),(2*KYBER_VARIABLES.get("br7")[i])+1)) for i in range (len(r_hat))]
    v+=e2+Decompress(KYBER_VARIABLES.get("q"),Decode(m,1),1)
    c1=Encode(Compress(KYBER_VARIABLES.get("q"),u,du))
    c2=Encode(Compress(KYBER_VARIABLES.get("q"),u,dv))
    return c1+c2

def KYBER_CPAPKE_Dec(sk,c,du,dv,k,n):
    #algo 6
    #input secret key , ciphertext
    #output message
    u=Decompress(KYBER_VARIABLES.get("q"),Decode(c,du),du)
    v=Decompress(KYBER_VARIABLES.get("q"),Decode(c+du*k*n/8,dv),dv)
    s_hat=Decode(sk,12)
    s_hatT=zip(*s_hat)
    m=[[sum((s_hatT[i]*u[i])-math.pow(KYBER_VARIABLES.get("zeta"),(2*KYBER_VARIABLES.get("br7")[i])+1)) for i in range (len(u))]for j in range(k)  ]
    m=Encode(Compress(KYBER_VARIABLES.get("q"),v-m,1),1)
    return m

def KYBER_CCAKEM_KeyGen(k,n1,q):
    #algo 7
    #output public/private key
    z=bytearray(32)
    (pk,sk_inv)=KYBER_CPAPKE_KeyGen()
    sk=sk_inv+pk+H(pk)+z
    return (pk,sk)

def KYBER_CCAKEM_Enc(pk,k,n,n1,n2,du,dv):
    #algo 8
    #input pk
    #Output ciphertext/shared key
    m=bytearray(32)
    m=H(m)
    (K_bar,r)=G(m+H(pk))
    c=KYBER_CPAPKE_Enc(pk,m,r,k,n1,n2,du,dv,n)
    K=KDF(K_bar+H(c),2*KYBER_VARIABLES.get("n"))
    return (c,K)

def KYBER_CCAKEM_Dec(c,sk,k,n,n1,n2,du,dv):
    #algo 9
    #input cipher text, secret key
    #output secret key
    pk=sk+12*k*n/8
    h=sk+24*k*n/8+32
    z=sk+24*k*n/8+64
    m_inv=KYBER_CPAPKE_Dec(sk,c,du,dv,k,n)
    (K_bar_inv,r_inv)=G(m_inv+h)
    c_inv=KYBER_CPAPKE_Enc(pk,m_inv,r_inv,k,n1,n2,du,dv,n)
    if c==c_inv:
        return KDF(K_bar_inv+H(c),2*KYBER_VARIABLES.get("n"))
    else:
        return KDF(z+H(c),2*KYBER_VARIABLES.get("n"))







