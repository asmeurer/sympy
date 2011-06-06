"Experimental F5(B)"

"""
Signature = (monomial, index) where monomial is a monomial as in monomialtools, NOT A TERM!

Labeled Polynomial = (signature, polynomial, number) where polynomial is a sdp, number an integer.

"""

from sympy.polys.groebnertools import *

# convenience functions

def Sign(f):
    return f[0]

def Polyn(f):
    return f[1]

def Num(f):
    return f[2]

# signature functions

def sig(monomial, index):
    return (monomial, index)

def sig_cmp(u, v, O):
    """
    Compare two signatures via extension of the order on K[X] to
    K[X]^n

    (u < v)
    """
    if u[1] > v[1]:
        return -1
    if u[1] == v[1]:
        if u[0] == v[0]:
            return 0
        if cmp(O(u[0]), O(v[0])) < 0: 
            return -1
    return 1        

def sig_mult(s, m):
    """
    Multiply a signature by a monomial
    """
    return sig(monomial_mul(s[0], m), s[1])

def _term_rr_div(a, b, K):
    """Division of two terms in over a ring. """
    a_lm, a_lc = a
    b_lm, b_lc = b

    monom = monomial_div(a_lm, b_lm)

    if not (monom is None or a_lc % b_lc):
        return monom, K.exquo(a_lc, b_lc)
    else:
        return None

def _term_ff_div(a, b, K):
    """Division of two terms in over a field. """
    a_lm, a_lc = a
    b_lm, b_lc = b

    monom = monomial_div(a_lm, b_lm)

    if monom is not None:
        return monom, K.exquo(a_lc, b_lc)
    else:
        return None


# labeled polynomial functions

def lbp(signature, polynomial, number):
    return (signature, sdp_strip(polynomial), number)

def lbp_add(f, g, u, O, K):
    if sig_cmp(Sign(f), Sign(g), O) == -1:
        max_poly = g
    else:
        max_poly = f

    ret = sdp_add(Polyn(f), Polyn(g), u, O, K)

    return lbp(Sign(max_poly), ret, Num(max_poly))

def lbp_sub(f, g, u, O, K):
    """
    Subtract g from f
    """
    if sig_cmp(Sign(f), Sign(g), O) == -1:
        max_poly = g
    else:
        max_poly = f

    ret = sdp_sub(Polyn(f), Polyn(g), u, O, K)

    return lbp(Sign(max_poly), ret, Num(max_poly))

def lbp_mul_term(f, cx, u, O, K):
    """
    Multiply a labeled polynomial with a term
    """ 
    return lbp(sig_mult(Sign(f), cx[0]), sdp_mul_term(Polyn(f), cx, u, O, K), Num(f))

def lbp_cmp(f, g, O):
    """
    Compare two labeled polynomials. Attention: This relation is not antisymmetric!
    
    (f < g)
    """
    if sig_cmp(Sign(f), Sign(g), O) == -1:
        return -1
    if Sign(f) == Sign(g):
        if Num(f) > Num(g):
            return -1
        if Num(f) == Num(g):
            return 0
    return 1

# algorithm and helper functions

def critical_pair(f, g, u, O, K):
    ltf = sdp_LT(Polyn(f), u, K)
    ltg = sdp_LT(Polyn(g), u, K)
    lt = (monomial_lcm(ltf[0], ltg[0]), K.one)

    if K.has_Field:
        term_div = _term_ff_div
    else:
        term_div = _term_rr_div

    um = term_div(lt, ltf, K)
    vm = term_div(lt, ltg, K)

    fr = lbp_mul_term(lbp(Sign(f), [sdp_LT(Polyn(f), u, K)], Num(f)), um, u, O, K)
    gr = lbp_mul_term(lbp(Sign(g), [sdp_LT(Polyn(g), u, K)], Num(g)), vm, u, O, K)

    if lbp_cmp(fr, gr, O) == -1:
        return (Sign(gr), vm, g, Sign(fr), um, f)
    else:
        return (Sign(fr), um, f, Sign(gr), vm, g)

def cp_cmp(c, d, O):
    c0 = lbp(c[0], [], Num(c[2]))
    d0 = lbp(d[0], [], Num(d[2]))

    if lbp_cmp(c0, d0, O) == -1:
        return -1
    if lbp_cmp(c0, d0, O) == 0:
        c1 = lbp(c[3], [], Num(c[5]))
        d1 = lbp(d[3], [], Num(d[5]))

        if lbp_cmp(c1, d1, O) == -1:
            return -1
        if lbp_cmp(c1, d1, O) == 0:
            return 0
    return 1

def s_poly(cp, u, O, K):
    return lbp_sub(lbp_mul_term(cp[2], cp[1], u, O, K), lbp_mul_term(cp[5], cp[4], u, O, K), u, O, K)





def is_comparable(f, B, u, K):
    for g in B:
        if Sign(f)[1] < Sign(g)[1]:
            if monomial_div(Sign(f)[0], sdp_LM(Polyn(g), u)) is not None:
                return True
    return False

def is_rewritable(f, B, u, K):
    for g in B:
        if Sign(f)[1] == Sign(g)[1]:
            if Num(f) < Num(g):
                if monomial_div(Sign(f)[0], Sign(g)[0]) is not None:
                    return True
    return False

