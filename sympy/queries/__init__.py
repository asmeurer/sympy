# -*- coding: utf-8 -*-
import inspect
from sympy.core import Symbol, sympify
from sympy.utilities.source import get_class
from sympy.assumptions import eliminate_assume, list_global
from sympy.logic.boolalg import to_cnf, conjuncts, \
    compile_rule, Equivalent, And
from sympy.logic.algorithms.dpll import dpll_satisfiable

def query(expr, *args, **kwargs):
    """
    Method for inferring properties about objects.

    Syntax

        * query(expression, key=boolean)

        * query(expression, key=boolean, assumptions=assumptions)

            where expression is any SymPy expression, and boolean is any
            boolean value (True/False). key can have any value listed in
            handlers_dict.keys()

            It accepts an optional keyword assumptions, a boolean expression
            containing assumptions satisfied by expr

    Examples
        >>> from sympy import *
        >>> x = Symbol('x')
        >>> query(x, commutative=True) # all symbols are assumed to be commutative by default
        True
        >>> query(x, real=True, assumptions=Assume(x, real=True)) # all integers are reals
        True
    """
    assumptions = kwargs.pop('assumptions', [])
    if assumptions and not hasattr(assumptions, '__iter__'):
        assumptions = conjuncts(to_cnf(assumptions))
    assumptions.extend(list_global())

    key, value = kwargs.popitem()
    expr = sympify(expr)
    if kwargs:
        # split multiple queries
        k = {key: value}
        return query(expr, assumptions=assumptions, **k) and \
               query(expr, assumptions=assumptions, **kwargs)
    if not value: # only True queries from now on (e.g. prime=True)
        k = {key: True}
        result = query(expr, assumptions=assumptions, **k)
        if result is not None:
            return not result
        return

    # direct resolution method, no logic
    resolutors = []
    for handler in handlers_dict[key]:
        resolutors.append( get_class(handler) )
    res, _res = None, None
    mro = inspect.getmro(type(expr))
    for handler in resolutors:
        for subclass in mro:
            if hasattr(handler, subclass.__name__):
                res = getattr(handler, subclass.__name__)(expr, assumptions)
                if _res is None: _res = res
                elif _res != res: raise ValueError, 'incompatible resolutors'
                break
    if res is not None:
        return res

    # use logic inference
    if not expr.is_Atom: return
    clauses = []
    for k, values in known_facts_dict.iteritems():
        for v in values:
            clauses.append(Equivalent(compile_rule(k), compile_rule(v)))
    result = None

    # add assumptions to the knowledge base
    for assump in assumptions:
        clauses.append(eliminate_assume(assump, symbol=expr))

    clauses.append(Symbol(key))
    if not dpll_satisfiable(And(*clauses)): #TODO: call dpll and avoid creating this object
        return False
    clauses[-1] = ~clauses[-1]
    if not dpll_satisfiable(And(*clauses)):
        # if the negation is satisfiable, it is entailed
        return True
    clauses.pop(-1)


def register_handler(key, handler):
    """Register a handler in the query system. key must be a string and handler a
    class inheriting from QueryHandler.

        >>> from sympy.queries.handlers import QueryHandler
        >>> class MersenneHandler(QueryHandler):
        ...     # Mersenne numbers are in the form 2**n + 1, n integer
        ...     @staticmethod
        ...     def Integer(expr, assumptions):
        ...         import math
        ...         return query(math.log(expr + 1, 2), integer=True)
        >>> register_handler('mersenne', MersenneHandler)
        >>> query(7, mersenne=True)
        True
    """
    if key in handlers_dict:
        handlers_dict[key].append(handler)
    else:
        handlers_dict.update({key: [handler]})

def remove_handler(key, handler):
    """Removes a handler from the query system. Same syntax as register_handler"""
    handlers_dict[key].remove(handler)

# query_dict tells us what query handler we should use
# for a particular key
handlers_dict = {
    'bounded'        : ['sympy.queries.handlers.calculus.QueryBoundedHandler'],
    'commutative'    : ['sympy.queries.handlers.QueryCommutativeHandler'],
    'comparable'     : ['sympy.queries.handlers.QueryComparableHadler'],
    'complex'        : ['sympy.queries.handlers.sets.QueryComplexHandler'],
    'composite'      : ['sympy.queries.handlers.ntheory.QueryCompositeHandler'],
    'even'           : ['sympy.queries.handlers.ntheory.QueryEvenHandler'],
    'extended_real'  : ['sympy.queries.handlers.sets.QueryExtendedRealHandler'],
    'imaginary'      : ['sympy.queries.handlers.sets.QueryImaginaryHandler'],
    'infinitesimal'  : ['sympy.queries.handlers.calculus.QueryInfinitesimalHandler'],
    'integer'        : ['sympy.queries.handlers.sets.QueryIntegerHandler'],
    'irrational'     : ['sympy.queries.handlers.sets.QueryIrrationalHandler'],
    'rational'       : ['sympy.queries.handlers.sets.QueryRationalHandler'],
    'negative'       : ['sympy.queries.handlers.order.QueryNegativeHandler'],
    'positive'       : ['sympy.queries.handlers.order.QueryPositiveHandler'],
    'prime'          : ['sympy.queries.handlers.ntheory.QueryPrimeHandler'],
    'real'           : ['sympy.queries.handlers.sets.QueryRealHandler'],
    'odd'            : ['sympy.queries.handlers.ntheory.QueryOddHandler'],
    'zero'           : ['sympy.queries.handlers.order.QueryZeroHandler']
}

known_facts_dict = {
    'complex'       : ['real | complex_number_re_0'],
    'even'          : ['integer & ~odd'],
    'extended_real' : ['real | infinity'],
    'odd'           : ['integer & ~even'],
    'prime'         : ['integer & positive & ~composite'],
    'integer'       : ['rational & denominator_one'],
    'imaginary'     : ['complex & ~real'],
    'negative'      : ['real & ~positive & ~zero'],
    'positive'      : ['real & ~negative & ~zero'],
    'rational'      : ['real & ~irrational'],
    'real'          : ['rational | irrational' ],
    'zero'          : ['real & ~positive & ~negative']
}
