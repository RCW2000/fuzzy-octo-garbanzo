import random
import numpy as np
import math
q=17
def LowPolyKeyGen():
    s1=[]
    for i in range(4):
        s1.append(random.randint(0,10)%q)
    return np.polynomial.polynomial.Polynomial(s1)

def BK_KeyGen():
    s=[[LowPolyKeyGen()],
       [LowPolyKeyGen()]]
    
    e=[[LowPolyKeyGen()],
       [LowPolyKeyGen()]]
    
    A=[[0,0],
       [0,0]]
    for i in range(2):
        for j in range(2):
            A[i][j]=LowPolyKeyGen()
    t=np.matmul(np.array(A),np.array(s))
    
    t=np.array(t)+np.array(list(e))
    return (np.array(s)),(np.array(A),t)

def BK_Enc(message,key:()):
    A,t=key
    r=(LowPolyKeyGen(),LowPolyKeyGen())
    
    e1=(LowPolyKeyGen(),LowPolyKeyGen())
    
    e2=(LowPolyKeyGen())
    
    m=bin(message)[2:]
    m=[int(m[i])for i in range(len(m))]
    print(m)
    polym=np.polynomial.polynomial.Polynomial(m)
    polym=polym*round(q/2)
    print(polym)
    u=np.matmul(np.transpose(A),np.array(list(r)))+np.array(list(e1))
    v=np.matmul(np.transpose(t),np.array(list(r)))+np.array(list(e2))+np.array([polym])
    return (u,v)

def BK_Dec(ctex:(),s):
    u,v=ctex
    nm=v-np.matmul(np.transpose(s),u)

    print(nm)
    m=[i for i in range(len(nm))]
    for i in range(len(nm)):
        if round(nm[i])==round(q/2):
            m[i]=round(nm[i])/round(q/2)
        else:
            m[i]=0
    #convert back
    m=[chr(m[i]) for i in range(len(m))]
    return m

#bk
s,AT=BK_KeyGen()
UV=BK_Enc(11,AT)
print(BK_Dec(UV,s))