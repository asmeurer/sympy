from sympy.core import Rational, Symbol, Basic, S, Real, Integer
from sympy.functions.elementary.miscellaneous import sqrt

def test_rational():
    a = Rational(1, 5)

    assert a**Rational(1, 2) == a**Rational(1, 2)
    assert 2 * a**Rational(1, 2) == 2 * a**Rational(1, 2)

    assert a**Rational(3, 2) == a * a**Rational(1, 2)
    assert 2 * a**Rational(3, 2) == 2*a * a**Rational(1, 2)

    assert a**Rational(17, 3) == a**5 * a**Rational(2, 3)
    assert 2 * a**Rational(17, 3) == 2*a**5 * a**Rational(2, 3)

def test_large_rational():
    e = (Rational(123712**12-1,7)+Rational(1,7))**Rational(1,3)
    assert e == 234232585392159195136 * (Rational(1,7)**Rational(1,3))

def test_negative_real():
    def feq(a,b):
        return abs(a - b) < 1E-10

    assert feq(S.One / Real(-0.5), -Integer(2))

def test_expand():
    x = Symbol('x')
    assert (2**(-1-x)).expand() == Rational(1,2)*2**(-x)

def test_issue153():
    #test that is runs:
    a = sqrt(2*(1+sqrt(2)))

def test_issue350():
    #test if powers are simplified correctly
    #see also issue 896
    a = Symbol('a')
    assert ((a**Rational(1,3))**Rational(2)) == a**Rational(2,3)
    assert ((a**Rational(3))**Rational(2,5)) == (a**Rational(3))**Rational(2,5)

    a = Symbol('a', real=True)
    b = Symbol('b', real=True)
    assert (a**2)**b == abs(a)**(2*b)
    assert sqrt(1/a) != 1/sqrt(a)
    assert (a**3)**Rational(1,3) != a

    z = Symbol('z')
    k = Symbol('k',integer=True)
    m = Symbol('m',integer=True)
    assert (z**k)**m == z**(k*m)
    #assert Number(5)**Rational(2,3)==Number(25)**Rational(1,3)

    a = Symbol('a', positive=True)
    assert (a**3)**Rational(2,5) == a**Rational(6,5)

def test_issue767():
    assert --sqrt(sqrt(5)-1)==sqrt(sqrt(5)-1)

def test_negative_one():
    x = Symbol('x', complex=True)
    y = Symbol('y', complex=True)
    assert 1/x**y == x**(-y)

def test_issue1263():
    neg = Symbol('neg', negative=True)
    nonneg = Symbol('nonneg', negative=False)
    any = Symbol('any')
    num, den = sqrt(1/nonneg).as_numer_denom()
    assert num == 1
    assert den == sqrt(nonneg)
    num, den = sqrt(1/any).as_numer_denom()
    assert num == sqrt(1/any)
    assert den == 1

    def eqn(num, den, pow):
        return (num/den)**pow
    npos=1
    nneg=-1
    dpos=2-sqrt(3)
    dneg=1-sqrt(3)
    I = S.ImaginaryUnit
    assert dpos > 0 and dneg < 0 and npos > 0 and nneg < 0
    # pos or neg integer
    eq=eqn(npos, dpos, 2);assert eq.is_Pow and eq.as_numer_denom() == (1, dpos**2)
    eq=eqn(npos, dneg, 2);assert eq.is_Pow and eq.as_numer_denom() == (1, dneg**2)
    eq=eqn(nneg, dpos, 2);assert eq.is_Pow and eq.as_numer_denom() == (1, dpos**2)
    eq=eqn(nneg, dneg, 2);assert eq.is_Pow and eq.as_numer_denom() == (1, dneg**2)
    eq=eqn(npos, dpos, -2);assert eq.is_Pow and eq.as_numer_denom() == (dpos**2, 1)
    eq=eqn(npos, dneg, -2);assert eq.is_Pow and eq.as_numer_denom() == (dneg**2, 1)
    eq=eqn(nneg, dpos, -2);assert eq.is_Pow and eq.as_numer_denom() == (dpos**2, 1)
    eq=eqn(nneg, dneg, -2);assert eq.is_Pow and eq.as_numer_denom() == (dneg**2, 1)
    eq=eqn(npos, dpos, S.Half);assert eq.is_Pow and eq.as_numer_denom() == (npos**S.Half, dpos**S.Half)
    eq=eqn(npos, dneg, S.Half);assert eq.is_Pow and eq.as_numer_denom() == (-npos**S.Half, dneg**S.Half)
    #eq=eqn(nneg, dpos, S.Half);assert eq.is_Pow and eq.as_numer_denom() == (I, dpos**S.Half)
    eq=eqn(nneg, dneg, S.Half);assert eq.is_Pow and eq.as_numer_denom() == (I, dneg**S.Half)
    eq=eqn(npos, dpos, -S.Half);assert eq.is_Pow and eq.as_numer_denom() == (dpos**S.Half, 1)
    eq=eqn(npos, dneg, -S.Half);assert eq.is_Pow and eq.as_numer_denom() == (-dneg**S.Half, 1)
    #eq=eqn(nneg, dpos, -S.Half);assert eq.is_Pow and eq.as_numer_denom() == (dpos**S.Half, I)
    eq=eqn(nneg, dneg, -S.Half);assert eq.is_Pow and eq.as_numer_denom() == (dneg**S.Half, I)
    eq=eqn(npos, dpos, 2*any);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)
    eq=eqn(npos, dneg, 2*any);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)
    eq=eqn(nneg, dpos, 2*any);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)
    eq=eqn(nneg, dneg, 2*any);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)
    eq=eqn(npos, dpos, S(1)/3);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)
    eq=eqn(npos, dneg, S(1)/3);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)
    #eq=eqn(nneg, dpos, S(1)/3);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)
    eq=eqn(nneg, dneg, S(1)/3);assert eq.is_Pow and eq.as_numer_denom() == (eq, 1)

