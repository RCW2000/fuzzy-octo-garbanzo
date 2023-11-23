import random
import AFUtility as util
def CreateKey(p:int,q:int):
    N=p*q
    phi=(p-1)*(q-1)
    #do while
    while(True):
        #gen random value
        e=random.randint(2,phi-1)
        #check if coprime
        if(util.isCoprime(phi,e)):
            break
    d=int(util.FindInverseMod(e,phi))
    public_key=(e,N)
    private_key=(d,N)
    return public_key,private_key

def SendMessage(public_key:(int,int), message:str)->list:
    e,N=public_key
    c_tex=[(ord(char)**e)%N for char in message] 
    #use public key to endode blocks
    #return encoded blocks
    return c_tex
def DecodeMessage(private_key:(int,int), enc_message:list)->str:
    d,N=private_key
    p_tex=[chr((num**d)%N) for num in enc_message]
    string=""
    for char in p_tex:
        string+=char
    #return decoded message
    return string


    







#primes=util.RandomPrimes(6)
#p,q=primes
#pubK,priK=CreateKey(p,q)
#message="Hello World. I sure hope this works!"
#sent=SendMessage(pubK,message)
#recieved=DecodeMessage(priK,sent)
#if(recieved==message):
    #print("Hey it worked!")
    #print("N="+str(pubK))
#else:
    #print("Boo Hoo :(")
    #print(recieved)
    #print(util.gcd(205,783))
    #print(111%3)
