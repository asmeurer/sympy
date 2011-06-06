
def test_dynamicsymbol():
    x = DynamicSymbol('x')
    xd = DynamicSymbol('xd')
    xdd = DynamicSymbol('xdd')
    y = DynamicSymbol('y')
    yd = DynamicSymbol('yd')
    ydd = DynamicSymbol('ydd')
    t = Symbol('t')
    assert diff(x,t) == xd
    assert diff(2 * x + 4, t) == 2 * xd
    assert diff(2 * x + 4 + y, t) == 2 * xd + yd
    assert diff(2 * x + 4 + y * x, t) == 2 * xd + x * yd + xd * y
    assert diff(2 * x + 4 + y * x, x) == 2 + y
    assert (diff(4 * x**2 + 3 * x + x * y, t) == 3 * xd + x * yd + xd * y +
            8 * x * xd)
    assert (diff(4 * x**2 + 3 * xd + x * y, t) ==  3 * xdd + x * yd + xd * y +
            8 * x * xd)
    assert diff(4 * x**2 + 3 * xd + x * y, xd) == 3
    assert diff(4 * x**2 + 3 * xd + x * y, xdd) == 0


"""
def test_ang_vel():
    A2 = N.orientnew('A2', 'Simple', q4, 2)
    assert N.ang_vel_in(N) == 0
    assert N.ang_vel_in(A) == -q1p*N.z
    assert N.ang_vel_in(B) == -q1p*A.z - q2p*B.x
    assert N.ang_vel_in(C) == -q1p*A.z - q2p*B.x - q3p*B.y
    assert N.ang_vel_in(A2) == -q4p*N.y

    assert A.ang_vel_in(N) == q1p*N.z
    assert A.ang_vel_in(A) == 0
    assert A.ang_vel_in(B) == - q2p*B.x
    assert A.ang_vel_in(C) == - q2p*B.x - q3p*B.y
    assert A.ang_vel_in(A2) == q1p*N.z - q4p*N.y

    assert B.ang_vel_in(N) == q1p*A.z + q2p*A.x
    assert B.ang_vel_in(A) == q2p*A.x
    assert B.ang_vel_in(B) == 0
    assert B.ang_vel_in(C) == -q3p*B.y
    assert B.ang_vel_in(A2) == q1p*A.z + q2p*A.x - q4p*N.y

    assert C.ang_vel_in(N) == q1p*A.z + q2p*A.x + q3p*B.y
    assert C.ang_vel_in(A) == q2p*A.x + q3p*C.y
    assert C.ang_vel_in(B) == q3p*B.y
    assert C.ang_vel_in(C) == 0
    assert C.ang_vel_in(A2) == q1p*A.z + q2p*A.x + q3p*B.y - q4p*N.y

    assert A2.ang_vel_in(N) == q4p*A2.y
    assert A2.ang_vel_in(A) == q4p*A2.y - q1p*N.z
    assert A2.ang_vel_in(B) == q4p*N.y - q1p*A.z - q2p*A.x
    assert A2.ang_vel_in(C) == q4p*N.y - q1p*A.z - q2p*A.x - q3p*B.y
    assert A2.ang_vel_in(A2) == 0


class Vector(object):
    def __init__(self, inlist):
    def __str__(self):
    def __repr__(self):
    def __add__(self, other):
    def __and__(self, other):
    def __div__(self, other):
    def __eq__(self, other):
    def __mul__(self, other):
    def __neg__(self):
    def __rmul__(self, other):
    def __sub__(self, other):
    def __xor__(self, other):
    def dot(self, other):
    def cross(self, other):
    def diff(self, wrt, otherframe):
    def dt(self, otherframe):
    def express(self, otherframe):
    def mag(self):
    def unit(self):

class ReferenceFrame(object):
    def __init__(self, name=''):
    def __iter__(self):
    def __str__(self):
    def __repr__(self):
    def next(self):
    def _common_frame(self,other):
    def ang_vel(self, other):
    def dcm(self, other):
    def orientnew(self, newname, rot_type, amounts, rot_order):
    def orient(self, parent, rot_type, amounts, rot_order):
    def set_ang_vel(self, value, other):
    def x(self):
    def y(self):
    def z(self):
"""
