"""Implementation of :class:`PythonComplexDomain` class. """

from sympy.polys.domains.realdomain import RealDomain

from sympy.polys.polyerrors import CoercionFailed

from sympy import (
    Real as sympy_mpf, S
)

sympy_mpc = lambda a: sympy_mpf(a.real) + sympy_mpf(a.imag)*S.ImaginaryUnit

class PythonComplexDomain(RealDomain): # XXX: tmp solution
    """Complex domain. """

    rep   = 'CC'

    dtype = complex
    zero  = dtype(0)
    one   = dtype(1)
    alias = 'CC_python'

    def __init__(self):
        pass

    def to_sympy(self, a):
        """Convert `a` to a SymPy object. """
        return sympy_mpc(a)

    def from_sympy(self, a):
        """Convert SymPy's Integer to `dtype`. """
        b = a.evalf()
        r, i = a.as_real_imag()
        r, i = map(sympy_mpf, (r, i))
        if r.is_Real and r not in [S.Infinity, S.NegativeInfinity] or r is S.Zero:
            R = float(r)
        else:
            raise CoercionFailed("expected Real object, got %s" % a)

        if i.is_Real and i not in [S.Infinity, S.NegativeInfinity] or i is S.Zero:
            I = float(i)
        else:
            raise CoercionFailed("expected Real object, got %s" % a)

        return complex(R, I)

    def from_ZZ_python(K1, a, K0):
        """Convert a Python `int` object to `dtype`. """
        return K1.dtype(a)

    def from_QQ_python(K1, a, K0):
        """Convert a Python `Fraction` object to `dtype`. """
        return K1.dtype(a.numerator) / a.denominator

    def from_ZZ_sympy(K1, a, K0):
        """Convert a SymPy `Integer` object to `dtype`. """
        return K1.dtype(a.p)

    def from_QQ_sympy(K1, a, K0):
        """Convert a SymPy `Rational` object to `dtype`. """
        return K1.dtype(a.p) / a.q

    def from_ZZ_gmpy(K1, a, K0):
        """Convert a GMPY `mpz` object to `dtype`. """
        return K1.dtype(int(a))

    def from_QQ_gmpy(K1, a, K0):
        """Convert a GMPY `mpq` object to `dtype`. """
        return K1.dtype(int(a.numer())) / int(a.denom)

    def from_RR_sympy(K1, a, K0):
        """Convert a SymPy `Real` object to `dtype`. """
        return K1.dtype(a)

    def from_RR_mpmath(K1, a, K0):
        """Convert a mpmath `mpf` object to `dtype`. """
        return K1.dtype(a)

    def from_FF_float(K1, a, K0):
        return K1.dtype(a)

    def real(self, a):
        return a.real

    def imag(self, a):
        return a.imag

