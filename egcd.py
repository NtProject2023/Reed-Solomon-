import gmpy2
import bisect


def bit(n,i):  #finding the ith bit in the binary representation of n
    n1 =n>>i
    n2 = n>>(i+1)
    bi = n1 - 2*n2
    return bi

def power(a,n):   #repeatd squaring algorithm
    p = 1
    for i in range(gmpy2.bit_length(n)):
        if bit(n,i) == 1:
            p = p*a
        a = gmpy2.square(a)
    return p

def G(x):
    return gmpy2.mpz(str(x))

def bin_egcd(a,b):
    a,b=G(a),G(b)
    r1,r2 = max(a,b),min(a,b)
    e = G(0)
    while r1%2 == 0 and r2%2 == 0:
        r1,r2 = r1>>1,r2>>1
        e = e + 1
    
    x,y = r1,r2
    s1,s2 = G(1),G(0)
    t1,t2 = G(0),G(1)
    
    while r2 != 0:
        while r1%2 == 0:
            r1 = r1>>1
            if s1%2 == G(0)  and t1%2 == G(0):
                s1,t1 = s1>>1,t1>>1
            else:
                s1,t1 = (s1+y)>>1,(t1-x)>>1
        while r2%2 == 0:
            r2 = r2>>1
            if s2%2 == 0  and t2%2 == 0:
                s2,t2 = s2>>1,t2>>1
            else:
                s2,t2 = (s2+y)>>1,(t2-x)>>1
        if r2<r1:
            r1,s1,t1,r2,s2,t2 = r2,s2,t2,r1,s1,t1
        r2,s2,t2 = (r2 - r1),(s2 - s1),(t2 - t1)
    return power(2,e)*r1,s1,t1

print(bin_egcd(280,480))

def inverseModn(b,n):
    g,s,t = bin_egcd(b,n)
    # if(s<0):
    #     s = s+n
    return t

def PreCompute(numbers):
    sz = len(numbers)
    product=1
    for i in range(0,sz):
        product = product*numbers[i]
    partialProducts = []
    for i in range(0,sz):   
        partialProducts.append(gmpy2.f_div(product,numbers[i]))
    return product,partialProducts

def CRT(remainders,numbers):
    product,partialProducts = PreCompute(numbers)
    sz = len(numbers)
    a=0
    # print(partialProducts)
    for i in range(0,sz):
        b_i = partialProducts[i]%numbers[i]
        t_i = inverseModn(b_i,numbers[i])
        # print(b_i,numbers[i],t_i)
        e_i = (partialProducts[i]*t_i)%(numbers[i])
        a = a + e_i*remainders[i]
        print(f'b_i- {b_i},t_i- {t_i},e_i- {e_i} i- {i}')
        print(f'value of a- {a} at i -{i}')
    a = a%product
    print(f'value of a - {a}')
    return a

num = [3,4,5]
rem = [2,3,1]

print(CRT(rem,num));        

def egcd(a,b):
    s,t,r=[],[],[]
    (a,b)=(G(max(int(a),int(b))),G(min(int(a),int(b))))
    # print(a,b)
    prevx, x = G(1), G(0); prevy, y = G(0), G(1)
    s.append(prevx);t.append(prevy);r.append(a)
    while b:
        s.append(x);t.append(y);r.append(b)
        quo,rem = gmpy2.t_divmod(a,b)
        x,prevx = prevx - quo*x, x
        y, prevy = prevy - quo*y, y
        a, b = b, rem
    return s,t,r

print(egcd(280,480))


k=G(10) 

def GlobalSetup(u,M):
    global kPrimes
    u = gmpy2.mpfr(u)
    M= G(M)
    countOfPrimes=0
    kPrimes=[]
    rand_state = gmpy2.random_state()
    while(countOfPrimes<k):
        r = gmpy2.mpz_random(rand_state, 2**7)
        if(gmpy2.is_prime(r) and r not in kPrimes):
            kPrimes.append(r)
            countOfPrimes=countOfPrimes+1
    print(f'kPrimes- {kPrimes}')

a = 100
u = 0.4
M = 1000
# kPrimes = GlobalSetup(u,M)

def Transmit(residues):
    global u,k,kPrimes
    rand_state = gmpy2.random_state()
    rounded = gmpy2.rint_floor(u*k)
    rounded = int(rounded)
    rounded = G(rounded)
    l = gmpy2.mpz_random(rand_state,rounded)
    corruptedIndices =[]
    countOfCorrupted = 0
    residueRecieved = []
    while(countOfCorrupted<l):
        r = gmpy2.mpz_random(rand_state, k)
        if(r not in corruptedIndices):
            corruptedIndices.append(r)
            countOfCorrupted = countOfCorrupted+1
    for i in range(0,k):
        if(i in corruptedIndices):
            b_i = gmpy2.mpz_random(rand_state,kPrimes[i]-1)
            while(b_i == residues[i]):
                b_i = gmpy2.mpz_random(rand_state,kPrimes[i]-1)
        else:
            b_i = residues[i]
        residueRecieved.append(b_i)
    print(f'l - {l}')
    print(f'corrupted - {corruptedIndices}')
    print(residueRecieved)
    return residueRecieved,l

def ReedSolomonSend(a):
    a = G(a)
    print(f'kPrimes in send- {kPrimes}')
    residues = []
    for i in range(len(kPrimes)):
        residues.append(a%kPrimes[i])
    # print(kPrimes)
    print(f'residue gen- {residues}')
    return residues
    # Transmit(residues)

# print(ReedSolomonSend(a))


def ReedSolomonRecieve(residueRecieved,l):
    global M,kPrimes
    b = CRT(residueRecieved,kPrimes)
    print(f'b = {b}')
    check=[]
    for i in range(0,len(kPrimes)):
        check.append(b%kPrimes[i]==residueRecieved[i])
    print(check)
    n = G(1)
    for i in kPrimes:
        n = n*i
    s_list,t_list,r_list = egcd(n,b)
    print(f'r list - {r_list}')
    print(f't list - {t_list}')
    kPrimes.sort(reverse=True)
    P = G(1)
    for i in range(0,l):
        P = P*kPrimes[i]
    r = M * P
    t = P
    for i in range(0,len(r_list)):
        if(r_list[i]<r):
           index =i
           break
    if(r_list[i]%t_list[i]==0):
        print(r_list[i]/t_list[i])
        a = r_list[i]/t_list[i]
        print(a)
        # return True
    else:
        print("couldn't reconstruct the message")
        # return False

def Reed():
    u = str(input("Error fraction- "))
    M = str(input("Bound- "))
    GlobalSetup(u,M)
    while(1):
        a = str(input("Enter the number to transmit- "))
        residues = ReedSolomonSend(a)
        residuesRecieved,l = Transmit(residues)
        ReedSolomonRecieve(residuesRecieved,l)
        
Reed()
        
        
        
    
    
        
    
    
            