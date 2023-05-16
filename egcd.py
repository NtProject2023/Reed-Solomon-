import gmpy2


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
    return gmpy2.mpz(str(x));

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
    if(s<0):
        s = s+n
    return s

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
        b_i = gmpy2.f_mod(partialProducts[i],numbers[i])
        t_i = inverseModn(b_i,numbers[i])
        # print(b_i,numbers[i],t_i)
        e_i = gmpy2.f_mod(partialProducts[i]*t_i,product)
        a = gmpy2.add(a,e_i*remainders[i])
    a = gmpy2.f_mod(a,product)
    return a

num = [3,4,5]
rem = [2,3,1]

print(CRT(rem,num));        

def egcd(a,b):
    s,t,r=[],[],[]
    (a,b)=(max(int(a),int(b)),min(int(a),int(b)))
    # print(a,b)
    prevx, x = 1, 0; prevy, y = 0, 1
    s.append(prevx);t.append(prevy);r.append(a)
    while b:
        s.append(x);t.append(y);r.append(b)
        quo,rem = gmpy2.t_divmod(a,b)
        x,prevx = prevx - quo*x, x
        y, prevy = prevy - quo*y, y
        a, b = b, rem
    return s,t,r

print(egcd(280,480))