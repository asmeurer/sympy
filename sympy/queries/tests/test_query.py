from sympy.core import Symbol, symbols, S, Rational, Integer
from sympy.functions import exp, log, sin, cos, sign, re, im
from sympy.assumptions import Assume
from sympy.queries import query, register_handler, remove_handler
from sympy.queries.handlers import QueryHandler
from sympy.utilities.pytest import raises, XFAIL

def test_int_1():
    z = 1
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == True
    assert query(z, rational=True)         == True
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == False
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == True
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == True

def test_float_1():
    z = 1.0
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == True
    assert query(z, rational=True)         == True
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == False
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == True
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == True

def test_zero_0():
    z = Integer(0)
    assert query(z, zero=True)             == True
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == True
    assert query(z, rational=True)         == True
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == False
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == True
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == True
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

def test_negativeone():
    z = Integer(-1)
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == True
    assert query(z, rational=True)         == True
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == False
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == False
    assert query(z, negative=True)         == True
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == True
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

def test_infinity():
    oo = S.Infinity
    assert query(oo, commutative=True)     == True
    assert query(oo, integer=True)         == False
    assert query(oo, rational=True)        == False
    assert query(oo, real=True)            == False
    assert query(oo, extended_real=True)   == True
    assert query(oo, complex=True)         == False
    assert query(oo, irrational=True)      == False
    assert query(oo, imaginary=True)       == False
    assert query(oo, positive=True)        == True
    assert query(oo, negative=True)        == False
    assert query(oo, even=True)            == False
    assert query(oo, odd=True)             == False
    assert query(oo, bounded=True)         == False
    assert query(oo, infinitesimal=True)   == False
    assert query(oo, comparable=True)      == True
    assert query(oo, prime=True)           == False
    assert query(oo, composite=True)       == False

def test_neg_infinity():
    mm = S.NegativeInfinity
    assert query(mm, commutative=True)    == True
    assert query(mm, integer=True)        == False
    assert query(mm, rational=True)       == False
    assert query(mm, real=True)           == False
    assert query(mm, extended_real=True)  == True
    assert query(mm, complex=True)        == False
    assert query(mm, irrational=True)     == False
    assert query(mm, imaginary=True)      == False
    assert query(mm, positive=True)       == False
    assert query(mm, negative=True)       == True
    assert query(mm, even=True)           == False
    assert query(mm, odd=True)            == False
    assert query(mm, bounded=True)        == False
    assert query(mm, infinitesimal=True)  == False
    assert query(mm, comparable=True)     == True
    assert query(mm, prime=True)          == False
    assert query(mm, composite=True)      == False

def test_nan():
    nan = S.NaN
    assert query(nan, commutative=True)   == True
    assert query(nan, integer=True)       == False
    assert query(nan, rational=True)      == False
    assert query(nan, real=True)          == False
    assert query(nan, extended_real=True) == False
    assert query(nan, complex=True)       == False
    assert query(nan, irrational=True)    == False
    assert query(nan, imaginary=True)     == False
    assert query(nan, positive=True)      == False
    assert query(nan, zero=True)          == False
    assert query(nan, even=True)          == False
    assert query(nan, odd=True)           == False
    assert query(nan, bounded=True)       == False
    assert query(nan, infinitesimal=True) == False
    assert query(nan, comparable=True)    == False
    assert query(nan, prime=True)         == False
    assert query(nan, composite=True)     == False

def test_Rational_number():
    r = Rational(3,4)
    assert query(r, commutative=True)      == True
    assert query(r, integer=True)          == False
    assert query(r, rational=True)         == True
    assert query(r, real=True)             == True
    assert query(r, complex=True)          == True
    assert query(r, irrational=True)       == False
    assert query(r, imaginary=True)        == False
    assert query(r, positive=True)         == True
    assert query(r, negative=True)         == False
    assert query(r, even=True)             == False
    assert query(r, odd=True)              == False
    assert query(r, bounded=True)          == True
    assert query(r, infinitesimal=True)    == False
    assert query(r, comparable=True)       == True
    assert query(r, prime=True)            == False
    assert query(r, composite=True)        == False

    r = Rational(1,4)
    assert query(r, positive=True)         == True
    assert query(r, negative=True)         == False

    r = Rational(5,4)
    assert query(r, negative=True)         == False
    assert query(r, positive=True)         == True

    r = Rational(5,3)
    assert query(r, positive=True)         == True
    assert query(r, negative=True)         == False

    r = Rational(-3,4)
    assert query(r, positive=True)         == False
    assert query(r, negative=True)         == True

    r = Rational(-1,4)
    assert query(r, positive=True)         == False
    assert query(r, negative=True)         == True

    r = Rational(-5,4)
    assert query(r, negative=True)         == True
    assert query(r, positive=True)         == False

    r = Rational(-5,3)
    assert query(r, positive=True)         == False
    assert query(r, negative=True)         == True

