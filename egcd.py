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

print(egcd(8,5))

