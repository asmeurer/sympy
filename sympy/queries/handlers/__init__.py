from sympy.logic.boolalg import disjuncts
from sympy.queries import query

class QueryHandler(object):
    """Base class that all Query Handlers must inherit"""
    pass

class CommonHandler(QueryHandler):
    """Defines some useful methods common to most Handlers """

    @staticmethod
    def NaN(expr, assumptions):
        return False

class QueryCommutativeHandler(CommonHandler):

    @staticmethod
    def Symbol(expr, assumptions):
        """Objects are expected to be commutative unless otherwise stated"""
        for assump in assumptions:
            if assump.expr == expr and assump.key == 'commutative':
                return assump.value
        return True

    @staticmethod
    def Basic(expr, assumptions):
        for arg in expr.args:
            if not query(arg, commutative=True, assumptions=assumptions):
                return False
        return True

    @staticmethod
    def Number(expr, assumptions):
        return True

    @staticmethod
    def NaN(expr, assumptions):
        return True

class QueryComparableHadler(CommonHandler):

    @staticmethod
    def Mul(expr, assumptions):
        for arg in expr.args:
            _result = query(arg, comparable=True, assumptions=assumptions)
            if not _result:
                return _result
        return True

    Add, Pow = Mul, Mul

    @staticmethod
    def Number(expr, assumptions):
        return True

    @staticmethod
    def ImaginaryUnit(expr, assumptions):
        return False

    @staticmethod
    def Pi(expr, assumptions):
        return True

    @staticmethod
    def Exp1(expr, assumptions):
        return True

