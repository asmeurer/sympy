"""rename this to test_assumptions.py when the old assumptions system is deleted"""
from sympy.core import symbols
from sympy.assumptions import Assume, eliminate_assume
import sympy.assumptions as assumptions

def test_assume():
    x = symbols('x')
    assump = Assume(x, integer=True)
    assert assump.expr == x
    assert assump.key == 'integer'
    assert assump.value == True

def test_False():
    """Test Assume object with False keys"""
    x = symbols('x')
    assump = Assume(x, integer=False)
    assert assump.expr == x
    assert assump.key == 'integer'
    assert assump.value == False

def test_equal():
    """Test for equality"""
    x = symbols('x')
    assert Assume(x, positive=True)  == Assume(x, positive=True)
    assert Assume(x, positive=True)  != Assume(x, positive=False)
    assert Assume(x, positive=False) == Assume(x, positive=False)

def test_eliminate_assumptions():
    a, b, x, y = symbols('abxy')
    assert eliminate_assume(Assume(x, a=True))  == a
    assert eliminate_assume(Assume(x, a=True), symbol=x)  == a
    assert eliminate_assume(Assume(x, a=True), symbol=y)  == None
    assert eliminate_assume(Assume(x, a=False)) == ~a
    assert eliminate_assume(Assume(x, a=False), symbol=y) == None
    assert eliminate_assume(Assume(x, a=True) | Assume(x, b=True)) == a | b
    assert eliminate_assume(Assume(x, a=True) | Assume(x, b=False)) == a | ~b

def test_global():
    """Test for global assumptions"""
    x = symbols('x')
    assumptions.register_global(Assume(x>0))
    assert Assume(x>0) in assumptions.list_global()
    assumptions.remove_global(Assume(x>0))
    assert Assume(x>0) not in assumptions.list_global()
