"""TODO: when relations are implemented, substitute most of this module
with equations"""
from sympy.queries import query
from sympy.queries.handlers import CommonHandler


class QueryNegativeHandler(CommonHandler):
    """http://en.wikipedia.org/wiki/Negative_number"""

    @staticmethod
    def Basic(expr, assumptions):
        if expr.is_number:
            if query(expr, extended_real=True) == False:
                # must be in extended_real
                return False
            return expr.evalf() < 0

    @staticmethod
    def Mul(expr, assumptions):
        _extended = query(expr, extended_real=True, assumptions=assumptions)
        if not _extended: return _extended
        if expr.is_number:
            return expr.evalf() < 0
        parity = 0
        for arg in expr.args:
            _result = query(arg, negative=True, assumptions=assumptions)
            if _result:
                parity += 1
            elif _result is None:
                return None
        return parity % 2 == 1

    @staticmethod
    def Add(expr, assumptions):
        """
        Positive + Positive -> Positive,
        Negative + Negative -> Negative
        """
        if expr.is_number:
            if query(expr, extended_real=True) == False: return False
            return expr.evalf() < 0
        for arg in expr.args:
            if not query(arg, negative=True, assumptions=assumptions):
                break
        else:
            # if all argument's are negative
            return True

    @staticmethod
    def Power(expr, assumptions):
        if expr.is_number:
            if query(expr, extended_real=True) == False: return False
            return expr.evalf() < 0
        if query(expr.base, negative=True, assumptions=assumptions):
            if query(expr.exp, odd=True, assumptions=assumptions):
                return True
            if query(expr.exp, even=True, assumptions=assumptions):
                return False
        elif query(expr.base, positive=True):
            if query(expr.exp, real=True):
                return False
        return None

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False

    @staticmethod
    def abs(expr, assumptions):
        return False

class QueryZeroHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        if expr.is_number:
            # if there are no symbols just evalf
            return expr.evalf() == 0

    @staticmethod
    def Add(expr, assumptions):
        if all([query(x, positive=True, assumptions=assumptions) for x in expr.args]) \
            or all([query(x, negative=True, assumptions=assumptions) for x in expr.args]):
            return False

    @staticmethod
    def Mul(expr, assumptions):
        for arg in expr.args:
            result = query(arg, zero=True, assumptions=assumptions)
            if result == True:
                # one zero is enough
                return True
            elif result is None:
                return None
        else:
            return False

    @staticmethod
    def Pow(expr, assumptions):
        if query(expr.exp, zero=True, assumptions=assumptions) == False:
            return query(expr.base, zero=True, assumptions=assumptions)

    @staticmethod
    def abs(expr, assumptions):
        return query(expr.args[0], zero=True, assumptions=assumptions)

class QueryPositiveHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        if expr.is_number:
            if query(expr, extended_real=True) == False:
                return False
            # if there are no symbols just evalf
            return expr.evalf() > 0

    @staticmethod
    def Mul(expr, assumptions):
        if expr.is_number:
            if query(expr, extended_real=True) == False: return False
            return expr.evalf() > 0
        _result = True
        parity = 0
        for arg in expr.args:
            _result = query(arg, positive=True, assumptions=assumptions)
            if _result == False:
                _is_zero = query(arg, zero=True, assumptions=assumptions)
                if _is_zero != False:
                    return None
                parity += 1
            elif _result is None:
                return None
        return parity % 2 == 0

    @staticmethod
    def Add(expr, assumptions):
        if expr.is_number:
            if query(expr, extended_real=False): return False
            return expr.evalf() > 0
        for arg in expr.args:
            if query(arg, positive=True, assumptions=assumptions) != True:
                break
        else:
            # if all argument's are positive
            return True

    @staticmethod
    def Pow(expr, assumptions):
        if expr.is_number: return expr.evalf() > 0
        if query(expr.base, positive=True, assumptions=assumptions):
            return True
        if query(expr.base, negative=True, assumptions=assumptions):
            if query(expr.exp, even=True, assumptions=assumptions):
                return True
            if query(expr.exp, even=True, assumptions=assumptions):
                return False

    @staticmethod
    def exp(expr, assumptions):
        if query(expr.args[0], real=True, assumptions=assumptions):
            return True

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False

    @staticmethod
    def abs(expr, assumptions):
        return query(expr, zero=False, assumptions=assumptions)