def test_eval_power():
    '''
    var('x  w y z')
    n1,n2,n3=[Symbol(s,negative=True) for s in 'n1 n2 n3'.split()]
    p1,p2,p3=[Symbol(s,negative=True) for s in 'p1 p2 p3'.split()]
    n4,n5,n6=[Symbol(s,negative=True) for s in 'n4 n5 n6'.split()]
    sqrt(3),sqrt(-3),sqrt(3*x),sqrt(-3*x)
    (3**(1/2), I*3**(1/2), 3**(1/2)*x**(1/2), 3**(1/2)*(-x)**(1/2))
    sqrt(n1*x),sqrt(-n1*x),sqrt(x*y)
    ((n1*x)**(1/2), (-n1*x)**(1/2), (x*y)**(1/2))
    sqrt(n1*n2*x),sqrt(-n1*n2*x)
    (-n1**(1/2)*n2**(1/2)*x**(1/2), -n1**(1/2)*n2**(1/2)*(-x)**(1/2))
    sqrt(n1*n2*n3*x),sqrt(-n1*n2*n3*x)
    (-n1**(1/2)*n2**(1/2)*(n3*x)**(1/2), -n1**(1/2)*n2**(1/2)*(-n3*x)**(1/2))
    sqrt(n1*n2*n3),sqrt(-n1*n2*n3)
    (-n1**(1/2)*n2**(1/2)*n3**(1/2), -n1**(1/2)*n2**(1/2)*(-n3)**(1/2))
    sqrt(n1*n2*n3*n4),sqrt(-n1*n2*n3*n4)
    (n1**(1/2)*n2**(1/2)*n3**(1/2)*n4**(1/2), n1**(1/2)*n2**(1/2)*n3**(1/2)*(-n4)**(
    1/2))
    sqrt(n1*n2*n3*n4*3),sqrt(-n1*n2*n3*n4*3)
    (3**(1/2)*n1**(1/2)*n2**(1/2)*n3**(1/2)*n4**(1/2), 3**(1/2)*n1**(1/2)*n2**(1/2)*
    n3**(1/2)*(-n4)**(1/2))
    >>> sqrt(x*n1*n2*n3*n4*3),sqrt(-n1*n2*n3*n4*3*x)
    (3**(1/2)*n1**(1/2)*n2**(1/2)*n3**(1/2)*n4**(1/2)*x**(1/2), 3**(1/2)*n1**(1/2)*n
    2**(1/2)*n3**(1/2)*n4**(1/2)*(-x)**(1/2))
    >>> sqrt(x*n1*n2*n3*n4*3*p1*p2),sqrt(-n1*n2*n3*n4*3*x*p1*p2)
    (-3**(1/2)*n1**(1/2)*n2**(1/2)*n3**(1/2)*n4**(1/2)*p1**(1/2)*p2**(1/2)*x**(1/2),
     -3**(1/2)*n1**(1/2)*n2**(1/2)*n3**(1/2)*n4**(1/2)*p1**(1/2)*p2**(1/2)*(-x)**(1/
    2))'''

def test_issue1496():
    x = Symbol('x')
    y = Symbol('y')
    n = Symbol('n', even=True)
    assert (3-y)**2 == (y-3)**2
    assert (3-y)**n == (y-3)**n
    assert (-3+y-x)**2 == (3-y+x)**2
    assert (y-3)**3 == -(3-y)**3

