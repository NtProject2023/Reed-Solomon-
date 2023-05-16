import gmpy2

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

def inverseModn(b,n):
    g,s,t = gmpy2.gcdext(b,n)
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
