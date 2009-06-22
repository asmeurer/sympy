# doctests are disabled because of issue #1521
from sympy.core import Basic, Symbol
from sympy.core.relational import Relational

__global_assumptions = []

def register_global(assump):
    """Register an assumption as global

    Examples:
#        >>> from sympy import *
#        >>> list_global()
#        []
#        >>> x = Symbol('x')
#        >>> register_global(Assume(x, real=True))
#        True
#        >>> list_global()
#        [Assume(x, real=True)]

    You can undo this calling remove_global
    """
    __global_assumptions.append(assump)
    return True

def list_global():
    """List all global assumptions"""
    return __global_assumptions[:] # make a copy

def remove_global(assump):
    """Remove a global assumption. If argument is not
    a global assumption, it will raise  ValueError
    """
    __global_assumptions.remove(assump)
    return True

class Assume(Basic):
    """New-style assumptions

#    >>> from sympy import Symbol, Assume
#    >>> x = Symbol('x')
#    >>> Assume(x, integer=True)
#    Assume( x, integer = True )
#    >>> Assume(x, integer=False)
#    Assume( x, integer = False )
#    >>> Assume( x > 1 )
#    Assume( x > 1, relational = True)
    """

    def __init__(self, expr, *args, **kwargs):
        if isinstance(expr, Symbol):
            key, value = kwargs.popitem()
        elif isinstance(expr, Relational):
            key, value = 'relational', True
        if kwargs:
            raise ValueError('Wrong set of arguments')
        self._args = (expr, key, value)

    is_Atom = True # do not attempt to decompose this

    @property
    def expr(self):
        return self._args[0]

    @property
    def key(self):
        return self._args[1]

    @property
    def value(self):
        return self._args[2]

    def __eq__(self, other):
        if type(other) == Assume:
            return self._args == other._args
        return False

def eliminate_assume(expr, symbol=None):
    """
    Will convert an expression with assumptions to an equivalent with all assumptions
    replaced by symbols
    Assume(x, integer=True) --> integer
    Assume(x, integer=False) --> ~integer
    """
    if isinstance(expr, Assume):
        if symbol is not None:
            if not expr.expr.has(symbol): return
        if expr.value: return Symbol(expr.key)
        return ~Symbol(expr.key)
    args = []
    for a in expr.args:
        args.append(eliminate_assume(a))
    return type(expr)(*args)

