import time
from math import ceil, copysign

class ModularCplx(complex):
    def __init__(self, num = 0, n = None):
        print(num)
        num = complex(num)
        self.num = complex.__call__((int(num.real) % n), (int(num.imag) % n))
        print((int(num.real) % n),(int(num.imag) % n))
    
    def __mod__(self, n):
        return ModularCplx(self, n)

def timeit(*deps):
    def timeit_(func):
        def wrap(*args, **kwargs):
            st = time.time()
            val = func(*args, **kwargs)
            et = time.time()
            print('timer',func.__name__,(et-st),abs(sum([args[v] for v in deps])), (et-st)/abs(sum([args[v] for v in deps])))
            return val
        return wrap
    return timeit_

@timeit(0)
def cplx_factor(q):
    factors = []
    r = int(abs(q)/2)+1
    for a in range(0, r):
        for b in range(1 if a == complex(0) else 0, r):
            p = q / complex(a, b)
            if p.real % 1 == 0 and p.imag % 1 == 0:
                factors.append(p)

#@timeit(0,1)
def cplx_div(p, q):
    low = 0
    low_v = None
    n = ceil(abs(p) / abs(q) + 1) + 1
    for a in range(-n, n):
        loc_low = 0
        loc_low_v = None
        pivot = False
        for b in range(-n, n):
            if a == b == 0:
                break
            r = complex(a, b)
            if abs(q * r) <= abs(p):
                v = abs(q * r - p)
                if q * r == p:
                    return r
                if not low_v:
                        low = r
                        low_v = v
                if not loc_low_v:
                    loc_low = r
                    loc_low_v = v
                if v < loc_low_v:
                    pivot = True
                    loc_low_v = v
                    loc_low = r
                elif pivot:
                    break
        if loc_low_v and \
           loc_low_v < low_v:
            low = loc_low
            low_v = loc_low_v
    return low

@timeit(0)
def perf_cplx_div(p, q):
    '''Based on the assumption that p, q are Gaussian Integers'''
    z = p / q
    r = z.real
    s = z.imag
    m = r // 1 # m such that abs(r - m) <= 1/2
    n = s // 1 # n such that abs(s - n) <= 1/2
    zeta = complex(m, n)
    delta = p - zeta*q
    return zeta

def perf_cplx_mod(p, q):
    '''Based on the assumption that p, q are Gaussian Integers'''
    z = p / q
    r = z.real
    s = z.imag
    m = r // 1 # m such that abs(r - m) <= 1/2
    n = s // 1 # n such that abs(s - n) <= 1/2
    zeta = complex(m, n)
    delta = p - zeta*q
    return delta


def cplx_mod(p, q):
    r = p - q * cplx_div(p, q)
    if abs(r) > abs(q):
        r = r - q * cplx_div(r, q)
    while (copysign(r.real, r.real*q.real) < 0) != (copysign(r.imag, r.imag*q.imag) < 0):
        print(r)
        r += q
    return r

def cplx_euclid(a, b):
    '''Solve x*a + y*b = ggt(a, b) and return (x, y, ggt(a, b))'''
    # Non-recursive approach hence suitable for large numbers
    x = yy = 0
    y = xx = 1
    while b != 0:
        q = perf_cplx_div(a, b)
        a, b = b, perf_cplx_mod(a, b)
        x, xx = xx - q * x, x
        y, yy = yy - q * y, y
    return xx, yy, a

def cplx_inv(a, n):
    '''Perform inversion 1/a modulo n. a and n should be COPRIME.'''
    # coprimality is not checked here in favour of performance
    i = perf_cplx_mod(cplx_euclid(a, n)[0], n)
    while i.real < 0:
        i += n
    tmp = 0
    return i

def test_div(n=20):
    for a in range(n):
        for b in range(0 if a != 0 else 1, n):
            z = complex(a,b)
            for c in range(a, n):
                for d in range(b, n):
                    perf_cplx_div(complex(c,d), z)

def test(z, n):
    r = cplx_inv(z, n)
    return abs(perf_cplx_mod(r * z, n)) == 1, perf_cplx_mod(r * z, n)

if __name__ == '__main__':
    pass;
