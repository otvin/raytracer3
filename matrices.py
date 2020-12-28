import numpy as np
import math
import rttuple


def matmul4x4(a, b):
    a0 = a[0]
    a00 = a0[0]
    a01 = a0[1]
    a02 = a0[2]
    a03 = a0[3]
    
    a1 = a[1]
    a10 = a1[0]
    a11 = a1[1]
    a12 = a1[2]
    a13 = a1[3]

    a2 = a[2]
    a20 = a2[0]
    a21 = a2[1]
    a22 = a2[2]
    a23 = a2[3]

    a3 = a[3]
    a30 = a3[0]
    a31 = a3[1]
    a32 = a3[2]
    a33 = a3[3]

    b0 = b[0]
    b00 = b0[0]
    b01 = b0[1]
    b02 = b0[2]
    b03 = b0[3]

    b1 = b[1]
    b10 = b1[0]
    b11 = b1[1]
    b12 = b1[2]
    b13 = b1[3]

    b2 = b[2]
    b20 = b2[0]
    b21 = b2[1]
    b22 = b2[2]
    b23 = b2[3]

    b3 = b[3]
    b30 = b3[0]
    b31 = b3[1]
    b32 = b3[2]
    b33 = b3[3]
    
    c00 = a00 * b00 + a01 * b10 + a02 * b20 + a03 * b30
    c10 = a10 * b00 + a11 * b10 + a12 * b20 + a13 * b30
    c20 = a20 * b00 + a21 * b10 + a22 * b20 + a23 * b30
    c30 = a30 * b00 + a31 * b10 + a32 * b20 + a33 * b30

    c01 = a00 * b01 + a01 * b11 + a02 * b21 + a03 * b31
    c11 = a10 * b01 + a11 * b11 + a12 * b21 + a13 * b31
    c21 = a20 * b01 + a21 * b11 + a22 * b21 + a23 * b31
    c31 = a30 * b01 + a31 * b11 + a32 * b21 + a33 * b31

    c02 = a00 * b02 + a01 * b12 + a02 * b22 + a03 * b32
    c12 = a10 * b02 + a11 * b12 + a12 * b22 + a13 * b32
    c22 = a20 * b02 + a21 * b12 + a22 * b22 + a23 * b32
    c32 = a30 * b02 + a31 * b12 + a32 * b22 + a33 * b32

    c03 = a00 * b03 + a01 * b13 + a02 * b23 + a03 * b33
    c13 = a10 * b03 + a11 * b13 + a12 * b23 + a13 * b33
    c23 = a20 * b03 + a21 * b13 + a22 * b23 + a23 * b33
    c33 = a30 * b03 + a31 * b13 + a32 * b23 + a33 * b33

    return [[c00, c01, c02, c03], [c10, c11, c12, c13], [c20, c21, c22, c23], [c30, c31, c32, c33]]


def identity4():
    return [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def transpose4x4(a):
    a0 = a[0]
    a1 = a[1]
    a2 = a[2]
    a3 = a[3]

    return [[a0[0], a1[0], a2[0], a3[0]],
            [a0[1], a1[1], a2[1], a3[1]],
            [a0[2], a1[2], a2[2], a3[2]],
            [a0[3], a1[3], a2[3], a3[3]]]


def inverse4x4(a):
    arr = np.array(a)
    inv = np.linalg.inv(arr)
    return inv.tolist()


def matmul4x1(a, b):
    a0 = a[0]
    a1 = a[1]
    a2 = a[2]
    a3 = a[3]

    b0 = b[0]
    b1 = b[1]
    b2 = b[2]
    b3 = b[3]

    c0 = a0[0] * b0 + a0[1] * b1 + a0[2] * b2 + a0[3] * b3
    c1 = a1[0] * b0 + a1[1] * b1 + a1[2] * b2 + a1[3] * b3
    c2 = a2[0] * b0 + a2[1] * b1 + a2[2] * b2 + a2[3] * b3
    c3 = a3[0] * b0 + a3[1] * b1 + a3[2] * b2 + a3[3] * b3

    return [c0, c1, c2, c3]


def matmul4xTuple(a, tup):
    res = rttuple.RT_Tuple()
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
