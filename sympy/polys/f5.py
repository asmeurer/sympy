"Experimental F5(B)"

"""
A signature is a tuple (monomial, index). monomial is not a term!

A labeled polynomial is a tuple (signature, polynomial, number)
"""

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
        return True
    if u[1] == v[1]:
        if cmp(O(u[0]), O(v[0])) < 0: # having > was the bug all along...
            return True
    return False            

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
    if sig_cmp(Sign(f), Sign(g), O):
        max_poly = g
    else:
        max_poly = f

    ret = sdp_add(Polyn(f), Polyn(g), u, O, K)

    return lbp(Sign(max_poly), ret, Num(max_poly))

def lbp_sub(f, g, u, O, K):
    """
    Subtract g from f
    """
    if sig_cmp(Sign(f), Sign(g), O):
        max_poly = g
    else:
        max_poly = f

    ret = sdp_sub(Polyn(f), Polyn(g), u, O, K)

    return lbp(Sign(max_poly), ret, Num(max_poly))

def lbp_mult(f, cx, u, O, K):
    """
    Multiply a labeled polynomial with a term
    """ 
    return lbp(sig_mult(Sign(f), cx[0]), sdp_mul_term(Polyn(f), cx, u, O, K), Num(f))


# algorithm and helper functions

def critical_pair(f, g, u, O, K):
    lmf = sdp_LM(Polyn(f), u)
    lmg = sdp_LM(Polyn(g), u)
    lm = monomial_lcm(lmf, lmg)

    um = monomial_div(lm, lmf)
    vm = monomial_div(lm, lmg)

    return (um, f, vm, g)

def s_poly(cp, u, O, K):
    # might not work with rings that aren't fields atm
    
    uf = lbp_mult(cp[1], (cp[0], sdp_LC(Polyn(cp[3]), K)), u, O, K)
    vg = lbp_mult(cp[3], (cp[2], sdp_LC(Polyn(cp[1]), K)), u, O, K)

    return lbp_sub(uf, vg, u, O, K)


def is_comparable(f, B, K):
    for g in B:
        if monomial_div(Sign(g)[0], Sign(f)[0]) is not None:
            if Sign(f)[1] < Sign(g)[1]:
                return True
    return False

def is_rewritable(f, B, K):
    for g in B:
        if Sign(f)[1] == Sign(g)[1]:
            if Num(f) < Num(g):
                if monomial_div(Sign(g)[0], Sign(f)[0]) is not None:
                    return True
    return False

def f5_reduce(f, B, u, O, K):
    #if Polyn(f) != []:
    #    for g in B:
    #        t = monomial_div(sdp_LM(Polyn(f), u), sdp_LM(Polyn(g), u))
    #        if t is not None:
    #            c = sdp_LC(Polyn(f), K) / sdp_LC(Polyn(g), K)
    #            gp = lbp_mult(g, (t, c), u, O, K)
    #            if sig_cmp(Sign(gp), Sign(f), O):
    #                if not is_comparable(gp, B, K):
    #                    if not is_rewritable(gp, B, K):
    #                        return lbp_sub(f, gp, u, O, K)
    #return None
    
    if K.has_Field:
        term_div = _term_ff_div
    else:
        term_div = _term_rr_div

    if Polyn(f) == []:
        return f

    #reducible = True

    while True: #reducible:
        #reducible = False
        for g in B:
            if Polyn(g) != []:
                #t = monomial_div(sdp_LM(Polyn(f), u), sdp_LM(Polyn(g), u))
                t = term_div(sdp_LT(Polyn(f), u, K), sdp_LT(Polyn(g), u, K), K)
                if t is not None:
                    #c = sdp_LC(Polyn(f), K) / sdp_LC(Polyn(g), K)
                    gp = lbp_mult(g, t, u, O, K)
                    if sig_cmp(Sign(gp), Sign(f), O):
                        if not is_comparable(gp, B, K):
                            if not is_rewritable(gp, B, K):
                                #print(sdp_str(Polyn(f), "x,y"), "lt: ", sdp_str([sdp_LT(Polyn(f), u, K)], "x,y"))
                                #print(sdp_str(Polyn(gp), "x,y"), "lt: ", sdp_str([sdp_LT(Polyn(gp), u, K)],"x,y"))
                                f = lbp_sub(f, gp, u, O, K)
                                #print(sdp_str(Polyn(f), "x,y"))
                                #raw_input("next")
                                #reducible = True
                                break
        # for ... else: execute else iff for is terminated without calling break
        else:
            break
    return f
            

def f5b(F, u, O, K, gens='', verbose = False):
    """
    Experimental F5(B)
    """
   
    if not K.has_Field:
        raise DomainError("can't compute a Groebner basis over %s" % K)

    B = [lbp(sig((0,) * (u + 1), i), F[i], i) for i in xrange(len(F))] # i from 0 to n-1 should work. in the paper it's 1 to n, though.
    CP = [critical_pair(B[i], B[j], u, O, K) for i in xrange(len(B)) for j in xrange(i+1, len(B))]

    k = len(B)

    while CP:
        cp = CP.pop()
        #print(len(CP))

        uf = lbp_mult(cp[1], (cp[0], K.one), u, O, K)
        vg = lbp_mult(cp[3], (cp[2], K.one), u, O, K)

        if is_comparable(uf, B, K):
            continue
        if is_comparable(vg, B, K):
            continue
        if is_rewritable(uf, B, K):
            continue
        if is_rewritable(vg, B, K):
            continue


        s = s_poly(cp, u, O, K)
        print(sdp_str(Polyn(s),"x,y,z"))



        #p = s

        #while s:
        #    p = s
        #    s = f5_reduce(s, B, u, O, K)
        #    if s == None or Polyn(s) == []:
        #       break
        #        print(p)
        p = f5_reduce(s, B, u, O, K)
        print(sdp_str(Polyn(p), "x,y,z"))


        #if Polyn(p) != []:
            #print(sdp_str(Polyn(p), "x,y")) # debug

        p = lbp(Sign(p), Polyn(p), k)

        if Polyn(p) != []: # [], why not K.zero?
            CP.extend([critical_pair(p, q, u, O, K) for q in B])

            # these should be outside the "if". Why?!
            # addendum: not only that, it won't work if it's inside the "if".
        B.append(p)
        k += 1
        #print("appended", k)

    # reduce   
    F = [sdp_strip(sdp_monic(Polyn(g), K)) for g in B]
    #F = [f for f in F if f != []]
    #H = []
    #for i, f in enumerate(F):
    #    if f != []:
            #print(f)
            #print(H + F[i:])
    #        f = sdp_rem(f, H + F[i + 1:], u, O, K)
            #print(f)
            #print("--")
    #        H.append(f)

    #print("\n\n")
    # test
    #for i in xrange(len(H)):
    #    for j in xrange(i + 1, len(H)):
    #        s = sdp_spoly(H[i], H[j], u, O, K)
    #        print(sdp_rem(s, H, u, O, K))
    

    return F #H

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