def test_pi():
    z = S.Pi
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == True
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

    z = S.Pi + 1
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == True
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

    z = 2*S.Pi
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == True
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

    z = S.Pi ** 2
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == True
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

    z = (1+S.Pi) ** 2
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == True
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

def test_E():
    z = S.Exp1
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == True
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == True
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == True
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, comparable=True)       == True
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

def test_I():
    z = S.ImaginaryUnit
    assert query(z, comparable=True)       == False
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == False
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == False
    assert query(z, imaginary=True)        == True
    assert query(z, positive=True)         == False
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

    z = 1 + S.ImaginaryUnit
    assert query(z, comparable=True)       == False
    assert query(z, commutative=True)      == True
    assert query(z, integer=True)          == False
    assert query(z, rational=True)         == False
    assert query(z, real=True)             == False
    assert query(z, complex=True)          == True
    assert query(z, irrational=True)       == False
    assert query(z, imaginary=True)        == False
    assert query(z, positive=True)         == False
    assert query(z, negative=True)         == False
    assert query(z, even=True)             == False
    assert query(z, odd=True)              == False
    assert query(z, bounded=True)          == True
    assert query(z, infinitesimal=True)    == False
    assert query(z, prime=True)            == False
    assert query(z, composite=True)        == False

def test_bounded():
    x, y = symbols('xy')
    assert query(x, bounded=True) == False
    assert query(x, bounded=False) == True
    assert query(x, bounded=True, assumptions=Assume(x, bounded=True)) == True
    assert query(x, bounded=True, assumptions=Assume(y, bounded=True)) == False
    assert query(x, bounded=True, assumptions=Assume(x, complex=True)) == False
    assert query(x, bounded=True, assumptions=Assume(x, zero=True)) == True
    assert query(x + 1, bounded=True) == False
    assert query(x + 1, bounded=True, assumptions=Assume(x, bounded=True)) == True
    assert query(x + y, bounded=True) == None
    assert query(x + y, bounded=True, assumptions=Assume(x, bounded=True)) == False
    assert query(x + 1, bounded=True, assumptions=[Assume(x, bounded=True), \
                Assume(y, bounded=True)]) == True
    assert query(2 * x, bounded=True) == False
    assert query(2 * x, bounded=True, assumptions=Assume(x, bounded=True)) == True
    assert query(x * y, bounded=True) == None
    assert query(x * y, bounded=True, assumptions=Assume(x, bounded=True)) == False
    assert query(x * y, bounded=True, assumptions=[Assume(x, bounded=True), \
                Assume(y, bounded=True)]) == True
    assert query(x ** 2, bounded=True) == False
    assert query(2 ** x, bounded=True) == False
    assert query(2 ** x, bounded=True, assumptions=Assume(x, bounded=True)) == True
    assert query(x ** x, bounded=True) == False
    assert query(Rational(1,2) ** x, bounded=True) == True
    assert query(x ** Rational(1,2), bounded=True) == False

    # sign function
    assert query(sign(x), bounded=True) == True
    assert query(sign(x), bounded=True, assumptions=Assume(x, bounded=False)) == True

    # exponential functions
    assert query(log(x), bounded=True) == False
    assert query(log(x), bounded=True, assumptions=Assume(x, bounded=True)) == True
    assert query(exp(x), bounded=True) == False
    assert query(exp(x), bounded=True, assumptions=Assume(x, bounded=True)) == True
    assert query(exp(2), bounded=True) == True

    # trigonometric functions
    assert query(sin(x), bounded=True) == True
    assert query(sin(x), bounded=True, assumptions=Assume(x, bounded=False)) == True
    assert query(cos(x), bounded=True) == True
    assert query(cos(x), bounded=True, assumptions=Assume(x, bounded=False)) == True
    assert query(2*sin(x), bounded=True) == True
    assert query(sin(x)**2, bounded=True) == True
    assert query(cos(x)**2, bounded=True) == True
    assert query(cos(x) + sin(x), bounded=True) == True

@XFAIL
def test_bounded_xfail():
    """We need to support relations in query for this to work"""
    x = Symbol('x')
    assert query(sin(x)**x, bounded=True) == True
    assert query(cos(x)**x, bounded=True) == True
    assert query(sin(x) ** x, bounded=True) == True

