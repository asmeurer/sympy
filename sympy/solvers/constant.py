from sympy.core import Basic, Symbol, S, sympify, Pow
from sympy.utilities.iterables import any
from sympy.core.decorators import _sympifyit


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
        if getattr(other, 'is_Constant', None):
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
            return other.new(other.name, *constantsymbols)
        if not any((t in other) for t in self.args):
            return self
        else:
            return Pow(other, self)
    
    def as_coefficient(self, expr):
        # Maybe this needs to be done differently?
        return None

