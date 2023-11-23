import RSA
import AFUtility as util
import ShorAlgo as S
import random
#Bob Creates keys
p,q=util.RandomPrimes(5)
pk,xk=RSA.CreateKey(p,q)
print(p)
print(q)
#Alice Sends message to Bob
message="Shhh! This is a Secret"
enc_message=RSA.SendMessage(pk,message)

#Emily Intercepts meassauge and uses shor's algorithm to decode it
e,N=pk
f1,f2=S.FactorLargePrime(N)

#construct private key
flag="0"
while flag=="0":
    Em_pk,Em_xk=RSA.CreateKey(int(f1),int(f2))
    emily=RSA.DecodeMessage(Em_xk,enc_message)
    print (emily)
    flag=input("1=Stop|0=Try Again")
#compare emily to bob
bob=RSA.DecodeMessage(xk,enc_message)

print(bob)