def is_rewritable_or_comparable(f, B, u, K):
    for h in B:
        if Sign(f)[1] < Sign(h)[1]:
            if monomial_div(Sign(f)[0], sdp_LM(Polyn(h), u)) is not None:
                return True        
        if Sign(f)[1] == Sign(h)[1]:
            if Num(f) < Num(h):
                if monomial_div(Sign(f)[0], Sign(h)[0]) is not None:
                    return True
    return False
            

def f5_single_reduction(f, B, u, O, K):
    if Polyn(f) == []:
        return f

    if K.has_Field:
        term_div = _term_ff_div
    else:
        term_div = _term_rr_div

    for g in B:
        if Polyn(g) != []:
            t = term_div(sdp_LT(Polyn(f), u, K), sdp_LT(Polyn(g), u, K), K)
            if t is not None:
                gp = lbp_mul_term(g, t, u, O, K)
                if sig_cmp(Sign(gp), Sign(f), O) == -1:
                    #if not is_rewritable_or_comparable(gp, B, u, K):
                    return lbp_sub(f, gp, u, O, K)
    return f

def f5_reduce(f, B, u, O, K):
    if Polyn(f) == []:
        return f

    while True:
        g = f
        f = f5_single_reduction(f, B, u, O, K)
        if g == f:
            return f

def f5b(F, u, O, K, gens='', verbose = False):
    """
    Experimental F5(B)
    """
   
    if not K.has_Field:
        raise DomainError("can't compute a Groebner basis over %s" % K)

    # reduce polynomials (like in mario pernici's algorithm) (Becker, Weispfennig, p. 203)
    B = F

    while True:
        F = B
        B = []

        for i in xrange(len(F)):
            p = F[i]
            r = sdp_rem(p, F[:i], u, O, K)

            if r != []:
                B.append(r)
        
        if F == B:
            break

    B = [lbp(sig((0,) * (u + 1), i + 1), F[i], i + 1) for i in xrange(len(F))]
    CP = [critical_pair(B[i], B[j], u, O, K) for i in xrange(len(B)) for j in xrange(i+1, len(B))]

    k = len(B)

    reductions_to_zero = 0

    while len(CP):
        cp = CP.pop()

        uf = lbp(cp[0], [], Num(cp[2]))
        vg = lbp(cp[3], [], Num(cp[5]))

        if is_rewritable_or_comparable(uf, B, u, K):
            continue
        if is_rewritable_or_comparable(vg, B, u, K):
            continue

        s = s_poly(cp, u, O, K)

        p = f5_reduce(s, B, u, O, K)

        p = lbp(Sign(p), Polyn(p), k + 1)

        if Polyn(p) != []:
            CP.extend([critical_pair(p, q, u, O, K) for q in B if Polyn(q) != []])
            CP.sort(lambda c, d: cp_cmp(c, d, O), reverse = True) 

            B.append(p)
            #B.sort(lambda x, y: lbp_cmp(x, y, O), reverse = True)
            #B = sorted(B, key = lambda f: O(sdp_LM(Polyn(f), u)), reverse = True)
            B.sort(key = lambda f: O(sdp_LM(Polyn(f), u)), reverse = True)
            k += 1
            
            # remove useless critical pairs
            indices = []
            for i, cp in enumerate(CP):
                if is_rewritable_or_comparable(lbp(cp[0], [], Num(cp[2])), [p], u, K):
                    indices.append(i)
                elif is_rewritable_or_comparable(lbp(cp[3], [], Num(cp[5])), [p], u, K):
                    indices.append(i)
            for i in reversed(indices):
                del CP[i]

            print(len(B), len(CP), "%d critical pairs removed" % len(indices))
        else:
            reductions_to_zero += 1

    print("reduction")

    # reduce   
    F = [sdp_strip(sdp_monic(Polyn(g), K)) for g in B]
    F = [f for f in F if f != []]
    F.sort(key = lambda f: O(sdp_LM(f, u)), reverse = False) # in order to compute katsura5
    H = []
    for i, f in enumerate(F):
        print(i)
        if f != []:
            f = sdp_rem(f, H + F[i + 1:], u, O, K)
            if f != []:
                H.append(f)

    # test
    #for i in xrange(len(H)):
    #    for j in xrange(i + 1, len(H)):
    #        s = sdp_spoly(H[i], H[j], u, O, K)
    #        s = sdp_rem(s, H, u, O, K)
    #        if s != []:
    #            print(s)
    
    #print("%d reductions to zero" % reductions_to_zero)
    
    return sorted(H, key = lambda f: O(sdp_LM(f, u)), reverse = True)

def sdp_spoly(p1, p2, u, O, K):
    """
    Compute LCM(LM(p1), LM(p2))/LM(p1)*p1 - LCM(LM(p1), LM(p2))/LM(p2)*p2
    """
    LM1 = sdp_LM(p1, u)
    LM2 = sdp_LM(p2, u)
    LCM12 = monomial_lcm(LM1, LM2)
    m1 = monomial_div(LCM12, LM1)
    m2 = monomial_div(LCM12, LM2)
    s1 = sdp_mul_term(p1, (m1, K.one), u, O, K)
    s2 = sdp_mul_term(p2, (m2, K.one), u, O, K)
    s = sdp_sub(s1, s2, u, O, K)
    return s