def test_commutative():
    """By default objects are commutative that is why it returns True
    for both key=True and key=False"""
    x, y = symbols('xy')
    assert query(x, commutative=True) == True
    assert query(x, commutative=False) == False
    assert query(x, commutative=True, assumptions=Assume(x, commutative=False)) == False
    assert query(x, commutative=True, assumptions=Assume(x, complex=True))      == True
    assert query(x, commutative=True, assumptions=Assume(x, imaginary=True))    == True
    assert query(x, commutative=True, assumptions=Assume(x, real=True))         == True
    assert query(x, commutative=True, assumptions=Assume(x, positive=True))     == True
    assert query(x, commutative=True, assumptions=Assume(y, commutative=False))  == True

    assert query(2*x, commutative=True ) == True
    assert query(2*x, commutative=True, assumptions=Assume(x, commutative=False)) == False

    assert query(x + 1, commutative=True ) == True
    assert query(x + 1, commutative=True, assumptions=Assume(x, commutative=False)) == False

    assert query(x**2, commutative=True) == True
    assert query(x**2, commutative=True, assumptions=Assume(x, commutative=False)) == False

    assert query(log(x), commutative=True) == True

def test_comparable():
    x, y = symbols('x y')
    assert query(x, comparable=True) == None
    assert query(x, comparable=True, assumptions=Assume(x, real=True)) == True
    assert query(x, comparable=True, assumptions=Assume(x, complex=True)) == None

    assert query(x*y, comparable=True, assumptions=Assume(x, comparable=True) & Assume(y, comparable=True))

def test_complex():
    x, y = symbols('xy')
    assert query(x, complex=True) == None
    assert query(x, complex=False) == None
    assert query(x, complex=True, assumptions=Assume(x, complex=True)) == True
    assert query(x, complex=True, assumptions=Assume(y, complex=True)) == None
    assert query(x, complex=True, assumptions=Assume(x, complex=False)) == False
    assert query(x, complex=True, assumptions=Assume(x, real=True)) == True
    assert query(x, complex=True, assumptions=Assume(x, real=False)) == None
    assert query(x, complex=True, assumptions=Assume(x, rational=True)) == True
    assert query(x, complex=True, assumptions=Assume(x, irrational=True)) == True
    assert query(x, complex=True, assumptions=Assume(x, zero=True)) == True
    assert query(x, complex=True, assumptions=Assume(x, zero=False)) == None
    assert query(x, complex=True, assumptions=Assume(x, positive=True)) == True
    assert query(x, complex=True, assumptions=Assume(x, imaginary=True)) == True

    # a+b
    assert query(x+1, complex=True, assumptions=Assume(x, complex=True)) == True
    assert query(x+1, complex=True, assumptions=Assume(x, real=True)) == True
    assert query(x+1, complex=True, assumptions=Assume(x, rational=True)) == True
    assert query(x+1, complex=True, assumptions=Assume(x, irrational=True)) == True
    assert query(x+1, complex=True, assumptions=Assume(x, imaginary=True)) == True
    assert query(x+1, complex=True, assumptions=Assume(x, integer=True))  == True
    assert query(x+1, complex=True, assumptions=Assume(x, even=True))  == True
    assert query(x+1, complex=True, assumptions=Assume(x, odd=True))  == True
    assert query(x+y, complex=True, assumptions=Assume(x, complex=True) & \
                     Assume(y, complex=True)) == True
    assert query(x+y, complex=True, assumptions=Assume(x, real=True) & \
                     Assume(y, imaginary=True)) == True

    # a*x +b
    assert query(2*x+1, complex=True, assumptions=Assume(x, complex=True)) == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, real=True)) == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, positive=True)) == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, rational=True)) == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, irrational=True)) == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, imaginary=True)) == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, integer=True))  == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, even=True))  == True
    assert query(2*x+1, complex=True, assumptions=Assume(x, odd=True))  == True

    # x**2
    assert query(x**2, complex=True, assumptions=Assume(x, complex=True)) == True
    assert query(x**2, complex=True, assumptions=Assume(x, real=True)) == True
    assert query(x**2, complex=True, assumptions=Assume(x, positive=True)) == True
    assert query(x**2, complex=True, assumptions=Assume(x, rational=True)) == True
    assert query(x**2, complex=True, assumptions=Assume(x, irrational=True)) == True
    assert query(x**2, complex=True, assumptions=Assume(x, imaginary=True)) == True
    assert query(x**2, complex=True, assumptions=Assume(x, integer=True))  == True
    assert query(x**2, complex=True, assumptions=Assume(x, even=True))  == True
    assert query(x**2, complex=True, assumptions=Assume(x, odd=True))  == True

    # 2**x
    assert query(2**x, complex=True, assumptions=Assume(x, complex=True)) == True
    assert query(2**x, complex=True, assumptions=Assume(x, real=True)) == True
    assert query(2**x, complex=True, assumptions=Assume(x, positive=True)) == True
    assert query(2**x, complex=True, assumptions=Assume(x, rational=True)) == True
    assert query(2**x, complex=True, assumptions=Assume(x, irrational=True)) == True
    assert query(2**x, complex=True, assumptions=Assume(x, imaginary=True)) == True
    assert query(2**x, complex=True, assumptions=Assume(x, integer=True))  == True
    assert query(2**x, complex=True, assumptions=Assume(x, even=True))  == True
    assert query(2**x, complex=True, assumptions=Assume(x, odd=True))  == True
    assert query(x**y, complex=True, assumptions=Assume(x, complex=True) & \
                     Assumptions(y, complex=True)) == True

    # trigonometric expressions
    assert query(sin(x), complex=True) == True
    assert query(sin(2*x + 1), complex=True) == True
    assert query(cos(x), complex=True) == True
    assert query(cos(2*x+1), complex=True) == True

    # exponential
    assert query(exp(x), complex=True) == True
    assert query(exp(x), complex=True) == True

    # complexes
    assert query(abs(x), complex=True) == True
    assert query(re(x),  complex=True) == True
    assert query(im(x),  complex=True) == True

