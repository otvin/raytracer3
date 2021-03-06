import math
import random
from .matrices import allclose4x1


class RT_Tuple(object):
    __slots__ = ['arr']

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.arr = [x, y, z, w]

    def __str__(self):
        return 'Tuple({})'.format(self.arr)

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
        return allclose4x1(self.arr, other.arr)

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
        a0 = self.arr[0]
        a1 = self.arr[1]
        a2 = self.arr[2]
        return math.sqrt(a0 * a0 + a1 * a1 + a2 * a2)

    def magnitudesquared(self):
        a0 = self.arr[0]
        a1 = self.arr[1]
        a2 = self.arr[2]
        return a0 * a0 + a1 * a1 + a2 * a2


class Point(RT_Tuple):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z, 1.0)

    def __str__(self):
        return 'Point({}, {}, {})'.format(self.arr[0], self.arr[1], self.arr[2])


class Vector(RT_Tuple):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z, 0.0)

    def __str__(self):
        return 'Vector({}, {}, {})'.format(self.arr[0], self.arr[1], self.arr[2])


class Color(RT_Tuple):
    def __init__(self, r=0.0, g=0.0, b=0.0):
        super().__init__(r, g, b, 0.0)

    def __str__(self):
        return 'Color({}, {}, {})'.format(self.arr[0], self.arr[1], self.arr[2])

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
    __slots__ = ['origin', 'direction']

    def __init__(self, origin=Point(), direction=Vector()):
        self.origin = origin
        self.direction = direction

    def __str__(self):
        return 'Ray: orig:({}), dir:({})'.format(self.origin.arr, self.direction.arr)

    def at(self, t=0.0):
        return self.origin + (self.direction * t)


def normalize(vec):
    # returns a vector which is the normalized version of self
    mag = vec.magnitude()
    res = vec / mag
    return res


def dot(tup1, tup2):
    # returns dot product of the two tuples
    t1arr = tup1.arr
    t2arr = tup2.arr

    return (t1arr[0] * t2arr[0] + t1arr[1] * t2arr[1] +
            t1arr[2] * t2arr[2] + t1arr[3] * t2arr[3])


def cross(vec1, vec2):
    # cross product of two vectors
    res = Vector()
    v1arr = vec1.arr
    v2arr = vec2.arr
    v10 = v1arr[0]
    v11 = v1arr[1]
    v12 = v1arr[2]
    v20 = v2arr[0]
    v21 = v2arr[1]
    v22 = v2arr[2]

    res.arr = [v11 * v22 - v12 * v21,
               v12 * v20 - v10 * v22,
               v10 * v21 - v11 * v20,
               0.0]
    return res


def reflect(v, n):
    return v - (n * (dot(v, n) * 2))


def tuples_are_close(tup1, tup2, abs_tol=1e-05, rel_tol=1e-05):
    ret = True
    if not math.isclose(tup1.x, tup2.x, abs_tol=abs_tol, rel_tol=rel_tol):
        ret = False
    elif not math.isclose(tup1.y, tup2.y, abs_tol=abs_tol, rel_tol=rel_tol):
        ret = False
    elif not math.isclose(tup1.z, tup2.z, abs_tol=abs_tol, rel_tol=rel_tol):
        ret = False
    return ret


def random_vector():
    return random_vector_range(-1.0, 1.0)


def random_vector_range(rangemin, rangemax):
    return Vector(random.uniform(rangemin, rangemax), random.uniform(rangemin, rangemax),
                  random.uniform(rangemin, rangemax))


def random_unit_vector():
    return normalize(random_vector())


def random_in_unit_disk():
    done = False
    p = None
    while not done:
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        if (x * x) + (y * y) < 1:
            p = Vector(x, y, 0)
            done = True
    return p


def random_in_unit_sphere():
    done = False
    p = None
    while not done:
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        z = random.uniform(-1.0, 1.0)
        if (x * x) + (y * y) + (z * z) < 1:
            p = Vector(x, y, z)
            done = True
    return p