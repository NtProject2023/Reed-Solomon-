import gmpy2

#used to generate 'k' primes such that their product is greater than 2MP^2  (M-the upper bound on the message, P-max possible product of any l primes which belong to the chosen 'k' primes)
#the value of k is being generated by adding a new prime to the list until the above condition is satisfied
def GlobalSetup(u,M):
    global kPrimes
    global k

    kPrimes = []                                                #stores the list of k primes
    rand_state = gmpy2.random_state()
    product = G(1)                        #stores the current product of all primes in kPrimes
    countOfPrimes = G(0)                    #stores a count of the number of primes currently in kPrimes
    limit = count_primes(M)//2              #maximum value of k (for the sake of implementation)

    while product <= 2*M*(maxProd(countOfPrimes)**2) and countOfPrimes<limit:       #generating k primes
        r = gmpy2.mpz_random(rand_state,M)
        if(gmpy2.is_prime(r,10) and r not in kPrimes):
            kPrimes.append(r)
            countOfPrimes=countOfPrimes+1
            product = product * r
    
    k = countOfPrimes



#generates the residues a_i
def ReedSolomonSend(a):
    a = G(a)
    residues = []                         #stores the values of a_i = a (mod n_i)
    for i in range(len(kPrimes)):
        residues.append(a%kPrimes[i])     #calcualting a_i

    return residues



#Imitates the faults of message sending and correspondingly generates the values of b_i
def Transmit(residues):     #residues - a list of a_i generated by the sender
    global u,k,kPrimes

    rand_state = gmpy2.random_state()   #random number generator object
    rounded = gmpy2.rint_ceil(u*k)
    rounded = G(int(rounded))
    l=G(0)                              # l - maximum number of residues that can be corrupted (randomly generated in the next step for the sake of implementation)
    if(rounded!=0):    #mpz_random generates a random number between 0,rounded-1 (in this case). If rounded = 0, the function will give an error
        l = gmpy2.mpz_random(rand_state,rounded)
    
    corruptedIndices =[]    #stores the indices of the corrupted residues that are sent to the receiver
    countOfCorrupted = 0    #keeps count of the number of corrupted residues
    residueRecieved = []    #stores the residue values received by the receiver

    while(countOfCorrupted<l):                   #to generate l distinct corrupted indices
        r = gmpy2.mpz_random(rand_state, k)
        if(r not in corruptedIndices):      
            corruptedIndices.append(r)
            countOfCorrupted = countOfCorrupted+1

    for i in range(0,k):                         #generation of b_i
        if(i in corruptedIndices):
            b_i = gmpy2.mpz_random(rand_state,kPrimes[i])
            print(b_i,residues[i],kPrimes[i])
            while(b_i == residues[i]):
                b_i = gmpy2.mpz_random(rand_state,kPrimes[i])
        else:
            b_i = residues[i]
        residueRecieved.append(b_i)

    return residueRecieved,l

        

#takes the corrupted residues and tries to contruct the message it has received
def ReedSolomonRecieve(residueRecieved,l):
    global M,kPrimes
    b = CRT(residueRecieved,kPrimes)    #constructs b
    n = G(1)                            #n stores the product of k primes
    for i in kPrimes:
        n = n*i

    s_list,t_list,r_list = egcd(n,b)    #using the egcd algortihm, the list of s,t and r are generated for (n,b), such that n*s[i] + b*t[i] = r[i]
    kPrimes.sort(reverse=True)          #sorting the kPrimes list in descending order
    P = G(1)                            #P, as defined above

    for i in range(0,l):
        P = P*kPrimes[i]                #calculting P
    
    r,t = M * P, P                      # r,t - r*,t* from the Reed-Solomon algorithm
    
    
    i = binary_search(r_list,r)         #searching for the smallest index 'i' in r_list, such that r_list[i]<r*, r = r'
    
    if(r_list[i]%t_list[i]==0):         #checking whether the message is constructed properly or not
        a = r_list[i]/t_list[i]
        print(f'Message received - {a}')
    else:
        print("Couldn't reconstruct the message")

    



