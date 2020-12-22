import numpy as np
import math


class RT_Tuple:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.arr = np.array([x, y, z, w])
        # We will allow creation of tuples with integer arguments, but want to store as floats.
        self.arr = self.arr.astype('float64')

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
        return np.allclose(self.arr, other.arr)

    def __neg__(self):
        res = RT_Tuple()
        res.arr = -self.arr
        return res

    def __iadd__(self, other):
        self.arr = self.arr + other.arr
        return self

    def __add__(self, other):
        res = RT_Tuple()
        res.arr = self.arr + other.arr
        return res

    def __sub__(self, other):
        res = RT_Tuple()
        res.arr = self.arr - other.arr
        return res

    def __mul__(self, other):
        res = RT_Tuple()
        if isinstance(other, RT_Tuple):
            res.arr = self.arr * other.arr
        else:
            res.arr = self.arr * other
        return res

    def __truediv__(self, other):
        res = RT_Tuple()
        if isinstance(other, RT_Tuple):
            res.arr = self.arr / other.arr
        else:
            res.arr = self.arr / other
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
        sqrlenarr = self.arr * self.arr
        sqrlensum = np.sum(sqrlenarr[:3])
        return math.sqrt(sqrlensum)


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


class Ray:
    def __init__(self, origin=Point(), direction=Vector()):
        self.origin = origin
        self.direction = direction

    def at(self, t=0.0):
        return self.origin + (self.direction * t)


def normalize(vec):
    # returns a vector which is the normalized version of self
    res = Vector()
    mag = vec.magnitude()
    res.arr = vec.arr / mag
    return res


def dot(tup1, tup2):
    # returns dot product of the two tuples
    return np.dot(tup1.arr, tup2.arr)


def cross(vec1, vec2):
    # cross product of two vectors
    res = Vector()
    res.arr[:3] = np.cross(vec1.arr[:3], vec2.arr[:3])
    return res


def matrix_mult_tuple(matrix, tup):
    # matrix must be a 4x4
    # TODO: Duplicate code with transformations.transform().  If this is only used for the unit test
    # test_matrix1() then fix the unit test and remove this code
    res = RT_Tuple()
    res.arr = np.matmul(matrix, tup.arr)
    return res
