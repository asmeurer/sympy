from sympy import Basic, Symbol, S, sympify, any, Mul, Pow
from sympy.core.decorators import _sympifyit
# remove the following. They are only for tests
from sympy import sin, exp


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
        obj = Basic.__new__(cls, *args)
        obj.name = name
        return obj
    
    def __str__(self):
        return self.name
    
    def _eval_power(self, other):
        # First combine constants together.  
        if other.is_Constant:
            # the same as in __rpow__ below, but is needed for direct call to 
            # Pow(C1, C2)
            constantsymbols = set(self.args).union(set(other.args))
            return self.new(self.name, *constantsymbols)
        # Then combine constant with other terms. 
        if not any((t in other) for t in self.args):
            return self
        else:
            return None

    @_sympifyit('other', NotImplemented)
    def __rpow__(self, other):
        # other**self
        if other.is_Constant:
            constantsymbols = set(self.args).union(set(other.args))
            print 'rpow test'
            return other.new(other.name, *constantsymbols)
        if not any((t in other) for t in self.args):
            return self
        else:
            return Pow(other, self)


x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
C = Constant('C', x)
C0 = Constant('C0', x, y)
C1 = Constant('C1', x, z)
C2 = Constant('C2', y, z)
# We want C (Constant) below to absorb the y's, but not the x's

print 'C.name', C.name, C.name == 'C'
print 'C.args', C.args, C.args == (x,)
print 'y*C', y*C, y*C == C
print 'x*C', x*C, x*C == x*Constant('C', x)
print 'C*y', C*y, C*y == C
print 'C*x', C*x, C*x == x*Constant('C', x)
print '2*C', 2*C, 2*C == C
print 'C*2', C*2, C*2 == C
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
print 'C0*x*y*z', C0*x*y*z, C0*x*y*z == C0*x*y
print 'C0*x*y**2*sin(z)', C0*x*y**2*sin(z), C0*x*y**2*sin(z) == C0*x*y**2
print 'C0*C1', C0*C1, C0*C1 == Constant('C0', x, y, z)
print 'C1*C', C1*C0, C1*C0 == Constant('C1', x, y, z)
print '(C1*C0).args', (C1*C0).args, (C1*C0).args == (x, y, z)
print '(C0*C1).args', (C0*C1).args, (C0*C1).args == (x, y, z)
print 'C1.name', C1.name, C1.name == 'C1'
print 'C1*C1', C1*C1, C1*C1 == Constant('C1', x, z)
print 'C0*C1*C2', C0*C1*C2, C0*C1*C2 == Constant('C0', x, y, z)
print
print 'C+C', C+C, C+C == C
print 'C+2', C+2, C+2 == C
print '2+C', 2+C, 2+C == C
print 'C+y', C+y, C+y == C
print 'C+x', C+x, C+x == Constant('C', x) + x
print 'C+x+y+x*y+2', C+x+y+x*y+2, C+x+y+x*y+2 == C+x+x*y
print 
print 'C**C', C**C, C**C == C
print 'Pow(C,C)', Pow(C,C), Pow(C,C) == C
print 'C0**C1', C0**C1, C0**C1 == Constant('C0', x, y, z)
print 'C1**C0', C1**C0, C1**C0 == Constant('C1', x, y, z)
print 'C**y', C**y, C**y == C
print 'C**x', C**x, C**x == Constant('C', x)**x
print 'C**2', C**2, C**2 == C
print 'C**(x*y)', C**(x*y) == Constant('C', x)**(x*y)
print 'x**C', x**C, x**C == x**Constant('C', x)
print 'y**C', y**C, y**C == C
print 'x**y**C', x**y**C, x**y**C == x**C
print '(x**y)**C', (x**y)**C, (x**y)**C == (x**y)**Constant('C', x)
print 'x**(y**C)', x**(y**C), x**(y**C) == x**C
print 'x**C**y', x**C**y, x**C**y, x**C**y == x**C
print 'x**(C**y)', x**(C**y), x**(C**y) == x**C
print '(x**C)**y', (x**C)**y, (x**C)**y == (x**Constant('C', x))**y
print '2**C', 2**C, 2**C == C
print 'S(2)**C', S(2)**C, S(2)**C == C
print 'exp(C)', exp(C), exp(C) == C
print 'exp(C+x)', exp(C+x), exp(C+x) == exp(C+x)
print 'sin(C)', sin(C), sin(C) == C
f = Function('f')
print 'f(C)', f(C), f(C) == C
print 'f(C, C1)', f(C, C1), f(C, C1) == Constant('C', x, z)
print 'f(C, x)', f(C, x), f(C, x) == f(Constant('C', x), x)
print 'f(C, C1, x)', f(C, C1, x), f(C, C1, x) == f(Constant('C', x), Constant('C1', x, z), x)
print 'f(C, y)', f(C, y), f(C, y) == C
print 'f(C, C1, y)', f(C, C1, y), f(C, C1, y) == Constant('C', x, z)
