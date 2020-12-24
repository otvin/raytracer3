import math
import matrices


class RT_Tuple:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.arr = [x, y, z, w]

    @property
    def x(self):
        return self.arr[0]

    @x.setter
    def x(self, x):
        self.arr[0] = x

    @property
    def y(self):
        return self.arr[1]

    @y.setter
    def y(self, y):
        self.arr[1] = y

    @property
    def z(self):
        return self.arr[2]

    @z.setter
    def z(self, z):
        self.arr[2] = z

    @property
    def w(self):
        return self.arr[3]

    @w.setter
    def w(self, w):
        self.arr[3] = w

    def __eq__(self, other):
        return matrices.allclose1x1(self.arr, other.arr)

    def __neg__(self):
        res = RT_Tuple()
        res.arr = [-self.arr[0], -self.arr[1], -self.arr[2], -self.arr[3]]
        return res

    def __iadd__(self, other):
        self.arr = [self.arr[0] + other.arr[0], self.arr[1] + other.arr[1],
                    self.arr[2] + other.arr[2], self.arr[3] + other.arr[3]]
        return self

    def __add__(self, other):
        res = RT_Tuple()
        res.arr = [self.arr[0] + other.arr[0], self.arr[1] + other.arr[1],
                   self.arr[2] + other.arr[2], self.arr[3] + other.arr[3]]
        return res

    def __sub__(self, other):
        res = RT_Tuple()
        res.arr = [self.arr[0] - other.arr[0], self.arr[1] - other.arr[1],
                   self.arr[2] - other.arr[2], self.arr[3] - other.arr[3]]
        return res

    def __mul__(self, other):
        res = RT_Tuple()
        if isinstance(other, RT_Tuple):
            res.arr = [self.arr[0] * other.arr[0], self.arr[1] * other.arr[1],
                       self.arr[2] * other.arr[2], self.arr[3] * other.arr[3]]
        else:
            res.arr = [self.arr[0] * other, self.arr[1] * other, self.arr[2] * other, self.arr[3] * other]
        return res

    def __truediv__(self, other):
        res = RT_Tuple()
        if isinstance(other, RT_Tuple):
            res.arr = [self.arr[0] / other.arr[0], self.arr[1] / other.arr[1],
                       self.arr[2] / other.arr[2], self.arr[3] / other.arr[3]]
        else:
            res.arr = [self.arr[0] / other, self.arr[1] / other, self.arr[2] / other, self.arr[3] / other]
        return res

    def ispoint(self):
        return math.isclose(self.w, 1.0)

    def isvector(self):
        return math.isclose(self.w, 0.0)

    def magnitude(self):
        # Had to move this here vs. being in the Vector class, because if you subtract
        # two points, you're supposed to get a Vector.  You do get a Tuple that is a
        # vector, but you do not get a Vector object.  It is possible that we will
        # need to change Point() and Vector() to functions that return Tuples instead
        # of objects of their own.
        return math.sqrt(self.arr[0] * self.arr[0] + self.arr[1] * self.arr[1] +
                         self.arr[2] * self.arr[2] + self.arr[3] * self.arr[3])


class Point(RT_Tuple):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z, 1.0)


class Vector(RT_Tuple):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z, 0.0)


class Color(RT_Tuple):
    def __init__(self, r=0.0, g=0.0, b=0.0):
        super().__init__(r, g, b, 0.0)

    @property
    def r(self):
        return self.arr[0]

    @r.setter
    def r(self, r):
        self.arr[0] = r

    @property
    def g(self):
        return self.arr[1]

    @g.setter
    def g(self, g):
        self.arr[1] = g

    @property
    def b(self):
        return self.arr[2]

    @b.setter
    def b(self, b):
        self.arr[2] = b

    def __mul__(self, other):
        res = Color()
        if isinstance(other, RT_Tuple):
            res.arr = [self.arr[0] * other.arr[0], self.arr[1] * other.arr[1],
                       self.arr[2] * other.arr[2], self.arr[3] * other.arr[3]]
        else:
            res.arr = [self.arr[0] * other, self.arr[1] * other, self.arr[2] * other, self.arr[3] * other]
        return res


# global constant colors
BLACK = Color(0, 0, 0)
WHITE = Color(1, 1, 1)


class Ray:
    def __init__(self, origin=Point(), direction=Vector()):
        self.origin = origin
        self.direction = direction

    def at(self, t=0.0):
        return self.origin + (self.direction * t)


def normalize(vec):
    # returns a vector which is the normalized version of self
    mag = vec.magnitude()
    res = vec / mag
    return res


def dot(tup1, tup2):
    # returns dot product of the two tuples
    return (tup1.arr[0] * tup2.arr[0] + tup1.arr[1] * tup2.arr[1] +
            tup1.arr[2] * tup2.arr[2] + tup1.arr[3] * tup2.arr[3])


def cross(vec1, vec2):
    # cross product of two vectors
    res = Vector()
    res.arr = [vec1.arr[1] * vec2.arr[2] - vec1.arr[2] * vec2.arr[1],
               vec1.arr[2] * vec2.arr[0] - vec1.arr[0] * vec2.arr[2],
               vec1.arr[0] * vec2.arr[1] - vec1.arr[1] * vec2.arr[0],
               0.0]
    return res


def reflect(v, n):
    return v - (n * (dot(v, n) * 2))