def test_even():
    x, y, z, t = symbols('x y z t')
    assert query(x, even=True) == None
    assert query(x, even=True, assumptions=Assume(x, integer=True)) == None
    assert query(x, even=True, assumptions=Assume(x, integer=False)) == False
    assert query(x, even=True, assumptions=Assume(x, rational=True)) == None
    assert query(x, even=True, assumptions=Assume(x, positive=True)) == None

    assert query(2*x, even=True) == None
    assert query(2*x, even=True, assumptions=Assume(x, integer=True)) == True
    assert query(2*x, even=True, assumptions=Assume(x, even=True)) == True
    assert query(2*x, even=True, assumptions=Assume(x, irrational=True)) == False
    assert query(2*x, even=True, assumptions=Assume(x, odd=True)) == True
    assert query(2*x, even=True, assumptions=Assume(x, integer=False)) == None
    assert query(3*x, even=True, assumptions=Assume(x, integer=True)) == None
    assert query(3*x, even=True, assumptions=Assume(x, even=True)) == True
    assert query(3*x, even=True, assumptions=Assume(x, odd=True)) == False

    assert query(x+1, even=True, assumptions=Assume(x, odd=True)) == True
    assert query(x+1, even=True, assumptions=Assume(x, even=True)) == False
    assert query(x+2, even=True, assumptions=Assume(x, odd=True)) == False
    assert query(x+2, even=True, assumptions=Assume(x, even=True)) == True
    assert query(7-x, even=True, assumptions=Assume(x, odd=True)) == True
    assert query(7+x, even=True, assumptions=Assume(x, odd=True)) == True
    assert query(x+y, even=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True)) == True
    assert query(x+y, even=True, assumptions=Assume(x, odd=True) & Assume(y, even=True)) == False
    assert query(x+y, even=True, assumptions=Assume(x, even=True) & Assume(y, even=True)) == True

    assert query(2*x + 1, even=True, assumptions=Assume(x, integer=True)) == False
    assert query(2*x*y, even=True, assumptions=Assume(x, rational=True) & Assume(x, rational=True)) == None
    assert query(2*x*y, even=True, assumptions=Assume(x, irrational=True) & Assume(x, irrational=True)) == None

    assert query(x+y+z, even=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True) & \
                     Assume(z, even=True)) == True
    assert query(x+y+z+t, even=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True) & \
                     Assume(z, even=True) & Assume(t, integer=True)) == None

    assert query(abs(x), even=True, assumptions=Assume(x, even=True)) == True
    assert query(abs(x), even=True, assumptions=Assume(x, even=False)) == None
    assert query(re(x),  even=True, assumptions=Assume(x, even=True)) == True
    assert query(re(x),  even=True, assumptions=Assume(x, even=False)) == None
    assert query(im(x),  even=True, assumptions=Assume(x, even=True)) == True
    assert query(im(x),  even=True, assumptions=Assume(x, real=True)) == True

def test_extended_real():
    x = symbols('x')
    assert query(x, extended_real=True, assumptions=Assume(x, positive=True)) == True
    assert query(-x, extended_real=True, assumptions=Assume(x, positive=True)) == True
    assert query(-x, extended_real=True, assumptions=Assume(x, negative=True)) == True

