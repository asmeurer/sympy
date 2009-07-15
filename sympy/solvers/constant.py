from sympy.core import Basic, Symbol, S, sympify, Pow
from sympy.utilities.iterables import any
from sympy.core.decorators import _sympifyit

import re


class Constant(Symbol):
    """
    Constant Symbol.

    This class represents an arbitrary constant Symbol.
    That means that it will absorb anything that it isn't independent of.
    It returns a new instance of the class whenever it absorbs something, with
    an incremented number at the end of the name.  Use .relations() to see how
    numbered Constants are related to each other.

    Example:
    >>> from sympy import *
    >>> x, a = symbols('xa')
    >>> C = Constant('C', x)
    >>> C*x
    C*x
    >>> 2*C+a
    C2
    >>> C3 = Constant('C3', x)
    >>> C3*2
    C4
    >>> C4+2
    C5
    >>> C5.relations()
    {C5:'C4+2', C4:'2*C3'}
    """
    is_Constant = True
    is_commutative = True

    def __new__(cls, name, *args):
        # args is a list of symbols the Constant is independent of
        args = tuple(set(args)) # eliminate duplicates and canonize order
        args = map(sympify, args)
        obj = Basic.__new__(cls, *args)
        namepattern = re.compile("([^\d]*)(_)?(\d*)$")
        name_number = re.match(namepattern, name)
        obj.varname = name_number.group(1)
        obj.number = name_number.group(3) # obj.number is a str, not an int
        obj.name = obj.varname + obj.number
        obj.relations_dict = {}
        return obj

    def __str__(self):
        return self.name

    def _eval_power(self, other):
        # First combine constants together.
        if getattr(other, 'is_Constant', None):
            # the same as in __rpow__ below, but is needed for direct call to
            # Pow(C1, C2)
            constantsymbols = set(self.args).union(set(other.args))
            highestconstant = max(self, other, key=lambda t: t.number)
            constant = highestconstant.new(highestconstant.name, *constantsymbols)
            constant.increment_number()
            return constant
        # Then combine constant with other terms.
        if not any((t in other) for t in self.args):
            return self.new(self.name, *self.args).increment_number()
        else:
            return None

    def _eval_rpower(self, other):
        # other**self
        if other.is_Constant:
            constantsymbols = set(self.args).union(set(other.args))
            highestconstant = max(self, other, key=lambda t: t.number)
            constant = highestconstant.new(highestconstant.name, *constantsymbols)
            constant.increment_number()
            return constant
        if not any((t in other) for t in self.args):
            return self.new(self.name, *self.args).increment_number()
        else:
            return Pow(other, self, evaluate=False, commutative=True)

    def as_coefficient(self, expr):
        # Maybe this needs to be done differently?
        return None
        
    def increment_number(self, amount=1, no_number_value=1):
        """
        Increments self.number by amount.  If self.number is "" (i.e., no
        number was given at assignment), self.number is assumed to be
        no_number_value.  This only changes the name of self, not the name of
        any variable that self is assigned to.  amount can be any integer value,
        positive, negative, or zero.  If self.number = '', amount=0 amounts to
        applying no_number_value to self.number.
        
        Example:
        >>> from sympy import *
        >>> x = Symbol('x')
        >>> A1 = Constant('A1', x)
        >>> A1.increment_number()
        A2
        >>> A1.increment_number(amount=2)
        A4
        >>> B = Constant('B', x)
        >>> C = Constant('C', x)
        >>> B.increment_number()
        B2
        >>> C.increment_number(no_number_value=2)
        C3
        >>> D = Constant('D', x)
        >>> D.increment_number(amount=0)
        D1
        >>> D.increment_number(amount=-1)
        D-1
        """
        if self.number == "":
            self.number = str(amount + no_number_value)
        else:
            self.number = str(int(self.number) + amount)
        self.name = self.varname + self.number
        return self

