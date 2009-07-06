from sympy import Basic, Symbol, S, sympify, any, Mul


class Constant(Symbol):
    """
    Constant Symbol.

    This class represents an arbirary constant Symbol.
    That means that it will absorb anything that it isn't independent of.
    """
    is_Constant = True
    is_commutative = True
    name = 'Constant'

    def __new__(cls, name, *args, **assumptions):
        args = map(sympify, args)
        return Basic.__new__(cls, *args)


x = Symbol('x')
y = Symbol('y')
C = Constant('C',x)
# We want C (Constant) below to absorb the y's, but not the x's
print 'y*C', y*C, y*C == C
print 'x*C', x*C, x*C == x*C
print 'C*y', C*y, C*y == C
print 'C*x', C*x, C*x == x*C
print 'y*C*x', y*C*x, y*C*x == C*x
print 'x*y*C', x*y*C, x*y*C == x*C
print 'y*x*C', y*x*C, y*x*C == x*C
print 'C*y*(y+1)', C*y*(y+1), C*y*(y+1) == C
print 'y*C*(y+1)', y*C*(y+1), y*C*(y+1) == C
print 'x*(y*C)', x*(y*C), x*(y*C) == x*C
print 'x*(C*y)', x*(C*y), x*(C*y) == x*C
print 'C*(x*y)', C*(x*y), C*(x*y) == C*x
print '(x*y)*C', (x*y)*C, (x*y)*C == x*C
print '(y*x)*C', (y*x)*C, (y*x)*C == x*C
print 'y*(y+1)*C', y*(y+1)*C, y*(y+1)*C == C
print 'C*x*y', C*x*y, C*x*y == C*x
print 'x*C*y', x*C*y, x*C*y == x*C
print '(C*x)*y', (C*x)*y, (C*x)*y == C*x
print 'y*(x*C)', y*(x*C), y*(x*C) == x*C
print '(x*C)*y', (x*C)*y, (x*C)*y == x*C