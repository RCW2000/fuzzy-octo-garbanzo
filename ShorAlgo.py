
import AFUtility as util
import math
import random
import sys
from fractions import Fraction
import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import ResourceCounter, Simulator
from projectq.cengines import (
    AutoReplacer,
    DecompositionRuleSet,
    InstructionFilter,
    LocalOptimizer,
    MainEngine,
    TagRemover,
)
from projectq.libs.math import AddConstant, AddConstantModN, MultiplyByConstantModN
from projectq.meta import Control
from projectq.ops import QFT, All, BasicMathGate, H, Measure, R, Swap, X, get_inverse

def high_level_gates(eng, cmd):
    return True

resource_counter = ResourceCounter()
rule_set = DecompositionRuleSet(modules=[projectq.libs.math, projectq.setups.decompositions])
compilerengines = [
    AutoReplacer(rule_set),
    InstructionFilter(high_level_gates),
    TagRemover(),
    LocalOptimizer(3),
    AutoReplacer(rule_set),
    TagRemover(),
    LocalOptimizer(3),
    resource_counter,
]
# make the compiler and run the circuit on the simulator backend
eng = MainEngine(Simulator(), compilerengines)
def find_period(eng, N, a, verbose=False):
    
    n = int(math.ceil(math.log(N, 2))) # log2(N)

    x = eng.allocate_qureg(n)

    '''Pauli-X gate: acts on a single qubit. It is the quantum equivalent of the NOT gate for classical computers'''
    X | x[0]

    measurements = [0] * (2 * n)  # will hold the 2n measurement results

    ctrl_qubit = eng.allocate_qubit()

    for k in range(2 * n):
        '''Compute a^x mod N conditioned on a control qubit ctrl_qubit in a uniform superposition of 0 and 1'''
        current_a = pow(a, 1 << (2 * n - 1 - k), N) # << is binary left shift, so we are computing a^(2^(2n-1-k)) mod N
        # one iteration of 1-qubit QPE (Quantum Phase Estimation)
        H | ctrl_qubit
        with Control(eng, ctrl_qubit):
            MultiplyByConstantModN(current_a, N) | x

        # perform semi-classical inverse QFT --> Rotations conditioned on previous outcomes
        for i in range(k):
            if measurements[i]:
                R(-math.pi/(1 << (k - i))) | ctrl_qubit
        
        # final Hadamard of the inverse QFT
        H | ctrl_qubit

        # and measure
        Measure | ctrl_qubit
        eng.flush() # flush all gates and execute measurements
        measurements[k] = int(ctrl_qubit)
        if measurements[k]:
            X | ctrl_qubit # reset

        if verbose:
            print("\033[95m{}\033[0m".format(measurements[k]), end="")
            sys.stdout.flush()

    All(Measure) | x # shortcut (instance of) projectq.ops.Tensor
    # turn the measured values into a number in [0,1)
    y = sum([(measurements[2 * n - 1 - i]*1. / (1 << (i + 1)))
             for i in range(2 * n)])

    # continued fraction expansion to get denominator (the period)
    r = Fraction(y).limit_denominator(N-1).denominator

    # return the (potential) period
    return r


# Filter function, which defines the gate set for the first optimization
# (don't decompose QFTs and iQFTs to make cancellation easier)




def FactorLargePrime(N:int)->(int,int): 
    attempt=0
    #base cases not covered by order finding
    if N%2==0 and util.isPimePow(N)==False:
        return (N/2,2)
    elif util.isPimePow(N)!=False:
        ispow,prime=util.isPimePow(N)
        return (prime,N/prime)
    else:
        while(True):
            attempt=attempt+1
            print("Quantum Attempt: "+str(attempt))
            #find relative prime a
            a = random.randint(2, N-1)
            d,f,g=util.gcd(a,N)
            if d>1:
                return (d,N/d)
            r = find_period(eng, N, a,True)
            print(r)
            if r % 2 != 0:
                r *= 2
                apowrhalf = pow(a, r >> 1, N)
                f1,f,g = util.gcd(apowrhalf + 1, N)
                f2,f,g = util.gcd(apowrhalf - 1, N)
                if (not f1 * f2 == N) and f1 * f2 > 1 and int(1.0 * N / (f1 * f2)) * f1 * f2 == N:
                    f1, f2 = f1 * f2, int(N / (f1 * f2))
                if f1 * f2 == N and f1 > 1 and f2 > 1:
                    return (f1,f2)
                        
            

    

    

    # choose a base at random:
""" a = int(random.random() * N)
    if not util.gcd(a, N) == 1:
        print("\n\n\t\033[92mOoops, we were lucky: Chose non relative prime" " by accident :)")
        print(f"\tFactor: {util.gcd(a, N)}\033[0m")
    else:
        # run the quantum subroutine
        

        # try to determine the factors
        if r % 2 != 0:
            r *= 2
        apowrhalf = pow(a, r >> 1, N)
        f1 = util.gcd(apowrhalf + 1, N)
        f2 = util.gcd(apowrhalf - 1, N)
        if (not f1 * f2 == N) and f1 * f2 > 1 and int(1.0 * N / (f1 * f2)) * f1 * f2 == N:
            f1, f2 = f1 * f2, int(N / (f1 * f2))
        if f1 * f2 == N and f1 > 1 and f2 > 1:
            print(f"\n\n\t\033[92mFactors found :-) : {f1} * {f2} = {N}\033[0m")
        else:
            print(f"\n\n\t\033[91mBad luck: Found {f1} and {f2}\033[0m")

        print(resource_counter)  # print resource usage
        """