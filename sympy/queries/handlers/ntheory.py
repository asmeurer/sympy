from sympy.queries import query
from sympy.queries.handlers import CommonHandler
from sympy.ntheory import isprime

class QueryPrimeHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        """Just use int(expr) once
        http://code.google.com/p/sympy/issues/detail?id=1462
        is solved"""
        if expr.is_number:
            _integer = query(expr, integer=True)
            if _integer:
                return isprime(expr.evalf(1))
            return _integer

    @staticmethod
    def Mul(expr, assumptions):
        if expr.is_number:
            return QueryPrimeHandler.Basic(expr, assumptions)
        for arg in expr.args:
            if query(arg, integer=True, assumptions=assumptions):
                pass
            else:
                break
        else:
            # a product of integers can't be a prime
            return False

    @staticmethod
    def Integer(expr, assumptions):
        return isprime(expr)

    @staticmethod
    def Rational(expr, assumptions):
        return False

    @staticmethod
    def Real(expr, assumptions):
        if (int(expr) - expr).evalf() == 0:
            return isprime(int(expr))
        return False

    @staticmethod
    def Infinity(expr, assumptions):
        return False

    @staticmethod
    def NegativeInfinity(expr, assumptions):
        return False

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False

    @staticmethod
    def NumberSymbol(expr, assumptions):
        if (expr - expr.evalf(1)) == 0:
            return isprime(int(expr.evalf(1)))
        return False

class QueryCompositeHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        return query(expr, positive=True, integer=True, prime=False, \
                assumptions=assumptions)

class QueryEvenHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        if expr.is_number:
            if query(expr, integer=False): return False
            return float(expr.evalf()) % 2 == 0

    @staticmethod
    def Mul(expr, assumptions):
        """
        Even * Integer -> Even
        Even * Odd     -> Even
        Integer * Odd  -> ?
        Odd * Odd      -> Odd
        """
        if expr.is_number:
            return QueryEvenHandler.Basic(expr, assumptions)
        even, odd, irrational = False, 0, False
        for arg in expr.args:
            # check for all integers and at least one even
            if query(arg, integer=True, assumptions=assumptions):
                if query(arg, even=True, assumptions=assumptions):
                    even = True
                elif query(arg, odd=True, assumptions=assumptions):
                    odd += 1
            elif query(arg, irrational=True, assumptions=assumptions):
                # one irrational makes the result False
                # two makes it undefined
                if irrational:
                    break
                irrational = True
            else: break
        else:
            if irrational: return False
            if even: return True
            if odd == len(expr.args): return False

    @staticmethod
    def Add(expr, assumptions):
        """
        Even + Odd  -> Odd
        Even + Even -> Even
        Odd  + Odd  -> Even

        TODO: remove float() when issue
        http://code.google.com/p/sympy/issues/detail?id=1473
        is solved
        """
        if expr.is_number:
            if query(expr, integer=False): return False
            return float(expr.evalf()) % 2 == 0
        _result = True
        for arg in expr.args:
            if query(arg, even=True, assumptions=assumptions):
                pass
            elif query(arg, odd=True, assumptions=assumptions):
                _result = not _result
            else: break
        else:
            return _result

    @staticmethod
    def Integer(expr, assumptions):
        return expr % 2 == 0

    @staticmethod
    def Rational(expr, assumptions):
        return False

    @staticmethod
    def Real(expr, assumptions):
        return expr % 2 == 0

    @staticmethod
    def Infinity(expr, assumptions):
        return False

    @staticmethod
    def NegativeInfinity(expr, assumptions):
        return False

    @staticmethod
    def NumberSymbol(expr, assumptions):
        if query(expr, integer=True):
            return query(int(expr), even=True)
        return False

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False

    @staticmethod
    def abs(expr, assumptions):
        if query(expr.args[0], real=True, assumptions=assumptions):
            return query(expr.args[0], even=True, assumptions=assumptions)

    @staticmethod
    def re(expr, assumptions):
        if query(expr.args[0], real=True, assumptions=assumptions):
            return query(expr.args[0], even=True, assumptions=assumptions)

    @staticmethod
    def im(expr, assumptions):
        if query(expr.args[0], real=True, assumptions=assumptions):
            return True

class QueryOddHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        return query(expr, integer=True, even=False, \
                assumptions=assumptions)
