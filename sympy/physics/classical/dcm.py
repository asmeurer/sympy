from sympy import *

# This will be a class, DCM, which will be used in creating the DCM
# It will store all the DCMs hardcoded

def DCM(self, rot_type='', amounts=[], rot_order=''):
    '''
    Direction Cosine Matrix class
    Used to represent rotations from one frame to another.
    It is seperate because there are a lot of matrices hardcoded.
    Takes in a type of rotation, amount of rotations, and order of rotations.
    '''

    approved_orders = ['123','231','312',132','213', 
            '321',121','131','212','232','313','323','1','2','3','']

    rot_order = str(rot_order).upper() # Now we need to make sure XYZ = 123
    rot_type  = rot_type.upper()
    rot_order = [i.replace('X','1') for i in rot_order]
    rot_order = [i.replace('Y','2') for i in rot_order]
    rot_order = [i.replace('Z','3') for i in rot_order]
    assert rot_order in approved_orders, 'Not approved order'

    if rot_type == 'AXIS':
        raise NotImplementedError('Axis rotation not yet implemented')
    elif rot_type == 'EULER':
        assert len(amounts)==4, 'Euler orietation requires 4 values'
        assert rot_order=='', 'Euler orientation take no rotation order'
        a
    elif rot_type == 'BODY':
        assert len(amounts)==3, 'Body orientation requires 3 values'
        assert len(rot_order)==3, 'Body orientation requires 3 orders'
        a1 = int(rot_order[0])
        a2 = int(rot_order[1])
        a3 = int(rot_order[2])
        return self._rot(a1, angle[0]) * self._rot(a2, angle[1]) * self._rot(a3, angle[2])
    elif rot_type == 'SPACE':
        assert len(amounts)==3, 'Space orientation requires 3 values'
        assert len(rot_order)==3, 'Space orientation requires 3 orders'
        a1 = int(rot_order[0])
        a2 = int(rot_order[1])
        a3 = int(rot_order[2])
        return self._rot(a3, angle[2]) * self._rot(a2, angle[1]) * self._rot(a1, angle[0])
    elif rot_type == 'SIMPLE':
        if (isinstance(amounts,list))|(isinstance(amounts,tuple)):
            assert len(amounts)==1, 'Simple orientation requires 1 value'
        if (isinstance(rot_order,list))|(isinstance(rot_order,tuple)):
            assert len(rot_order)==1, 'Simple orientation requires 1 order'
        a = int(rot_order[0])
        return self._rot(a,amount)
    else:
        raise NotImplementedError('That is not an implemented rotation')


def _rot(self, axis, angle): 
    """
    Returns direction cosine matrix for simple 1,2,3 rotations
    """
    if axis == 1:
        return Matrix([[1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)]])
    elif axis == 2:
        return Matrix([[cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]])
    elif axis == 3:
        return Matrix([[cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]])



