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

    def __mul__(self, other):
        print 'mul', self, other
        if other.is_Mul:
            # Mul case
            keep = []
            for i in other.args:
                if any((i.has(t) for t in self.args)):
                    keep.append(i)
            return Mul(self, *keep)
        else:
        # Other case
            if any((other.has(t) for t in self.args)):
                return Mul(self,other)
            else:
                return self

    def __rmul__(self, other):
        print 'rmul'
        if other.is_Mul:
            # Mul case
            keep = []
            for i in other.args:
                if any((i.has(t) for t in self.args)):
                    keep.append(i)
            return Mul(self, *keep)
        else:
       # Other case
            if any((other.has(t) for t in self.args)):
                return Mul(self,other)
            else:
                return self

x = Symbol('x')
y = Symbol('y')
a = Constant('C',x)
# We want a (Constant) below to absorb the y's, but not the x's
print 'y*a', y*a, y*a == a
print 'x*a', x*a, x*a == x*a
print 'a*y', a*y, a*y == a
print 'a*x', a*x, a*x == x*a
print 'y*a*x', y*a*x, y*a*x == a*x
print 'x*y*a', x*y*a, x*y*a == x*a
print 'y*x*a', y*x*a, y*x*a == x*a
print 'a*y*(y+1)', a*y*(y+1), a*y*(y+1) == a
print 'y*a*(y+1)', y*a*(y+1), y*a*(y+1) == a
print 'x*(y*a)', x*(y*a), x*(y*a) == x*a
print 'x*(a*y)', x*(a*y), x*(a*y) == x*a
print 'a*(x*y)', a*(x*y), a*(x*y) == a*x
print '(x*y)*a', (x*y)*a, (x*y)*a == x*a
print '(y*x)*a', (y*x)*a, (y*x)*a == x*a
print 'y*(y+1)*a', y*(y+1)*a, y*(y+1)*a == a
print
print "Failing tests:"
print 'a*x*y', a*x*y, a*x*y == a*x
print 'x*a*y', x*a*y, x*a*y == x*a
print '(a*x)*y', (a*x)*y, (a*x)*y == a*x
print 'y*(x*a)', y*(x*a), y*(x*a) == x*a
print '(x*a)*y', (x*a)*y, (x*a)*y == x*a
print
print 'a*x*y', a*x*y