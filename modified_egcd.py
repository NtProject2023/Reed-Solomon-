import gmpy2

def G(x):
    return gmpy2.mpz(str(x));

def bin_egcd(a,b):
    s,t,r = [],[],[]
    a,b=G(a),G(b)
    r1,r2 = max(a,b),min(a,b)
    e = G(0)
    while r1%2 == 0 and r2%2 == 0:
        r1,r2 = r1>>1,r2>>1
        e = e + 1
    
    x,y = r1,r2
    s1,s2 = G(1),G(0)
    t1,t2 = G(0),G(1)
    
    s.append(s1);t.append(t1);r.append(r1)
    
    while r2 != 0:
        while r1%2 == 0:
            r1 = r1>>1
            if s1%2 == G(0)  and t1%2 == G(0):
                s1,t1 = s1>>1,t1>>1
            else:
                s1,t1 = (s1+y)>>1,(t1-x)>>1
            if not (s[-1]==s1 and t[-1]==t1 and r[-1]==r1):
                s.append(s1);t.append(t1);r.append(r1)
        while r2%2 == 0:
            r2 = r2>>1
            if s2%2 == 0  and t2%2 == 0:
                s2,t2 = s2>>1,t2>>1
            else:
                s2,t2 = (s2+y)>>1,(t2-x)>>1
        if r1 > r2:
            r1,s1,t1,r2,s2,t2 = r2,s2,t2,r1,s1,t1
        r2,s2,t2 = (r2 - r1),(s2 - s1),(t2 - t1)
        if(r2==0):
            s.append(s1);t.append(t1);r.append(r1)
    print(s)
    print(t)
    print(r)
    # print(l);print(m);print(n)
    return power(2,e)*r1,s1,t1

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

print(bin_egcd(280,480))