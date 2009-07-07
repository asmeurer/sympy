from sympy import Basic, Symbol, S, sympify, any, Mul, sin


class Constant(Symbol):
    """
    Constant Symbol.

    This class represents an arbirary constant Symbol.
    That means that it will absorb anything that it isn't independent of.
    """
    is_Constant = True
    is_commutative = True
    
    def __new__(cls, name, *args, **assumptions):
        # args is a list of symbols the Constant is independent of
        args = tuple(set(args)) # eliminate duplicates and canonize order
        args = map(sympify, args)
        cls.name = name
        return Basic.__new__(cls, *args)


x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
C = Constant('C', x)
# We want C (Constant) below to absorb the y's, but not the x's

print C.name
print C.args
print 'y*C', y*C, y*C == C
print 'x*C', x*C, x*C == x*Constant('C', x)
print 'C*y', C*y, C*y == C
print 'C*x', C*x, C*x == x*Constant('C', x)
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
C = Constant('C', x, y)
print 'C*x*y*z', C*x*y*z, C*x*y*z == C*x*y
print 'C*x*y**2*sin(z)', C*x*y**2*sin(z), C*x*y**2*sin(z) == C*x*y**2
C1 = Constant('C1', x, z)
print 'C*C1', C*C1, C*C1 == Constant('C', x, y, z)
print 'C1*C', C1*C, C1*C == Constant('C1', x, y, z)
print '(C1*C).args', (C1*C).args, (C1*C).args == (x, y, z)
print '(C*C1).args', (C*C1).args, (C*C1).args == (x, y, z)
print C1.name
print 'C1*C1', C1*C1, C1*C1 == Constant('C1', x, z)
C2 = Constant('C2', y, z)
print 'C*C1*C2', C*C1*C2, C*C1*C2 == Constant('C', x, y, z)

