import RSA
import AFUtility as util
import ShorAlgo as S
import random
import time as timer
# #Bob Creates keys
# p,q=util.RandomPrimes(5)
# pk,xk=RSA.CreateKey(p,q)
# print(p)
# print(q)
# #Alice Sends message to Bob
# message="Shhh! This is a Secret"
# enc_message=RSA.SendMessage(pk,message)

# #Emily Intercepts meassauge and uses shor's algorithm to decode it
# e,N=pk
# f1,f2=S.FactorLargePrime(N)

# #construct private key
# flag="0"
# while flag=="0":
#     Em_pk,Em_xk=RSA.CreateKey(int(f1),int(f2))
#     emily=RSA.DecodeMessage(Em_xk,enc_message)
#     print (emily)
#     flag=input("1=Stop|0=Try Again")
# #compare emily to bob
# bob=RSA.DecodeMessage(xk,enc_message)

# print(bob)

#test
#5 #10 #15 #20 bits 
def test(numbits):
    p,q=util.RandomPrimes(numbits)
    pk,xk=RSA.CreateKey(p,q)
    message="Shhh! This is a Secret"
    enc_message=RSA.SendMessage(pk,message)
    bob=RSA.DecodeMessage(xk,enc_message)
    if bob == message:
        #do test
        Attempts=0
        e,N=pk
        f1,f2,attempts=S.FactorLargePrime(N)
        Attempts+=attempts
        Em_pk,Em_xk=RSA.CreateKey(int(f1),int(f2))
        emily=RSA.DecodeMessage(Em_xk,enc_message)
        while emily != message:
            Attempts+=1
            Em_pk,Em_xk=RSA.CreateKey(int(f1),int(f2))
            emily=RSA.DecodeMessage(Em_xk,enc_message)
        return Attempts
    else:
        return False
def tester(numbits,ssize):
    for i in range(ssize+1):
        start=timer.perf_counter()
        ans=test(numbits)
        end=timer.perf_counter()
        if ans != False:
            print("numbits: "+str(numbits))
            print("num attemps: "+str(ans))
            print("tot-time: "+str(end-start))
        else:
            i-=1

#tester(5,5)
#tester(6,5)
#tester(7,5)
tester(8,5)