def test_rational():
    x, y = symbols('xy')
    assert query(x, rational=True, assumptions=Assume(x, zero=True)) == True
    assert query(x, rational=True, assumptions=Assume(x, integer=True)) == True
    assert query(x, rational=True, assumptions=Assume(x, irrational=True)) == False
    assert query(x, rational=True, assumptions=Assume(x, real=True)) == None
    assert query(x, rational=True, assumptions=Assume(x, positive=True)) == None
    assert query(x, rational=True, assumptions=Assume(x, negative=True)) == None
    assert query(x, rational=True, assumptions=Assume(x, nonzero=True)) == None

    assert query(2*x, rational=True, assumptions=Assume(x, rational=True)) == True
    assert query(2*x, rational=True, assumptions=Assume(x, integer=True)) == True
    assert query(2*x, rational=True, assumptions=Assume(x, even=True)) == True
    assert query(2*x, rational=True, assumptions=Assume(x, odd=True)) == True
    assert query(2*x, rational=True, assumptions=Assume(x, irrational=True)) == False

    assert query(x/2, rational=True, assumptions=Assume(x, rational=True)) == True
    assert query(x/2, rational=True, assumptions=Assume(x, integer=True)) == True
    assert query(x/2, rational=True, assumptions=Assume(x, even=True)) == True
    assert query(x/2, rational=True, assumptions=Assume(x, odd=True)) == True
    assert query(x/2, rational=True, assumptions=Assume(x, irrational=True)) == False

    assert query(1/x, rational=True, assumptions=Assume(x, rational=True)) == True
    assert query(1/x, rational=True, assumptions=Assume(x, integer=True)) == True
    assert query(1/x, rational=True, assumptions=Assume(x, even=True)) == True
    assert query(1/x, rational=True, assumptions=Assume(x, odd=True)) == True
    assert query(1/x, rational=True, assumptions=Assume(x, irrational=True)) == False

    assert query(2/x, rational=True, assumptions=Assume(x, rational=True)) == True
    assert query(2/x, rational=True, assumptions=Assume(x, integer=True)) == True
    assert query(2/x, rational=True, assumptions=Assume(x, even=True)) == True
    assert query(2/x, rational=True, assumptions=Assume(x, odd=True)) == True
    assert query(2/x, rational=True, assumptions=Assume(x, irrational=True)) == False

    # with multiple symbols
    assert query(x*y, rational=True, assumptions=[Assume(x, irrational=True), \
        Assume(y, irrational=True)]) == None
    assert query(y/x, rational=True, assumptions=[Assume(x, rational=True), \
        Assume(y, rational=True)]) == True
    assert query(y/x, rational=True, assumptions=[Assume(x, integer=True), \
        Assume(y, rational=True)]) == True
    assert query(y/x, rational=True, assumptions=[Assume(x, even=True), \
        Assume(y, rational=True)]) == True
    assert query(y/x, rational=True, assumptions=[Assume(x, odd=True), \
        Assume(y, rational=True)]) == True
    assert query(y/x, rational=True, assumptions=[Assume(x, irrational=True), \
        Assume(y, rational=True)]) == False

def test_imaginary():
    x, y, z = symbols('x y z')
    I = S.ImaginaryUnit
    assert query(x, imaginary=True) == None
    assert query(x, imaginary=True, assumptions=Assume(x, real=True)) == False
    assert query(x, imaginary=True, assumptions=Assume(x, prime=True)) == False

    assert query(x+1, imaginary=True, assumptions=Assume(x, real=True)) == False
    assert query(x+1, imaginary=True, assumptions=Assume(x, imaginary=True)) == False
    assert query(x+I, imaginary=True, assumptions=Assume(x, real=True)) == False
    assert query(x+I, imaginary=True, assumptions=Assume(x, imaginary=True)) == True
    assert query(x+y, imaginary=True, assumptions=Assume(x, imaginary=True) & \
                     Assume(y, imaginary=True)) == True
    assert query(x+y, imaginary=True, assumptions=Assume(x, real=True) & \
                     Assume(y, real=True)) == False
    assert query(x+y, imaginary=True, assumptions=Assume(x, imaginary=True) & \
                     Assume(y, real=True)) == False
    assert query(x+y, imaginary=True, assumptions=Assume(x, complex=True) & \
                     Assume(y, real=True)) == None

    assert query(I*x, imaginary=True, assumptions=Assume(x, real=True)) == True
    assert query(I*x, imaginary=True, assumptions=Assume(x, imaginary=True)) == False
    assert query(I*x, imaginary=True, assumptions=Assume(x, complex=True)) == None
    assert query(x*y, imaginary=True, assumptions=Assume(x, imaginary=True) & 
                 Assume(y, real=True)) == True

    assert query(x+y+z, imaginary=True, assumptions=Assume(x, real=True) & \
                     Assume(y, real=True) & Assume(z, real=True)) == False
    assert query(x+y+z, imaginary=True, assumptions=Assume(x, real=True) & \
                     Assume(y, real=True) & Assume(z, imaginary=True)) == None
    assert query(x+y+z, imaginary=True, assumptions=Assume(x, real=True) & \
                     Assume(y, imaginary=True) & Assume(z, imaginary=True)) == False

