from sympy import Constant, sin, exp, Function, Wild, Symbol, S, Pow

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
C = Constant('C', x)
C0 = Constant('C0', x, y)
C1 = Constant('C1', x, z)
C2 = Constant('C2', y, z)
f = Function('f')

def test_constant_mul():
    # We want C (Constant) below to absorb the y's, but not the x's
    assert C.name == 'C'
    assert C.args == (x,)
    assert y*C == C
    assert x*C == x*Constant('C', x)
    assert C*y == C
    assert C*x == x*Constant('C', x)
    assert 2*C == C
    assert C*2 == C
    assert y*C*x == C*x
    assert x*y*C == x*C
    assert y*x*C == x*C
    assert C*y*(y+1) == C
    assert y*C*(y+1) == C
    assert x*(y*C) == x*C
    assert x*(C*y) == x*C
    assert C*(x*y) == C*x
    assert (x*y)*C == x*C
    assert (y*x)*C == x*C
    assert y*(y+1)*C == C
    assert C*x*y == C*x
    assert x*C*y == x*C
    assert (C*x)*y == C*x
    assert y*(x*C) == x*C
    assert (x*C)*y == x*C
    assert C0*x*y*z == C0*x*y
    assert C0*x*y**2*sin(z) == C0*x*y**2
    assert C0*C1 == Constant('C0', x, y, z)
    assert C1*C0 == Constant('C1', x, y, z)
    assert (C1*C0).args == (x, y, z)
    assert (C0*C1).args == (x, y, z)
    assert C1.name == 'C1'
    assert C1*C1 == Constant('C1', x, z)
    assert C0*C1*C2 == Constant('C0', x, y, z)
    assert C*x*2**x != C*x

def test_constant_add():
    assert C+C == C
    assert C+2 == C
    assert 2+C == C
    assert C+y == C
    assert C+x == Constant('C', x) + x
    assert C+x+y+x*y+2 == C+x+x*y
    assert C+x+2**x+y+2 == C+x+2**x

def test_constant_power_as_base():
    assert C**C == C
    assert Pow(C,C) == C
    assert C0**C1 == Constant('C0', x, y, z)
    assert C1**C0 == Constant('C1', x, y, z)
    assert C**y == C
    assert C**x == Constant('C', x)**x
    assert C**2 == C
    assert C**(x*y) == Constant('C', x)**(x*y)

def test_constant_power_as_exp():
    assert x**C == x**Constant('C', x)
    assert y**C == C
    assert x**y**C == x**C
    assert (x**y)**C == (x**y)**Constant('C', x)
    assert x**(y**C) == x**C
    assert x**C**y == x**C
    assert x**(C**y) == x**C
    assert (x**C)**y == (x**Constant('C', x))**y
    assert 2**C == C
    assert S(2)**C == C
    assert exp(C) == C
    assert exp(C+x) == exp(C+x)
    assert Pow(2, C) == C

def test_constant_function():
    assert C.as_coefficient(C) == None
    assert sin(C) == C
    assert f(C) == C
    assert f(C, C1), f(C, C1) == Constant('C', x, z)
    assert f(C, x), f(C, x) == f(Constant('C', x), x)
    assert f(C, C1, x) == f(Constant('C', x), Constant('C1', x, z), x)
    assert f(C, y) == C
    assert f(C, C1, y), f(C, C1, y) == Constant('C', x, z)

