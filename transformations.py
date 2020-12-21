import math
import numpy as np
import tuple


def transform(mat, tup):
    # returns the result of multiplying a transformation matrix by a tuple.  Result will be a tuple
    res = tuple.RT_Tuple();
    res.arr = np.matmul(mat, tup.arr)
    return res


def translation(x, y, z):
    # the leading 1.0 makes it a float64
    return np.array([[1.0, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])


def scaling(x, y, z):
    # the 0.0 makes it a float64
    return np.array([[x, 0.0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])


def reflection(acrossx = False, acrossy = False, acrossz = False):
    scalex = 1.0
    scaley = 1.0
    scalez = 1.0
    if acrossx:
        scalex = -1.0
    if acrossy:
        scaley = -1.0
    if acrossz:
        scalez = -1.0
    return scaling(scalex, scaley, scalez)


def rotation_x(theta):
    # theta is in radians
    return np.array([[1.0, 0, 0, 0],
                     [0, math.cos(theta), -math.sin(theta), 0],
                     [0, math.sin(theta), math.cos(theta), 0],
                     [0, 0, 0, 1]])


def rotation_y(theta):
    # theta is in radians
    return np.array([[math.cos(theta), 0.0, math.sin(theta), 0],
                     [0, 1, 0, 0],
                     [-math.sin(theta), 0, math.cos(theta), 0],
                     [0, 0, 0, 1]])


def rotation_z(theta):
    # theta is in radians
    return np.array([[math.cos(theta), -math.sin(theta), 0.0, 0],
                     [math.sin(theta), math.cos(theta), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def skew(xy, xz, yx, yz, zx, zy):
    # xy = skew of x in proportion to y
    # xz = skew of x in proportion to z
    # etc.
    return np.array([[1.0, xy, xz, 0],
                     [yx, 1, yz, 0],
                     [zx, zy, 1, 0],
                     [0, 0, 0, 1]])