def test_integer():
    x = symbols('x')
    assert query(x, integer=True) == None
    assert query(x, integer=True, assumptions=Assume(x, integer=True)) == True
    assert query(x, integer=True, assumptions=Assume(x, integer=False)) == False
    assert query(x, integer=True, assumptions=Assume(x, real=False)) == False
    assert query(x, integer=True, assumptions=Assume(x, positive=False)) == None

    assert query(2*x, integer=True, assumptions=Assume(x, integer=True)) == True
    assert query(2*x, integer=True, assumptions=Assume(x, even=True)) == True
    assert query(2*x, integer=True, assumptions=Assume(x, prime=True)) == True
    assert query(2*x, integer=True, assumptions=Assume(x, rational=True)) == None
    assert query(2*x, integer=True, assumptions=Assume(x, real=True)) == None

    assert query(x/2, integer=True, assumptions=Assume(x, odd=True)) == False
    assert query(x/2, integer=True, assumptions=Assume(x, even=True)) == True
    assert query(x/3, integer=True, assumptions=Assume(x, odd=True)) == None
    assert query(x/3, integer=True, assumptions=Assume(x, even=True)) == False

def test_negative():
    x, y = symbols('xy')
    assert query(x, negative=True, assumptions=Assume(x, negative=True)) == True
    assert query(x, negative=True, assumptions=Assume(x, positive=True)) == False
    assert query(x, negative=True, assumptions=Assume(x, real=False)) == False
    assert query(x, negative=True, assumptions=Assume(x, prime=True)) == False
    assert query(x, negative=True, assumptions=Assume(x, prime=False)) == None

    assert query(-x, negative=True, assumptions=Assume(x, positive=True)) == True
    assert query(-x, negative=True, assumptions=Assume(x, positive=False)) == None
    assert query(-x, negative=True, assumptions=Assume(x, negative=True)) == False
    assert query(-x, negative=True, assumptions=Assume(x, positive=True)) == True

    assert query(x-1, negative=True, assumptions=Assume(x, negative=True)) == True

    assert query(x+y, negative=True, assumptions=[Assume(x, negative=True), Assume(y, negative=True)]) == True

def test_nonzero():
    x = Symbol('x')
    def nonzero(expr, assumptions=[]):
        return query(expr, real=True, assumptions=assumptions) and \
            query(expr, zero=False, assumptions=assumptions)
    assert nonzero(x) == None
    assert nonzero(x, assumptions=Assume(x, real=True) & Assume(x, zero=False))== True
    assert nonzero(x, assumptions=Assume(x, zero=True)) == False
    assert nonzero( x, assumptions=Assume(x, positive=True)) == True
    assert nonzero(2*x, assumptions=Assume(x, positive=True)) == True

def test_odd():
    x, y, z, t = symbols('x y z t')
    assert query(x, odd=True) == None
    assert query(x, odd=True, assumptions=Assume(x, odd=True)) == True
    assert query(x, odd=True, assumptions=Assume(x, integer=True)) == None
    assert query(x, odd=True, assumptions=Assume(x, integer=False)) == False
    assert query(x, odd=True, assumptions=Assume(x, rational=True)) == None
    assert query(x, odd=True, assumptions=Assume(x, positive=True)) == None

    assert query(-x, odd=True, assumptions=Assume(x, odd=True)) == True

    assert query(2*x, odd=True) == None
    assert query(2*x, odd=True, assumptions=Assume(x, integer=True)) == False
    assert query(2*x, odd=True, assumptions=Assume(x, odd=True)) == False
    assert query(2*x, odd=True, assumptions=Assume(x, irrational=True)) == False
    assert query(2*x, odd=True, assumptions=Assume(x, integer=False)) == None
    assert query(3*x, odd=True, assumptions=Assume(x, integer=True)) == None

    assert query(x/3, odd=True, assumptions=Assume(x, odd=True)) == None
    assert query(x/3, odd=True, assumptions=Assume(x, even=True)) == None

    assert query(x+1, odd=True, assumptions=Assume(x, even=True)) == True
    assert query(x+2, odd=True, assumptions=Assume(x, even=True)) == False
    assert query(x+2, odd=True, assumptions=Assume(x, odd=True))  == True
    assert query(3-x, odd=True, assumptions=Assume(x, odd=True))  == False
    assert query(3-x, odd=True, assumptions=Assume(x, even=True))  == True
    assert query(3+x, odd=True, assumptions=Assume(x, odd=True))  == False
    assert query(3+x, odd=True, assumptions=Assume(x, even=True))  == True
    assert query(x+y, odd=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True)) == False
    assert query(x+y, odd=True, assumptions=Assume(x, odd=True) & Assume(y, even=True)) == True
    assert query(x-y, odd=True, assumptions=Assume(x, even=True) & Assume(y, odd=True)) == True
    assert query(x-y, odd=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True)) == False

    assert query(x+y+z, odd=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True) & \
                     Assume(z, even=True)) == False
    assert query(x+y+z+t, odd=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True) & \
                     Assume(z, even=True) & Assume(t, integer=True)) == None

    assert query(2*x + 1, odd=True, assumptions=Assume(x, integer=True)) == True
    assert query(2*x + y, odd=True, assumptions=Assume(x, integer=True) & Assume(y, odd=True)) == True
    assert query(2*x + y, odd=True, assumptions=Assume(x, integer=True) & Assume(y, even=True)) == False
    assert query(2*x + y, odd=True, assumptions=Assume(x, integer=True) & Assume(y, integer=True)) == None
    assert query(x*y,   odd=True, assumptions=Assume(x, odd=True) & Assume(y, even=True)) == False
    assert query(x*y,   odd=True, assumptions=Assume(x, odd=True) & Assume(y, odd=True)) == True
    assert query(2*x*y, odd=True, assumptions=Assume(x, rational=True) & Assume(x, rational=True)) == None
    assert query(2*x*y, odd=True, assumptions=Assume(x, irrational=True) & Assume(x, irrational=True)) == None

    assert query(abs(x), odd=True, assumptions=Assume(x, odd=True)) == True

