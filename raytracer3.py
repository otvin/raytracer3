import numpy as np
import math


class RT_Tuple:
    def __init__(self, x, y, z, a):
        self.arr = np.array([x, y, z, a])

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
    def a(self):
        return self.arr[3]

    @a.setter
    def a(self, a):
        self.arr[3] = a

    def __eq__(self, other):
        return np.allclose(self.arr, other.arr)

    def ispoint(self):
        return math.isclose(self.a, 1.0)

    def isvector(self):
        return math.isclose(self.a, 0.0)





class Point(RT_Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 1.0)


class Vector(RT_Tuple):
    def __init__(self, x, y, z):
        super().__init__(x, y, z, 0.0)


def render():
    pass


if __name__ == '__main__':
    render()
