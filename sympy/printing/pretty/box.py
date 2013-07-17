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

class MultiBox(Box):
    pass

class HorizMultiBox(MultiBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.args = (left, right)
        self.width = left.width + right.width
        self.height = max(left.height, right.height)

    def __str__(self):
        # Thoughts: '\n'.join([''.join(i) for i in zip(*a.split('\n'))]) will
        # "transpose" a string, for example
        # >>> print a
        # 123
        # 456
        # >>> print '\n'.join([''.join(i) for i in zip(*a.split('\n'))])
        # 14
        # 25
        # 36
        leftstr = str(self.left)
        rightstr = str(self.right)


class VertMultiBox(MultiBox):
    def __init__(self, bottom, top):
        self.bottom = bottom
        self.top = top
        self.args = (bottom, top)
        self.width = max(bottom.width, top.width)
        self.height = bottom.height + top.height

    def __str__(self):
        topstr = str(self.top).split('\n')
        botstr = str(self.bottom).split('\n')
        bigger = max(['top', 'bottom'], key=lambda i: getattr(self, i).width)
        topstr = [line + ' '*(self.width - self.top.width) for line in topstr]
        botstr = [line + ' '*(self.width - self.bottom.width) for line in botstr]
        if bigger == 'bottom':
            topstr = topstr[:-1]
            botstr[0] = botstr[0][:self.top.width+1] + '+' + botstr[0][self.top.width+2:]
        else:
            botstr = botstr[1:]
            topstr[-1] = topstr[-1][:self.bottom.width+1] + '+' + topstr[-1][self.bottom.width+2:]
        return '\n'.join(topstr + botstr)