def test_prime():
    x, y = symbols('x y')
    assert query(x, prime=True, assumptions=Assume(x, prime=True)) == True
    assert query(x, prime=True, assumptions=Assume(x, prime=False)) == False
    assert query(x, prime=True, assumptions=Assume(x, integer=True)) == None
    assert query(x, prime=True, assumptions=Assume(x, integer=False)) == False

    assert query(2*x, prime=True, assumptions=Assume(x, integer=True)) == False
    assert query(x*y, prime=True, assumptions=Assume(x, integer=True) &\
                     Assume(y, integer=True)) == False

    assert query(x**2, prime=True, assumptions=Assume(x, integer=True)) == False
    assert query(x**2, prime=True, assumptions=Assume(x, prime=True)) == False
    assert query(x**y, prime=True, assumptions=Assume(x, integer=True) &\
                     Assume(y, integer=True)) == False

def test_positive():
    x, y, z, w = symbols('xyzw')
    assert query(x, positive=True, assumptions=Assume(x, positive=True)) == True
    assert query(x, positive=True, assumptions=Assume(x, negative=True)) == False
    assert query(x, positive=True, assumptions=Assume(x, zero=True)) == False
    assert query(x, positive=True, assumptions=Assume(x, nonnegative=True)) == None
    assert query(x, positive=True, assumptions=Assume(x, nonnegative=False)) == None

    assert query(-x, positive=True, assumptions=Assume(x, positive=True)) == False
    assert query(-x, positive=True, assumptions=Assume(x, negative=True)) == True
    assert query(y+z,   negative=True,      assumptions=assumptions) == True
    assert query(x+y,   positive=True,      assumptions=assumptions) == None
    assert query(x+y,   negative=True,      assumptions=assumptions) == None

    assert query(2*x,  positive=True, assumptions=Assume(x, positive=True)) == True
    assumptions =  Assume(x, positive=True) & Assume(y, negative=True) & \
                    Assume(z, negative=True) & Assume(w, positive=True)
    assert query(x*y*z,  positive=True)  == None
    assert query(x*y*z,  positive=True,      assumptions=assumptions) == True
    assert query(-x*y*z, positive=True,      assumptions=assumptions) == False

    assert query(x**2, positive=True, assumptions=Assume(x, positive=True)) == True
    assert query(x**2, positive=True, assumptions=Assume(x, negative=True)) == True
    assert query(x**2, positive=True, assumptions=Assume(x, nonnegative=True)) == None # could be 0

    #exponential
    assert query(exp(x),     positive=True, assumptions=Assume(x, real=True)) == True
    assert query(x + exp(x), positive=True, assumptions=Assume(x, real=True)) == None

    #absolute value
    assert query(abs(x), positive=True) == None # abs(0) = 0
    assert query(abs(x), positive=True, assumptions=Assume(x, positive=True)) == True

@XFAIL
def test_positive_xfail():
    assert query(1/(1 + x**2), positive=True, assumptions=Assume(x, real=True)) == True

