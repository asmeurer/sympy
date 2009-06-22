from sympy.queries import query
from sympy.queries.handlers import CommonHandler


class QueryIntegerHandler(CommonHandler):

    @staticmethod
    def Add(expr, assumptions):
        """
        Integer + Integer       -> Integer
        NonInteger + Integer    -> Noninteger
        NonInteger + NonInteger -> ?
        """
        _output = True
        for arg in expr.args:
            _result = query(arg, integer=True, assumptions=assumptions)
            if _result is None:
                return
            elif _result is False:
                if _output:
                    _output = False
                else:
                    return
        else:
            return _output

    @staticmethod
    def Mul(expr, assumptions):
        """
        Integer*Integer -> Integer
        Integer*Irrational -> NonInteger
        Integer*Rational   -> ?
        """
        _output = True
        for arg in expr.args:
            if not query(arg, integer=True, assumptions=assumptions):
                if arg.is_Rational:
                    if arg.q == 2:
                        return query(2*expr, even=True, assumptions=assumptions)
                    if arg.q % 2 == 1:
                        if query(arg.q*expr, even=True, assumptions=assumptions):
                            # even / odd -> !integer
                            return False
                        else: break
                elif query(arg, irrational=True, assumptions=assumptions):
                    if _output:
                        _output = False
                    else:
                        return
                else:
                    return
        else:
            return _output

    @staticmethod
    def Pow(expr, assumptions):
        if expr.is_number:
            if query(expr, real=False): return False
            return int(expr.evalf()) == expr
        for arg in expr.args:
            if not query(arg, integer=True, assumptions=assumptions):
                return
        else:
            return True

    @staticmethod
    def int(expr, assumptions):
        return True

    @staticmethod
    def Integer(expr, assumptions):
        return True

    @staticmethod
    def Rational(expr, assumptions):
        # rationals with denominator one get
        # evaluated to Integers
        return False

    @staticmethod
    def Real(expr, assumptions):
        return int(expr) == expr

    @staticmethod
    def Pi(expr, assumptions):
        return False

    @staticmethod
    def Exp1(expr, assumptions):
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
    def abs(expr, assumptions):
        return query(expr.args[0], integer=True, assumptions=assumptions)

class QueryRationalHandler(CommonHandler):

    @staticmethod
    def Symbol(expr, assumptions):
        if query(expr, zero=True, assumptions=assumptions):
            # zero is a rational number
            return True

    @staticmethod
    def Add(expr, assumptions):
        """
        Rational + Rational     -> Rational
        Irrational + Rational   -> Irrational
        Irrational + Irrational -> ?
        """
        _output = True
        for arg in expr.args:
            _result = query(arg, rational=True, assumptions=assumptions)
            if _result is None:
                return
            elif _result is False:
                if _output:
                    _output = False
                else:
                    return
        else:
            return _output

    @staticmethod
    def Mul(expr, assumptions):
        """
        Rational * Rational     -> Rational
        Rational * Irrational   -> Irrational
        Irrational * Irrational -> ?
        """
        _first_irrational = True
        for arg in expr.args:
            _r = query(arg, rational=True, assumptions=assumptions)
            if not _r:
                if _r is None: return
                if _first_irrational: _first_irrational = False
                else: return
        else: return _first_irrational

    @staticmethod
    def Pow(expr, assumptions):
        """
        Rational ** Rational -> Rational
        Irrational ** Rational -> Irrational
        Rational ** Irrational -> ?
        """
        return query(expr.base, rational=True, assumptions=assumptions) and \
            query(expr.exp, rational=True, assumptions=assumptions)

    @staticmethod
    def Rational(expr, assumptions):
        return True

    @staticmethod
    def Real(expr, assumptions):
        # it's finite-precission
        return True

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False

    @staticmethod
    def Infinity(expr, assumptions):
        return False

    @staticmethod
    def NegativeInfinity(expr, assumptions):
        return False

    @staticmethod
    def Pi(expr, assumptions):
        return False

    @staticmethod
    def Exp1(expr, assumptions):
        return False

class QueryIrrationalHandler(CommonHandler):

    @staticmethod
    def Basic(expr, assumptions):
        return query(expr, real=True, rational=False, \
                assumptions=assumptions)

class QueryRealHandler(CommonHandler):

    @staticmethod
    def Add(expr, assumptions):
        if expr.is_number: return expr.as_real_imag()[1] == 0
        for arg in expr.args:
            if not query(arg, real=True, assumptions=assumptions):
                break
        else:
            return True

    Mul, Pow = Add, Add

    @staticmethod
    def Rational(expr, assumptions):
        return True

    @staticmethod
    def Real(expr, assumptions):
        return True

    @staticmethod
    def Pi(expr, assumptions):
        return True

    @staticmethod
    def Exp1(expr, assumptions):
        return True

    @staticmethod
    def abs(expr, assumptions):
        return True

    @staticmethod
    def re(expr, assumptions):
        return True

    im = re

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False

    @staticmethod
    def Infinity(expr, assumptions):
        return False

    @staticmethod
    def NegativeInfinity(expr, assumptions):
        return False

    @staticmethod
    def sin(expr, assumptions):
        if query(expr.args[0], real=True, assumptions=assumptions):
            return True

    cos, exp = sin, sin

class QueryExtendedRealHandler(QueryRealHandler):

    @staticmethod
    def Infinity(expr, assumptions):
        return True

    @staticmethod
    def NegativeInfinity(expr, assumptions):
        return True

class QueryComplexHandler(CommonHandler):

    @staticmethod
    def Add(expr, assumptions):
        for arg in expr.args:
            if not query(arg, complex=True, assumptions=assumptions):
                return None
        return True

    Mul, Pow = Add, Add

    @staticmethod
    def Number(expr, assumptions):
        return True

    @staticmethod
    def NumberSymbol(expr, assumptions):
        return True

    @staticmethod
    def abs(expr, assumptions):
        return True

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return True

    @staticmethod
    def Infinity(expr, assumptions):
        return False

    @staticmethod
    def NegativeInfinity(expr, assumptions):
        return False

    sin, cos, exp, re, im = [abs]*5 # they are all complex functions

class QueryImaginaryHandler(CommonHandler):

    @staticmethod
    def Add(expr, assumptions):
        """
        Imaginary + Imaginary -> Imaginary
        Imaginary + Complex   -> ?
        Imaginary + Real      -> !Imaginary
        """
        reals = 0
        for arg in expr.args:
            if query(arg, imaginary=True, assumptions=assumptions):
                pass
            elif query(arg, real=True, assumptions=assumptions):
                reals += 1
            else:
                break
        else:
            if reals == 0:
                return True
            if reals == 1 or (len(expr.args) == reals):
                # two reals could sum 0 thus giving an imaginary
                return False

    @staticmethod
    def Mul(expr, assumptions):
        """
        Real*Imaginary -> Imaginary
        Imaginary*Imaginary -> Real
        """
        result = False
        reals = 0
        for arg in expr.args:
            if query(arg, imaginary=True, assumptions=assumptions):
                result = result ^ True
            elif not query(arg, real=True, assumptions=assumptions):
                break
        else:
            if reals == len(expr.args):
                return False
            return result

    Pow = Add

    @staticmethod
    def Number(expr, assumptions):
        return not (expr.as_real_imag()[1] == 0)

    NumberSymbol = Number

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return True
