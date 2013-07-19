from itertools import izip_longest
import operator

class Box(object):
    def __init__(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("width and height must be >= 0")
        self.width = width
        self.height = height
        self.args = (width, height)

    def __repr__(self):
        return "%s%r" % (self.__class__.__name__, self.args)

    def __str__(self):
        top = '+' + '-'*(self.width) + '+'
        mid = '|' + ' '*(self.width) + '|'
        return '\n'.join([top] + [mid]*(self.height) + [top])

    def transpose(self):
        return self.__class__(self.args[1], self.args[0])

    def __invert__(self):
        return self.transpose()

    def stack_right(self, other):
        return HorizMultiBox(self, other)

    def stack_left(self, other):
        return HorizMultiBox(other, self)

    # We use + and ** for horizontal and vertical stacking (respectively)
    # because
    # - It makes typing easier
    # - It is suggestive. + feels like horizontal stacking (e.g., it already
    # does basically this for str), and ** is almost like vertical stacking,
    #                                         2
    # if you think of something like x**2 as x
    # - The precedence of + and ** is well known. No one is going to be
    # surprised by the behavior of x + y ** z, especially if you write it like
    # x + y**z.

    __add__ = stack_right
    __radd__ = stack_left

    def stack_top(self, other):
        return VertMultiBox(self, other)

    def stack_bottom(self, other):
        return VertMultiBox(other, self)

    __pow__ = stack_top
    __rpow__ = stack_bottom

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return reduce(operator.add, other*[self], EmptyBox())

    __rmul__ = __mul__

def mergerows(row1, row2):
    newrow = [max(c1, c2, key=boxkey) for c1, c2 in izip_longest(row1,
        row2, fillvalue=' ')]
    return ''.join(newrow)


class HorizMultiBox(Box):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.args = (left, right)
        self.width = left.width + right.width
        self.height = max(left.height, right.height)

    def __str__(self):
        leftstr = str(self.left)
        rightstr = str(self.right)
        # Now transpose, so left becomes top, and right becomes bottom
        topstrl = strtranspose(leftstr).split('\n')
        botstrl = strtranspose(rightstr).split('\n')
        middle = mergerows(topstrl[-1], botstrl[0])
        return strtranspose('\n'.join(topstrl[:-1] + [middle] + botstrl[1:]))

    def transpose(self):
        return VertMultiBox(self.args[1].transpose(), self.args[0].transpose())

class VertMultiBox(Box):
    def __init__(self, bottom, top):
        self.bottom = bottom
        self.top = top
        self.args = (bottom, top)
        self.width = max(bottom.width, top.width)
        self.height = bottom.height + top.height

    def __str__(self):
        topstrl = str(self.top).split('\n')
        botstrl = str(self.bottom).split('\n')
        middle = mergerows(topstrl[-1], botstrl[0])
        return '\n'.join(topstrl[:-1] + [middle] + botstrl[1:])

    def transpose(self):
        return HorizMultiBox(self.args[1].transpose(),
            self.args[0].transpose())

def boxkey(item):
    return (
        item == '+',
        item == '|',
        item == '-',
        )

def strtranspose(s):
    r"""
    "transpose" a string, for example

    >>> from sympy.printing.pretty.box import strtranspose
    >>> a = '123\n456'
    >>> print a
    123
    456
    >>> print strtranspose(a)
    14
    25
    36
    """
    return '\n'.join([''.join(i) for i in izip_longest(*s.split('\n'),
        fillvalue=' ')])
