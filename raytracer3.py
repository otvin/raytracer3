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

    def ispoint(self):
        return math.isclose(self.w, 1.0)

    def isvector(self):
        return math.isclose(self.w, 0.0)





class Point(RT_Tuple):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z, 1.0)


class Vector(RT_Tuple):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z, 0.0)


def render():
    pass


if __name__ == '__main__':
    render()
