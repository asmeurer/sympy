from sympy import Constant, sin, exp, Function, Wild, Symbol, S, Pow

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
A = Constant('A', x)
A2 = Constant('A2', x)
B1 = Constant('B1', x, y)
C1 = Constant('C1', x, z)
C2 = Constant('C2', x, z)
D2 = Constant('D2', y, z)
D3 = Constant('D3', y, z)
f = Function('f')

# B1 = B1
# C1 = C1
# D2 = D2
def test_constant_parameter():
    assert A.name == 'A'
    assert A.args == (x,)
    assert A.varname == 'A'
    assert C1.name == 'C1'
    assert A.number == '1'
    assert C1.number == '1'
    assert D2.number == '2'
    assert D2.varname == 'D'
    assert D3.increment_number() == Constant('D4', y, z)
    assert A.increment_number() == Constant('A2', x)
    assert A.increment_number(amount=2) == Constant('A3', x)
    assert A.increment_number(no_number_value=0) == Constant('A1', x)
    assert A.increment_number(amount=0, no_number_value=1) == Constant('A1', x)
    assert A.as_coefficient(C) == None

def test_constant_mul():
    # We want A (Constant) below to absorb the y's, but not the x's
    assert y*A == A2
    assert x*A == x*Constant('A', x)
    assert A*y == A2
    assert A*x == x*Constant('A', x)
    assert 2*A == A2
    assert A*2 == A2
    assert y*A*x == A2*x
    assert x*y*A == x*A2
    assert y*x*A == x*A2
    assert A*y*(y + 1) == A2
    assert y*A*(y + 1) == A2
    assert x*(y*A) == x*A2
    assert x*(A*y) == x*A2
    assert A*(x*y) == A2*x
    assert (x*y)*A == x*A2
    assert (y*x)*A == x*A2
    assert y*(y + 1)*A == A2
    assert A*x*y == A2*x
    assert x*A*y == x*A2
    assert (A*x)*y == A2*x
    assert y*(x*A) == x*A2
    assert (x*A)*y == x*A2
    assert A*x*y*x*y*2 == A2*x**2
    assert B1*x*y*z == B2*x*y
    assert B1*x*y**2*sin(z) == B2*x*y**2
    assert B1*C1 in (Constant('B2', x, y, z), Constant('C2', x, y, z))
    assert C1*B1 in (Constant('B2', x, y, z), Constant('C2', x, y, z))
    assert (C1*B1).args == (x, y, z)
    assert (B1*C1).args == (x, y, z)
    assert C1*C1 == Constant('C2', x, z)
    assert B1*C1*D2 == Constant('D3', x, y, z)
    assert C*x*2**x != C*x

def test_constant_add():
    assert A + A == A2
    assert A + 2 == A2
    assert 2 + A == A2
    assert A + y == A2
    assert A + x == Constant('A', x) + x
    assert A + x + y + x*y + 2 == A2 + x + x*y
    assert A + x + 2**x + y + 2 == A2 + x + 2**x
    assert B1 + C1 in (Constant('B2', x, y, z), Constant('C2', x, y, z)) 
    assert C1 + B1 in (Constant('B2', x, y, z), Constant('C2', x, y, z))
    assert B1 + D2 + C1 == Constant('D3', x, y, z)

def test_constant_power_as_base():
    assert A**A == A2
    assert Pow(A,A) == A2
    assert B1**C1 in (Constant('B2', x, y, z), Constant('C2', x, y, z))
    assert C1**B1 in (Constant('B2', x, y, z), Constant('C2', x, y, z))
    assert D2**C1 == Constant('D3', x, y, z)
    assert C1**D2 == Constant('D3', x, y, z)
    assert A**y == A2
    assert A**x == Constant('A', x)**x
    assert A**2 == A2
    assert A**(x*y) == Constant('A', x)**(x*y)

def test_constant_power_as_exp():
    assert x**A == x**Constant('A', x)
    assert y**A == A2
    assert x**y**A == x**A2
    assert (x**y)**A == (x**y)**Constant('A', x)
    assert x**(y**A) == x**A2
    assert x**A**y == x**A2
    assert x**(A**y) == x**A2
    assert (x**A)**y == (x**Constant('A', x))**y
    assert 2**A == A2
    assert S(2)**A == A2
    assert exp(A) == A2
    assert exp(A+x) == exp(A+x)
    assert Pow(2, A) == A2

def test_constant_function():
    assert sin(A) == A2
    assert f(A) == A2
    assert f(A, C1) in (Constant('C2', x, z), Constant('A2', x, z))
    assert f(C1, A) in (Constant('C2', x, z), Constant('A2', x, z))
    assert f(A, C1, y) in (Constant('C2', x, z), Constant('A2', x, z))
    assert f(A, x) == f(Constant('A', x), x)
    assert f(A, C1, x) == f(Constant('A', x), Constant('C1', x, z), x)
    assert f(A, y) == A2
    assert f(y, A) == A2


