from sympy.core import S, Symbol, sympify
from sympy.utilities.source import get_class
from sympy.queries import query

def refine(expr, assumptions=None):
    """Simplify an expression using assumptions

    gives the form of expr that would be obtained if symbols
    in it were replaced by explicit numerical expressions satisfying
    the assumptions assum.

    Examples: TODO
    """
    if not expr.is_Atom:
        args = map(refine, expr.args, [assumptions]*len(expr.args))
        expr = type(expr)(*args)
    name = expr.__class__.__name__
    handler = handlers_dict.get(name, None)
    if handler is None: return expr
    new_expr = handler(expr, assumptions)
    if (new_expr is None) or (expr == new_expr):
        return expr
    return refine(new_expr)

def refine_abs(expr, assumptions):
    """handler for the absolute value"""
    arg = expr.args[0]
    if query(arg, positive=True, assumptions=assumptions):
        return arg
    if query(arg, negative=True, assumptions=assumptions):
        return -arg

def refine_pow(expr, assumptions):
    pass

def refine_exp(expr, assumptions):
    """handler for exponential function
    Some rules to simplify complex exponentials
    """
    arg = expr.args[0]
    if arg.is_Mul:
        coeff = arg.as_coefficient(S.Pi*S.ImaginaryUnit)
        if coeff:
            if query(2*coeff, integer=True, assumptions=assumptions):
                if query(coeff, even=True, assumptions=assumptions):
                    return S.One
                elif query(coeff, odd=True, assumptions=assumptions):
                    return S.NegativeOne
                elif query(coeff + S.Half, even=True, assumptions=assumptions):
                    return -S.ImaginaryUnit
                elif query(coeff + S.Half, odd=True, assumptions=assumptions):
                    return S.ImaginaryUnit

handlers_dict = {
    'abs'        : refine_abs,
    'pow'        : refine_pow,
    'exp'        : refine_exp,
}
