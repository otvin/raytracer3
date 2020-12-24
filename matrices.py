import numpy as np
import math
import tuple


def matmul4x4(a, b):
    c00 = a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0] + a[0][3] * b[3][0]
    c10 = a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0] + a[1][3] * b[3][0]
    c20 = a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0] + a[2][3] * b[3][0]
    c30 = a[3][0] * b[0][0] + a[3][1] * b[1][0] + a[3][2] * b[2][0] + a[3][3] * b[3][0]

    c01 = a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1] + a[0][3] * b[3][1]
    c11 = a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1] + a[1][3] * b[3][1]
    c21 = a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1] + a[2][3] * b[3][1]
    c31 = a[3][0] * b[0][1] + a[3][1] * b[1][1] + a[3][2] * b[2][1] + a[3][3] * b[3][1]

    c02 = a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2] + a[0][3] * b[3][2]
    c12 = a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2] + a[1][3] * b[3][2]
    c22 = a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2] + a[2][3] * b[3][2]
    c32 = a[3][0] * b[0][2] + a[3][1] * b[1][2] + a[3][2] * b[2][2] + a[3][3] * b[3][2]

    c03 = a[0][0] * b[0][3] + a[0][1] * b[1][3] + a[0][2] * b[2][3] + a[0][3] * b[3][3]
    c13 = a[1][0] * b[0][3] + a[1][1] * b[1][3] + a[1][2] * b[2][3] + a[1][3] * b[3][3]
    c23 = a[2][0] * b[0][3] + a[2][1] * b[1][3] + a[2][2] * b[2][3] + a[2][3] * b[3][3]
    c33 = a[3][0] * b[0][3] + a[3][1] * b[1][3] + a[3][2] * b[2][3] + a[3][3] * b[3][3]

    return [[c00, c01, c02, c03], [c10, c11, c12, c13], [c20, c21, c22, c23], [c30, c31, c32, c33]]


def identity4():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def transpose4x4(a):
    return [[a[0][0], a[1][0], a[2][0], a[3][0]],
            [a[0][1], a[1][1], a[2][1], a[3][1]],
            [a[0][2], a[1][2], a[2][2], a[3][2]],
            [a[0][3], a[1][3], a[2][3], a[3][3]]]


def inverse4x4(a):
    arr = np.array(a)
    inv = np.linalg.inv(arr)
    return inv.tolist()


def matmul4x1(a, b):
    c0 = a[0][0] * b[0] + a[0][1] * b[1] + a[0][2] * b[2] + a[0][3] * b[3]
    c1 = a[1][0] * b[0] + a[1][1] * b[1] + a[1][2] * b[2] + a[1][3] * b[3]
    c2 = a[2][0] * b[0] + a[2][1] * b[1] + a[2][2] * b[2] + a[2][3] * b[3]
    c3 = a[3][0] * b[0] + a[3][1] * b[1] + a[3][2] * b[2] + a[3][3] * b[3]

    return [c0, c1, c2, c3]


def matmul4xTuple(a, tup):
    res = tuple.RT_Tuple()
    res.arr = matmul4x1(a, tup.arr)
    return res


def allclose4x4(a, b):
    return math.isclose(a[0][0], b[0][0], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[0][1], b[0][1], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[0][2], b[0][2], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[0][3], b[0][3], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[1][0], b[1][0], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[1][1], b[1][1], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[1][2], b[1][2], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[1][3], b[1][3], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[2][0], b[2][0], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[2][1], b[2][1], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[2][2], b[2][2], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[2][3], b[2][3], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[3][0], b[3][0], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[3][1], b[3][1], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[3][2], b[3][2], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[3][3], b[3][3], rel_tol=1e-05, abs_tol=1e-05)


def allclose1x1(a, b):
    return math.isclose(a[0], b[0], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[1], b[1], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[2], b[2], rel_tol=1e-05, abs_tol=1e-05) and \
        math.isclose(a[3], b[3], rel_tol=1e-05, abs_tol=1e-05)
