"""This module contains query handlers resposible for calculus queries:
infinitesimal, bounded, etc.
"""
from sympy.queries import query
from sympy.queries.handlers import CommonHandler

class QueryInfinitesimalHandler(CommonHandler):

    @staticmethod
    def Mul(expr, assumptions):
        for arg in expr.args:
            _result = query(arg, infinitesimal=True, assumptions=assumptions)
            if _result:
                pass
            else:
                return _result
        else:
            return True

    Add, Pow = Mul, Mul

    @staticmethod
    def Number(expr, assumptions):
        return expr == 0

    NumberSymbol = Number

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False


class QueryBoundedHandler(CommonHandler):

    @staticmethod
    def Add(expr, assumptions):
        """
        Bounded + Bounded     -> Bounded
        Unbounded + Bounded   -> Unbounded
        Unbounded + Unbounded -> ?
        """
        _first_unbounded = True
        for arg in expr.args:
            _result = query(arg, bounded=True, assumptions=assumptions)
            if _result is None:
                return
            elif not _result:
                if _first_unbounded:
                    _first_unbounded = False
                else:
                    # more than one unbounded, we don't know
                    return
        return _first_unbounded

    @staticmethod
    def Mul(expr, assumptions):
        """
        Bounded * Bounded -> Bounded
        (Infinitesimal & Bounded) * Unbounded -> ?
        (Bounded & ~Infinitesimal) * Unbounded -> Unbounded
        Ubounded * Unbounded -> Unbounded
        """
        _output = True
        for arg in expr.args:
            if not query(arg, bounded=True, assumptions=assumptions):
                if not query(arg, infinitesimal=True, assumptions=assumptions):
                    if _output:
                        _output = False
                    else:
                        return
                else:
                    return
        return _output

    @staticmethod
    def Pow(expr, assumptions):
        """
        Unbounded ** Whatever -> Unbounded
        Bounded ** Unbounded -> Unbounded if base > 1
        Bounded ** Unbounded -> Unbounded if base < 1
        """
        base_bounded = query(expr.base, bounded=True, assumptions=assumptions)
        if not base_bounded: return base_bounded
        if query(expr.exp, bounded=True, assumptions=assumptions) \
            and base_bounded: return True
        if base_bounded and expr.base.is_number:
            # We need to implement relations for this
            if abs(expr.base) > 1:
                return False
            return True

    @staticmethod
    def Symbol(expr, assumptions):
        if query(expr, zero=True, assumptions=assumptions):
            return True
        for assump in assumptions:
            if assump.key == 'bounded' and assump.expr == expr:
                return assump.value
        return False

    @staticmethod
    def log(expr, assumptions):
        return query(expr.args[0], bounded=True, assumptions=assumptions)

    exp = log

    @staticmethod
    def sin(expr, assumptions):
        return True

    cos = sin

    @staticmethod
    def Number(expr, assumptions):
        return True

    @staticmethod
    def Infinity(expr, assumptions):
        return False

    @staticmethod
    def NegativeInfinity(expr, assumptions):
        return False

    @staticmethod
    def Pi(expr, assumptions):
        return True

    @staticmethod
    def Exp1(expr, assumptions):
        return True

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return True

    @staticmethod
    def sign(expr, assumptions):
        return True

class QueryUnboundedHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        return query(expr, bounded=False, extended_real=True, \
                assumptions=assumptions)
