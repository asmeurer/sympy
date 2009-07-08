from sympy import symbols, Assume, exp, pi, Rational, I
from sympy.refine import refine
from sympy.utilities.pytest import XFAIL

def test_abs():
    x = symbols('x')
    assert refine(abs(x), Assume(x, positive=True)) == x
    assert refine(1+abs(x), Assume(x, positive=True)) == 1+x
    assert refine(abs(x), Assume(x, negative=True)) == -x
    assert refine(1+abs(x), Assume(x, negative=True)) == 1-x

@XFAIL
def test_pow():
    x = symbols('x')
    assert refine((-1)**x, Assume(x, even=True)) == 1
    assert refine((-1)**x, Assume(x, odd=True)) == -1

def test_exp():
    x = symbols('x')
    assert refine(exp(pi*I*2*x), Assume(x, integer=True)) == 1
    assert refine(exp(pi*I*2*(x+Rational(1,2))), Assume(x, integer=True)) == -1
    assert refine(exp(pi*I*2*(x+Rational(1,4))), Assume(x, integer=True)) == I
    assert refine(exp(pi*I*2*(x+Rational(3,4))), Assume(x, integer=True)) == -I