#helper functions:


#finds the maximum value product of 'u*count' number of primes from the list kPrimes (u-fraction of error, count - present number of primes in the list, u*count - present max number of corrupted residues)
def maxProd(count):
    global kPrimes,u
    kPrimes.sort(reverse = True)    #sorting the list in descending order
    prod = 1
    l = gmpy2.rint_floor(u*count)
    l = G(int(l))

    for i in range(0,l):
        prod = prod*kPrimes[i]
    return prod


#finding the ith bit in the binary representation of n
def bit(n,i):  
    n1 =n>>i
    n2 = n>>(i+1)
    bi = n1 - 2*n2
    return bi


#repeatd squaring algorithm
def power(a,n):   
    p = 1
    for i in range(gmpy2.bit_length(n)):
        if bit(n,i) == 1:
            p = p*a
        a = gmpy2.square(a)
    return p


#converting an integer to a gmpy2 object
def G(x):        
    return gmpy2.mpz(str(int(x)))


#binary implementation of egcd of the numbers a and b
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


#finds the inverse af a number b (mod n)
def inverseModn(b,n):    
    g,s,t = bin_egcd(b,n)
    
    if b >= n:
        return s
    else:
        return t


#helper function for CRT - computates n (product of k primes) and n_i* (n/n_i) where i = 0 to k-1
def PreCompute(numbers):   
    sz = len(numbers)
    product=1
    for i in range(0,sz):
        product = product*numbers[i]
    partialProducts = []
    for i in range(0,sz):   
        partialProducts.append(product//numbers[i])
    return product,partialProducts



#implementation of the Chinese remainder theorem
def CRT(remainders,numbers):    #remainders - the list of a_i, numbers - list of n_i
    product,partialProducts = PreCompute(numbers)
    sz = len(numbers)
    a=0
    e=[]
    for i in range(0,sz):
        b_i = partialProducts[i]%numbers[i]
        t_i = inverseModn(b_i,numbers[i])
        e_i = (partialProducts[i]*t_i)
        e.append(e_i)
        a = a + e_i*remainders[i]
    a = a%product
    return a


#implementation of egcd algorithm, used in ReedSolomonReceive() to find the r' < r* (where r' is the largest value of r such that r<r*)
def egcd(a,b):   
    s,t,r=[],[],[]
    (a,b)=(G(max(int(a),int(b))),G(min(int(a),int(b))))
    prevx, x = G(1), G(0); prevy, y = G(0), G(1)
    s.append(prevx);t.append(prevy);r.append(a)
    while b:
        s.append(x);t.append(y);r.append(b)
        quo,rem = gmpy2.t_divmod(a,b)
        x,prevx = prevx - quo*x, x
        y, prevy = prevy - quo*y, y
        a, b = b, rem
    if a>=b:
        return s,t,r
    else:
        return t,s,r


#returns the number of primes less than M
def count_primes(M):
    count = G(0)
    for num in range(2,M):
        if gmpy2.is_prime(num):
            count += 1
    return count


#uses the binary search technique to find the greatest value less than the target in the array
def binary_search(arr, target):
    low = G(0)
    high = G(len(arr) - 1)

    while low <= high:
        mid = G((low + high) // 2)
        if arr[mid] < target:
            high = mid-1
        else:
            low = mid + 1
    
    if high >= G(0):
            return high+1
    else:
        return G(0)



#driver code

def Reed():
    global u,M
    u = str(input("Error fraction- "))
    M = str(input("Bound- "))
    u = gmpy2.mpfr(u)
    M= G(M)
    GlobalSetup(u,M)
    while(1):
        a = str(input("Enter the number to transmit- "))
        residues = ReedSolomonSend(a)                       #generating the residues a_i corresponding to message 'a'
        residuesRecieved,l = Transmit(residues)             #generating the residues b_i that the receiver receives
        ReedSolomonRecieve(residuesRecieved,l)              #constructing the message

Reed()