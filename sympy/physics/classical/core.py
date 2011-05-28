from sympy import *
from copy import deepcopy
import dcm

class Vector:
    '''
    This is the class used to define vectors.  It along with reference frame are the building blocks of pydy.  
    Class attributes include: 
        subscript_indices - a 3 character string used for printing

    '''
    
    subscript_indices = "xyz"

    def __init__(self,mat,frame):
        '''
        This is the constructor for the Vector class.  
        It should only be used in construction of the basis vectors,
        which is part of the reference frame construction.  
        It takes in a SymPy matrix and a frame.  
        '''
        self.args=[[mat,frame]]

    def __str__(self):
        '''
        Printing method.  Uses Vector Attribute subscript_indices.
        '''
        ar = self.args # just to shorten things
        ol = [] # output list, to be concatenated to a string
        for i in range(len(ar)):
            for j in 0,1,2:
                if ar[i][0][j] == 1: # if the coef of the basis vector is 1, we skip the 1
                    if len(ol) != 0: 
                        ol.append(' + ')
                    ol.append( ar[i][1].lower() + self.subscript_indices[j] + '>' )
                elif ar[i][0][j] == -1: # if the coef of the basis vector is -1, we skip the 1
                    if len(ol) != 0:
                        ol.append(' ')
                    ol.append( '- ' + ar[i][1].lower() + self.subscript_indices[j] + '>' )
                elif ar[i][0][j] != 0: 
                    '''
                    If the coefficient of the basis vector is not 1 or -1, 
                    we wrap it in parentheses, for readability.
                    '''
                    if len(ol) != 0:
                        ol.append(' + ')
                    ol.append('(' +  `ar[i][0][j]` + ')*' + ar[i][1].lower() + self.subscript_indices[j] + '>' )
        return ''.join(ol)

    def __repr__(self):
        '''
        Wraps __str__
        '''
        return self.__str__()

    def __add__(self,other):
        '''
        The add operator for Vector. 
        It checks that other is a Vector, otherwise it throws an error.
        '''
        if not(isinstance(other,Vector)): # Rejects adding a scalar to a vector
            raise NameError('cant do that')
        self2 = deepcopy(self)
        for i in range(len(self2.args)):
            for j in range(len(other.args)):
                if self2.args[i][1] == other.args[j][1]:
                    self2.args[i][0] += other.args[j][0]
                else:
                    self2.args += other.args
        return self2

    def __sub__(self,other):
        '''
        The subraction operator. 
        Reuses add and multiplication operations.  
        '''
        return self.__add__(other*-1)

    def __mul__(self,other):
        '''
        Multiplies the Vector by a scalar. 
        Throws an error if another Vector is entered.  
        '''
        if isinstance(other,Vector): # Rejects scalar multiplication of two vectors
            raise NameError('Why u try to mul vecs?')
        self2 = deepcopy(self)
        for i in range(len(self.args)):
            self2.args[i][0] *= other
        return self2
    
    def __rmul__(self,other):
        '''
        This wraps mul. 
        '''
        return self.__mul__(other)
    
    def __div__(self,other):
        '''
        This uses mul and inputs self and 1 divided by other.  
        '''
        return self.__mul__(1/other)

    def dot(self,other):
        '''
        Dot product of two vectors.  
        Wraps around & operator, which is the designated operator for dot.
        '''
        out = 0
        a

    


class ReferenceFrame:
    '''
    ReferenceFrame is a reference frame.
    It will store its basis vectors as attributes, 
    and orientation information to a parent frame,
    or it will be at the top of a tree.
    
    '''
    
    def __init__(self, name='', parent=None):
        '''
        Initialization for 
        '''
        self.name = name
        self.parent = parent
        self.x = Vector(Matrix([1,0,0]),name)
        self.y = Vector(Matrix([0,1,0]),name)
        self.z = Vector(Matrix([0,0,1]),name)
    
    
    def 