def test_real():
    x = Symbol('x')
    assert query(x, real=True) == None
    assert query(x, real=True, assumptions=Assume(x, real=True)) == True
    assert query(x, real=True, assumptions=Assume(x, zero=True)) == True
    assert query(x, real=True, assumptions=Assume(x, zero=False) & Assume(x, real=True)) == True
    assert query(x, real=True, assumptions=Assume(x, positive=True)) == True
    assert query(x, real=True, assumptions=Assume(x, negative=True)) == True
    assert query(x, real=True, assumptions=Assume(x, negative=True) | Assume(x, zero=True)) == True
    assert query(x, real=True, assumptions=Assume(x, positive=True) | Assume(x, zero=True)) == True
    assert query(x, real=True, assumptions=Assume(x, integer=True)) == True
    assert query(x, real=True, assumptions=Assume(x, even=True)) == True
    assert query(x, real=True, assumptions=Assume(x, prime=True)) == True

    from sympy import sqrt
    assert query(x/sqrt(2), real=True, assumptions=Assume(x, real=True)) == True
    assert query(x/sqrt(-2), real=True, assumptions=Assume(x, real=True)) == False

    I = S.ImaginaryUnit
    assert query(x+1, real=True, assumptions=Assume(x, real=True)) == True
    assert query(x+I, real=True, assumptions=Assume(x, real=True)) == False
    assert query(x+I, real=True, assumptions=Assume(x, complex=True)) == None

    assert query(2*x, real=True, assumptions=Assume(x, real=True)) == True
    assert query(I*x, real=True, assumptions=Assume(x, real=True)) == False
    assert query(I*x, real=True, assumptions=Assume(x, imaginary=True)) == True
    assert query(I*x, real=True, assumptions=Assume(x, complex=True)) == None

    assert query(x**2,  real=True, assumptions=Assume(x, real=True)) == True
    assert query(x**x,  real=True, assumptions=Assume(x, real=True)) == True

    # trigonometric functions
    assert query(sin(x), real=True) == None
    assert query(cos(x), real=True) == None
    assert query(sin(x), real=True, assumptions=Assume(x, real=True)) == True
    assert query(cos(x), real=True, assumptions=Assume(x, real=True)) == True

    # exponential function
    assert query(exp(x), real=True) == None
    assert query(exp(x), real=True, assumptions=Assume(x, real=True)) == True
    assert query(x + exp(x), real=True, assumptions=Assume(x, real=True)) == True

    # complexes
    assert query(re(x), real=True) == True
    assert query(im(x), real=True) == True

def test_zero():
    x, y = symbols('xy')
    assert query(x, zero=True) == None
    assert query(x, zero=True, assumptions=Assume(x, positive=True)) == False
    assert query(x, zero=True, assumptions=Assume(x, negative=True)) == False

    assert query(x+y, zero=True) == None
    assert query(x+y, zero=True, assumptions=Assume(x, positive=True) & Assume(y, positive=True)) == False
    assert query(x+y, zero=True, assumptions=Assume(x, positive=True) & Assume(y, negative=True)) == None
    assert query(x+y, zero=True, assumptions=Assume(x, negative=True) & Assume(y, negative=True)) == False

    assert query(2*x, zero=True) == None
    assert query(2*x, zero=True, assumptions=Assume(x, positive=True)) == False
    assert query(2*x, zero=True, assumptions=Assume(x, negative=True)) == False
    assert query(x*y, zero=True, assumptions=Assume(x, zero=False)) == None
    assert query(x*y, zero=True, assumptions=Assume(x, zero=False) & Assume(y, zero=False)) == False

    assert query(abs(x), zero=True) == None
    assert query(abs(x), zero=True, assumptions=Assume(x, zero=False)) == False


def test_hash_vs_eq():
    """catch: different hash for equal objects"""
    a = 1 + S.Pi    # important: do not fold it into a Number instance
    ha= hash(a)     #            it should be Add/Mul/... to trigger the bug
    b = a.expand(trig=True)
    hb= hash(b)

    assert query(a, positive=True) == True   # this uses .evalf() and deduces it is positive
    # be sure that hash stayed the same
    assert a == b
    assert ha == hash(a)
    assert ha== hb

def test_global():
    """Test query with global assumptions"""
    import sympy.assumptions as assumptions
    x = symbols('x')
    assert query(x, integer=True) == None
    assumptions.register_global(Assume(x, integer=True))
    assert query(x, integer=True) == True
    assumptions.remove_global(Assume(x, integer=True))
    assert query(x, integer=True) == None

def test_key_extensibility():
    """test that you can add keys to the query system at runtime"""
    x = Symbol('x')
    raises(KeyError, "query(x, my_key=True)") # make sure this is not defined beforehand
    class MyQueryHandler(QueryHandler):
        @staticmethod
        def Symbol(expr, assumptions):
            return True
    register_handler('my_key', MyQueryHandler)
    assert query(x, my_key=True) == True
    assert query(x+1, my_key=True) == None
    remove_handler('my_key', MyQueryHandler)

def test_type_extensibility():
    """test that new types can be added to the query system at runtime
    We create a custom type MyType, and override query prime=True with handler
    MyQueryHandler for this type

    TODO: test incompatible resolutors
    """
    from sympy.core import Basic

    class MyType(Basic):
        pass

    class MyQueryHandler(QueryHandler):
        @staticmethod
        def MyType(expr, assumptions):
            return True

    a = MyType()
    register_handler('prime', MyQueryHandler)
    assert query(a, prime=True) == True
