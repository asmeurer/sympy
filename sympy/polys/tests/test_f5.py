"""Tests for sparse distributed polynomials and Groebner bases. """

from sympy.polys.groebnertools import (
    sdp_LC, sdp_LM, sdp_LT, sdp_del_LT,
    sdp_coeffs, sdp_monoms,
    sdp_sort, sdp_strip, sdp_normal,
    sdp_from_dict, sdp_to_dict,
    sdp_indep_p, sdp_one_p, sdp_one, sdp_term_p,
    sdp_abs, sdp_neg,
    sdp_add_term, sdp_sub_term, sdp_mul_term,
    sdp_add, sdp_sub, sdp_mul, sdp_sqr, sdp_pow,
    sdp_monic, sdp_content, sdp_primitive,
    _term_rr_div, _term_ff_div,
    sdp_div, sdp_quo, sdp_rem,
    sdp_lcm, sdp_gcd,
    sdp_groebner,
)

###
from sympy.polys.f5 import *

from sympy.polys.polytools import (
    parallel_poly_from_expr,
)
###

from sympy.polys.monomialtools import (
    monomial_lex_key as O_lex,
    monomial_grlex_key as O_grlex,
    monomial_grevlex_key as O_grevlex,
)

from sympy.polys.polyerrors import (
    ExactQuotientFailed, DomainError,
)

from sympy.polys.domains import ZZ, QQ

from sympy import S, Symbol, symbols, groebner

from sympy.utilities.pytest import raises, skip, XFAIL

#def test_sdp_LC():
#    assert sdp_LC([], QQ) == QQ(0)
#    assert sdp_LC([((1,0), QQ(1,2))], QQ) == QQ(1,2)
#    assert sdp_LC([((1,1), QQ(1,4)), ((1,0), QQ(1,2))], QQ) == QQ(1,4)

def test_sig_cmp():
    a = ((1, 0, 0), 0)
    b = ((2, 0, 0), 1)
    assert sig_cmp(a, b, O_lex) == False

    b = ((2, 0, 0), 0)
    assert sig_cmp(a, b, O_lex) == True

    b = ((1, 0, 0), 0)
    assert sig_cmp(a, b, O_lex) == False

def test_sig_mult():
    a = ((1, 1, 1), 1)
    m = (0, 2, 1)
    assert sig_mult(a, m) == ((1, 3, 2), 1)

    m = (0, 0, 0)
    assert sig_mult(a, m) == a

def test_lbp_add():
    x, y, z = symbols("x:3")
    L = [x**2*y*z+z**2, x**3 + x + y + z]
    L.append(L[0] + L[1])
    polys, opt = parallel_poly_from_expr(L, x, y, z, order="lex")
    
    for i, poly in enumerate(polys):
        poly = poly.set_domain(opt.domain).rep.to_dict()
        polys[i] = sdp_from_dict(poly, opt.order)

    f = lbp(sig((0, 1, 0), 1), polys[0], 0)
    g = lbp(sig((1, 0, 0), 1), polys[1], 1)
    add = lbp(sig((1, 0, 0), 1), polys[2], 1)

    assert lbp_add(f, g, 2, O_lex, QQ) == add

def test_lbp_sub():
    x, y, z = symbols("x:3")
    L = [x**2*y*z+z**2, x**3 + x + y + z]
    L.append(L[0] - L[1])
    polys, opt = parallel_poly_from_expr(L, x, y, z, order="lex")
    
    for i, poly in enumerate(polys):
        poly = poly.set_domain(opt.domain).rep.to_dict()
        polys[i] = sdp_from_dict(poly, opt.order)

    f = lbp(sig((0, 1, 0), 1), polys[0], 0)
    g = lbp(sig((1, 0, 0), 1), polys[1], 1)
    sub = lbp(sig((1, 0, 0), 1), polys[2], 1)

    assert lbp_sub(f, g, 2, O_lex, QQ) == sub

    
