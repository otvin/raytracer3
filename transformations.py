import math
import tuple
import matrices


def transform(mat, tup):
    # returns the result of multiplying a transformation matrix by a tuple.  Result will be a tuple
    res = tuple.RT_Tuple()
    res.arr = matrices.matmul4x1(mat, tup.arr)
    return res


def transformray(mat, ray):
    neworigin = transform(mat, ray.origin)
    newdirection = transform(mat, ray.direction)
    return tuple.Ray(neworigin, newdirection)


def translation(x, y, z):
    # the leading 1.0 makes it a float64
    return [[1.0, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]


def scaling(x, y, z):
    # the 0.0 makes it a float64
    return [[x, 0.0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]


def reflection(acrossx=False, acrossy=False, acrossz=False):
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
    return [[1.0, 0, 0, 0],
            [0, math.cos(theta), -math.sin(theta), 0],
            [0, math.sin(theta), math.cos(theta), 0],
            [0, 0, 0, 1]]


def rotation_y(theta):
    # theta is in radians
    return [[math.cos(theta), 0.0, math.sin(theta), 0],
            [0, 1, 0, 0],
            [-math.sin(theta), 0, math.cos(theta), 0],
            [0, 0, 0, 1]]


def rotation_z(theta):
    # theta is in radians
    return [[math.cos(theta), -math.sin(theta), 0.0, 0],
            [math.sin(theta), math.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]


def skew(xy, xz, yx, yz, zx, zy):
    # xy = skew of x in proportion to y
    # xz = skew of x in proportion to z
    # etc.
    return [[1.0, xy, xz, 0],
            [yx, 1, yz, 0],
            [zx, zy, 1, 0],
            [0, 0, 0, 1]]


def view_transform(from_pt, to_pt, up_vec):
    forward = tuple.normalize(to_pt - from_pt)
    left = tuple.cross(forward, tuple.normalize(up_vec))
    true_up = tuple.cross(left, forward)
    orientation = [left.arr, true_up.arr,
                   [-forward.arr[0], -forward.arr[1], -forward.arr[2], -forward.arr[3]],
                   [0, 0, 0, 1.0]]
    return matrices.matmul4x4(orientation, translation(-from_pt.x, -from_pt.y, -from_pt.z))
