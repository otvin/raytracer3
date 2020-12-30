import math
import time
import os
import raytracer as rt
from .transformations import transform, transformray, translation, scaling, reflection, rotation_x, rotation_y, \
                            rotation_z, skew, view_transform
from .world import prepare_computations, schlick_reflectance
from .canvas import init_canvas, write_pixel, get_canvasdims, pixel_at
from .matrices import allclose4x4
from .lights import lighting
from .objects import EPSILON


def compare_ppms(file1, file2):
    # now compare the file we wrote here to the good file that is saved locally
    f = open(file1, 'r')
    f1 = open(file2, 'r')

    fline = f.readline()
    f1line = f1.readline()
    linenumber = 1

    while fline != '' or f1line != '':
        assert fline == f1line, "file difference in line {}".format(linenumber)
        fline = f.readline()
        f1line = f1.readline()
        linenumber += 1

    f.close()
    f1.close()


def default_world():
    s1 = rt.Sphere(material = rt.Material(rt.Color(0.8, 1.0, 0.6), 0.1, 0.7, 0.2, 200))
    s2 = rt.Sphere()
    s2.transform = rt.scaling(0.5, 0.5, 0.5)
    light = rt.PointLight(rt.Point(-10, 10, -10), rt.Color(1, 1, 1))
    w = rt.World([s1, s2], [light])
    return w


def glass_sphere():
    # helper function for refraction tests
    s = rt.Sphere()
    s.material.transparency = 1.0
    s.material.refractive_index = 1.5
    return s




def rtunittest_point1():
    # A tuple with w=1.0 is a point
    t = rt.RT_Tuple(4.3, -4.2, 3.1, 1.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert t.ispoint()
    assert not t.isvector()


def rtunittest_vector1():
    # A tuple with w=0 is a vector
    t = rt.RT_Tuple(4.3, -4.2, 3.1, 0.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert not t.ispoint()
    assert t.isvector()


def rtunittest_point2():
    # Point() creates tuples with w=1
    p = rt.Point(4.0, -4.0, 3.0)
    assert isinstance(p, rt.RT_Tuple)
    assert p == rt.RT_Tuple(4.0, -4.0, 3.0, 1.0)


def rtunittest_vector2():
    # Vector() creates tuples with w=0
    p = rt.Vector(4, -4, 3)
    assert isinstance(p, rt.RT_Tuple)
    assert p == rt.RT_Tuple(4.0, -4.0, 3.0, 0.0)


def rtunittest_add1():
    # Adding two tuples
    p1 = rt.RT_Tuple(3, -2, 5, 1)
    p2 = rt.RT_Tuple(-2, 3, 1, 0)
    assert p1 + p2 == rt.RT_Tuple(1, 1, 6, 1)


def rtunittest_sub1():
    # Subtracting two points
    p1 = rt.Point(3, 2, 1)
    p2 = rt.Point(5, 6, 7)
    assert p1 - p2 == rt.Vector(-2, -4, -6)


def rtunittest_sub2():
    # Subtracting a vector from a point
    p = rt.Point(3, 2, 1)
    v = rt.Vector(5, 6, 7)
    assert p - v == rt.Point(-2, -4, -6)


def rtunittest_sub3():
    # Subtracting two vectors
    v1 = rt.Vector(3, 2, 1)
    v2 = rt.Vector(5, 6, 7)
    assert v1 - v2 == rt.Vector(-2, -4, -6)


def rtunittest_negation1():
    # Subtracting a vector from the zero vector
    zero = rt.Vector(0, 0, 0)
    v = rt.Vector(1, -2, 3)
    assert zero - v == rt.Vector(-1, 2, -3)


def rtunittest_negation2():
    # Negating a tuple
    a = rt.RT_Tuple(1, -2, 3, -4)
    assert -a == rt.RT_Tuple(-1, 2, -3, 4)


def rtunittest_scalarmult1():
    # Multiplying a tuple by a scalar
    a = rt.RT_Tuple(1, -2, 3, -4)
    assert a * 3.5 == rt.RT_Tuple(3.5, -7, 10.5, -14)


def rtunittest_scalarmult2():
    # Multiplying a tuple by a fraction
    a = rt.RT_Tuple(1, -2, 3, -4)
    assert a * 0.5 == rt.RT_Tuple(0.5, -1, 1.5, -2)


def rtunittest_tuplemult1():
    # Multiplying a tuple by a tuple
    a = rt.RT_Tuple(2, 3, 4, 5)
    b = rt.RT_Tuple(0.5, 4, -1.2, 1.5)
    assert a * b == rt.RT_Tuple(1, 12, -4.8, 7.5)


def rtunittest_scalardiv1():
    # Dividing a tuple by a scalar
    a = rt.RT_Tuple(1, -2, 3, -4)
    assert a / 2 == rt.RT_Tuple(0.5, -1, 1.5, -2)


def rtunittest_tuplediv1():
    # Dividing a tuple by a tuple
    a = rt.RT_Tuple(3, 4, 5, 6)
    b = rt.RT_Tuple(1, 2, -2.5, 4)
    assert a / b == rt.RT_Tuple(3, 2, -2, 1.5)


def rtunittest_magnitude1():
    # Computing the magnitude of vector (1,0,0)
    v = rt.Vector(1, 0, 0)
    assert v.magnitude() == 1


def rtunittest_magnitude2():
    # Computing the magnitude of vector (0,1,0)
    v = rt.Vector(0, 1, 0)
    assert v.magnitude() == 1


def rtunittest_magnitude3():
    # Computing the magnitude of vector (0,0,1)
    v = rt.Vector(0, 0, 1)
    assert v.magnitude() == 1


def rtunittest_magnitude4():
    # Computing the magnitude of vector (1,2,3)
    v = rt.Vector(1, 2, 3)
    assert v.magnitude() == math.sqrt(14)


def rtunittest_magnitude5():
    # Computing the magnitude of vector (-1, -2, -3)
    v = rt.Vector(-1, -2, -3)
    assert v.magnitude() == math.sqrt(14)


def rtunittest_normalize1():
    # Normalizing vector (4,0,0) gives (1,0,0)
    v = rt.Vector(4, 0, 0)
    assert rt.normalize(v) == rt.Vector(1, 0, 0)


def rtunittest_normalize2():
    # Normalizing vector (1, 2, 3)
    v = rt.Vector(1, 2, 3)
    assert rt.normalize(v) == rt.Vector(0.26726, 0.53452, 0.80178)


def rtunittest_dot1():
    # The dot product of two tuples
    a = rt.RT_Tuple(1, 2, 3)
    b = rt.RT_Tuple(2, 3, 4)
    assert rt.dot(a, b) == 20


def rtunittest_cross1():
    # The cross product of two vectors
    a = rt.Vector(1, 2, 3)
    b = rt.Vector(2, 3, 4)
    assert rt.cross(a, b) == rt.Vector(-1, 2, -1)
    assert rt.cross(b, a) == rt.Vector(1, -2, 1)


def rtunittest_color1():
    # Adding colors
    c1 = rt.Color(0.9, 0.6, 0.75)
    c2 = rt.Color(0.7, 0.1, 0.25)
    assert c1 + c2 == rt.Color(1.6, 0.7, 1.0)


def rtunittest_color2():
    # Subtracting colors
    c1 = rt.Color(0.9, 0.6, 0.75)
    c2 = rt.Color(0.7, 0.1, 0.25)
    assert c1 - c2 == rt.Color(0.2, 0.5, 0.5)


def rtunittest_color3():
    # Multiplying a color by a scalar
    c = rt.Color(0.2, 0.3, 0.4)
    assert c * 2 == rt.Color(0.4, 0.6, 0.8)


def rtunittest_color4():
    # Mutiplying colors
    c1 = rt.Color(1, 0.2, 0.4)
    c2 = rt.Color(0.9, 1, 0.1)
    assert c1 * c2 == rt.Color(0.9, 0.2, 0.04)


def rtunittest_canvas1():
    # Creating a canvas

    init_canvas(10, 20)
    w, h = get_canvasdims()
    assert w == 10
    assert h == 20
    black = rt.Color(0, 0, 0)
    for w in range(10):
        for h in range(20):
            assert pixel_at(w, h) == black


def rtunittest_canvas2():
    # Writing pixels to a canvas
    init_canvas(10, 20)
    red = rt.Color(1, 0, 0)
    write_pixel(2, 3, red)
    assert pixel_at(2, 3) == red


def rtunittest_canvas3():
    # This is the final exercise from chapter 2; will test the ppm generated against a "good" ppm.
    # Note I use different variables, etc, but still get the parabola.
    init_canvas(900, 550)
    gravity = rt.Vector(0, -0.1, 0)
    wind = rt.Vector(-0.01, 0, 0)
    velocity = rt.normalize(rt.Vector(1, 1.8, 0)) * 11.25
    red = rt.Color(1, 0, 0)
    position = rt.Point(0, 1, 0)

    while 0 <= position.x <= 900 and 0 <= position.y <= 550:
        write_pixel(int(position.x), int(position.y), red)
        position += velocity
        velocity = velocity + (gravity + wind)  # parens stop Pycharm from complaining about wrong type for gravity.

    rt.canvas_to_ppm('test_canvas3.ppm')
    compare_ppms('test_canvas3.ppm', 'raytracer/test_canvas3_success.ppm')
    os.remove('test_canvas3.ppm')


def rtunittest_matrix1():
    # A matrix mutliplied by a tuple
    A = [[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]]
    b = rt.RT_Tuple(1, 2, 3, 1)
    assert rt.matmul4xTuple(A, b) == rt.RT_Tuple(18, 24, 33, 1)


def rtunittest_matrices():
    # Replaced numpy as straight Python was faster

    A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    B = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    assert allclose4x4(A, B)

    A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    B = [[2, 3, 4, 5], [6, 7, 8, 9], [8, 7, 6, 5], [4, 3, 2, 1]]
    assert (not allclose4x4(A, B))

    A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    B = [[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]]
    res = [[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]]
    assert allclose4x4(rt.matmul4x4(A, B), res)

    A = [[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]]
    assert allclose4x4(rt.matmul4x4(A, rt.identity4()), A)

    A = [[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]]
    AT = [[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]]
    assert allclose4x4(rt.transpose4x4(A), AT)

    '''
    A = np.array([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
    assert math.isclose(np.linalg.det(A), -2120)

    A = np.array([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
    assert math.isclose(np.linalg.det(A), 0)
    '''

    A = [[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]]
    res = [[0.21805, 0.45113, 0.24060, -0.04511],
           [-0.80827, -1.45677, -0.44361, 0.52068],
           [-0.07895, -0.22368, -0.05263, 0.19737],
           [-0.52256, -0.81391, -0.30075, 0.30639]]
    B = rt.inverse4x4(A)
    assert allclose4x4(B, res)
    assert math.isclose(B[3][2], -160.0/532.0)
    assert math.isclose(B[2][3], 105.0/532.0)
    assert allclose4x4(rt.matmul4x4(A, B), rt.identity4())

    A = [[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]]
    B = [[8, 2, 2, 2], [3, -1, 7, 0], [7, 0, 5, 4], [6, -2, 0, 5]]
    C = rt.matmul4x4(A, B)
    assert allclose4x4(rt.matmul4x4(C, rt.inverse4x4(B)), A)


def rtunittest_translation1():
    # Multiplying by a translation matrix
    trans = translation(5, -3, 2)
    p = rt.Point(-3, 4, 5)
    assert transform(trans, p) == rt.Point(2, 1, 7)


def rtunittest_translation2():
    # Multiplying by the inverse of a translation matrix
    trans = translation(5, -3, 2)
    inv = rt.inverse4x4(trans)
    p = rt.Point(-3, 4, 5)
    assert transform(inv, p) == rt.Point(-8, 7, 3)


def rtunittest_translation3():
    # Translation does not affect vectors
    trans = translation(5, -3, 2)
    v = rt.Vector(-3, 4, 5)
    assert transform(trans, v) == v


def rtunittest_scaling1():
    # A scaling matrix applied to a point
    trans = scaling(2, 3, 4)
    p = rt.Point(-4, 6, 8)
    assert transform(trans, p) == rt.Point(-8, 18, 32)


def rtunittest_scaling2():
    # A scaling matrix applied to a vector
    trans = scaling(2, 3, 4)
    v = rt.Vector(-4, 6, 8)
    assert transform(trans, v) == rt.Vector(-8, 18, 32)


def rtunittest_scaling3():
    # Multiplying by the inverse of a scaling matrix
    trans = scaling(2, 3, 4)
    inv = rt.inverse4x4(trans)
    v = rt.Vector(-4, 6, 8)
    assert transform(inv, v) == rt.Vector(-2, 2, 2)


def rtunittest_reflection1():
    # Reflection is scaling by a negative value
    trans = reflection(True, False, False)
    p = rt.Point(2, 3, 4)
    assert transform(trans, p) == rt.Point(-2, 3, 4)


def rtunittest_rotation1():
    # Rotating a point around the x axis
    p = rt.Point(0, 1, 0)
    half_quarter = rotation_x(math.pi / 4)
    full_quarter = rotation_x(math.pi / 2)
    assert transform(half_quarter, p) == rt.Point(0, math.sqrt(2)/2, math.sqrt(2)/2)
    assert transform(full_quarter, p) == rt.Point(0, 0, 1)


def rtunittest_rotation2():
    # The inverse of a rotation rotates in the opposite direction
    p = rt.Point(0, 1, 0)
    half_quarter = rotation_x(math.pi / 4)
    inv = rt.inverse4x4(half_quarter)
    assert transform(inv, p) == rt.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2)


def rtunittest_rotation3():
    # Rotating a point around the y axis
    p = rt.Point(0, 0, 1)
    half_quarter = rotation_y(math.pi / 4)
    full_quarter = rotation_y(math.pi / 2)
    assert transform(half_quarter, p) == rt.Point(math.sqrt(2)/2, 0, math.sqrt(2)/2)
    assert transform(full_quarter, p) == rt.Point(1, 0, 0)


def rtunittest_rotation4():
    # Rotating a point around the z axis
    p = rt.Point(0, 1, 0)
    half_quarter = rotation_z(math.pi / 4)
    full_quarter = rotation_z(math.pi / 2)
    assert transform(half_quarter, p) == rt.Point(-math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert transform(full_quarter, p) == rt.Point(-1, 0, 0)


def rtunittest_skew1():
    # A shearing transformation moves x in proportion to y
    trans = skew(1, 0, 0, 0, 0, 0)
    p = rt.Point(2, 3, 4)
    assert transform(trans, p) == rt.Point(5, 3, 4)


def rtunittest_skew2():
    # Several other shearing transformations
    p = rt.Point(2, 3, 4)
    trans1 = skew(0, 1, 0, 0, 0, 0)
    trans2 = skew(0, 0, 1, 0, 0, 0)
    trans3 = skew(0, 0, 0, 1, 0, 0)
    trans4 = skew(0, 0, 0, 0, 1, 0)
    trans5 = skew(0, 0, 0, 0, 0, 1)
    assert transform(trans1, p) == rt.Point(6, 3, 4)
    assert transform(trans2, p) == rt.Point(2, 5, 4)
    assert transform(trans3, p) == rt.Point(2, 7, 4)
    assert transform(trans4, p) == rt.Point(2, 3, 6)
    assert transform(trans5, p) == rt.Point(2, 3, 7)


def rtunittest_transformchain1():
    # Individual transformations are applied in sequence
    p = rt.Point(1, 0, 1)
    A = rotation_x(math.pi / 2)
    B = scaling(5, 5, 5)
    C = translation(10, 5, 7)
    p2 = transform(A, p)
    assert p2 == rt.Point(1, -1, 0)
    p3 = transform(B, p2)
    assert p3 == rt.Point(5, -5, 0)
    p4 = transform(C, p3)
    assert p4 == rt.Point(15, 0, 7)


def rtunittest_transformchain2():
    # CHained transformations must be applied in reverse order
    p = rt.Point(1, 0, 1)
    A = rotation_x(math.pi / 2)
    B = scaling(5, 5, 5)
    C = translation(10, 5, 7)
    T = rt.matmul4x4(rt.matmul4x4(C, B), A)
    assert transform(T, p) == rt.Point(15, 0, 7)


def rtunittest_transformchain3():
    # This is the final exercise from chapter 4.
    halfcanvas = 12
    init_canvas(2 * halfcanvas, 2 * halfcanvas)
    clockradius = int(0.75 * halfcanvas)
    trans = rotation_y(math.pi / 6)

    gold = rt.Color(1, 0.84314, 0)
    p = rt.RT_Tuple(0, 0, 1)  # start at 12 o'clock
    for i in range(13):
        dot = p * clockradius
        write_pixel(int(dot.x) + halfcanvas, int(dot.z) + halfcanvas, gold)
        p = transform(trans, p)

    rt.canvas_to_ppm('test_transformchain3.ppm')
    compare_ppms('test_transformchain3.ppm', 'raytracer/test_transformchain3_success.ppm')
    os.remove('test_transformchain3.ppm')


def rtunittest_ray1():
    # Creating and querying a ray
    origin = rt.Point(1, 2, 3)
    direction = rt.Vector(4, 5, 6)
    r = rt.Ray(origin, direction)
    assert r.origin == origin
    assert r.direction == direction


def rtunittest_ray2():
    # Computing a point from a distance
    r = rt.Ray(rt.Point(2, 3, 4), rt.Vector(1, 0, 0))
    assert r.at(0) == rt.Point(2, 3, 4)
    assert r.at(1) == rt.Point(3, 3, 4)
    assert r.at(-1) == rt.Point(1, 3, 4)
    assert r.at(2.5) == rt.Point(4.5, 3, 4)


def rtunittest_sphereintersect1():
    # A ray intersects a sphere at two points
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 4.0)
    assert math.isclose(xs[1].t, 6.0)


def rtunittest_sphereintersect2():
    # A ray intersects a sphere at a tangent
    r = rt.Ray(rt.Point(0, 1, -5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 5.0)
    assert math.isclose(xs[1].t, 5.0)


def rtunittest_sphereintersect3():
    # A ray misses a sphere
    r = rt.Ray(rt.Point(0, 2, -5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 0


def rtunittest_sphereintersect4():
    # A ray originates inside a sphere
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, -1.0)
    assert math.isclose(xs[1].t, 1.0)


def rtunittest_sphereintersect5():
    # A sphere is behind a ray
    r = rt.Ray(rt.Point(0, 0, 5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, -6.0)
    assert math.isclose(xs[1].t, -4.0)


def rtunittest_intersection1():
    # An intersection encapsulates t and object
    s = rt.Sphere()
    i = rt.Intersection(s, 3.5)
    assert math.isclose(i.t, 3.5)
    assert i.objhit is s


def rtunittest_intersection2():
    # Intersect sets the object on the intersection
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].objhit is s
    assert xs[1].objhit is s


def rtunittest_raytransform1():
    # Translating a ray
    r = rt.Ray(rt.Point(1, 2, 3), rt.Vector(0, 1, 0))
    m = translation(3, 4, 5)
    r2 = transformray(m, r)
    assert r2.origin == rt.Point(4, 6, 8)
    assert r2.direction == rt.Vector(0, 1, 0)


def rtunittest_raytransform2():
    # Scaling a ray
    r = rt.Ray(rt.Point(1, 2, 3), rt.Vector(0, 1, 0))
    m = scaling(2, 3, 4)
    r2 = transformray(m, r)
    assert r2.origin == rt.Point(2, 6, 12)
    assert r2.direction == rt.Vector(0, 3, 0)


def rtunittest_spheretransform1():
    # A sphere's default transformation
    s = rt.Sphere()
    assert allclose4x4(s.transform, rt.identity4())


def rtunittest_spheretransform2():
    # Changing a sphere's transformation
    t = translation(2, 3, 4)
    s = rt.Sphere(t)
    assert allclose4x4(s.transform, t)


def rtunittest_sphereintersect6():
    # Intersecting a scaled sphere with a ray
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    t = scaling(2, 2, 2)
    s = rt.Sphere(t)
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 3.0)
    assert math.isclose(xs[1].t, 7.0)


def rtunittest_sphereintersect7():
    # Intersecting a translated sphere with a ray
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    t = translation(5, 0, 0)
    s = rt.Sphere(t)
    xs = s.intersect(r)
    assert len(xs) == 0


def rtunittest_normalat1():
    # The normal on a sphere at a point on the x axis
    s = rt.Sphere()
    n = s.normal_at(rt.Point(1, 0, 0))
    assert n == rt.Vector(1, 0, 0)


def rtunittest_normalat2():
    # The normal on a sphere at a point on the y axis
    s = rt.Sphere()
    n = s.normal_at(rt.Point(0, 1, 0))
    assert n == rt.Vector(0, 1, 0)


def rtunittest_normalat3():
    # The normal on a sphere at a point on the z axis
    s = rt.Sphere()
    n = s.normal_at(rt.Point(0, 0, 1))
    assert n == rt.Vector(0, 0, 1)


def rtunittest_normalat4():
    # The normal on a sphere at a nonaxial point
    s = rt.Sphere()
    rt3over3 = math.sqrt(3) / 3.0
    n = s.normal_at(rt.Point(rt3over3, rt3over3, rt3over3))
    assert n == rt.Vector(rt3over3, rt3over3, rt3over3)


def rtunittest_normalat5():
    # Computing the normal on a translated sphere
    s = rt.Sphere(translation(0, 1, 0))
    n = s.normal_at(rt.Point(0, 1.70711, -0.70711))
    assert n == rt.Vector(0, 0.70711, -0.70711)


def rtunittest_normalat6():
    # Computing the normal on a transformed sphere
    m = rt.matmul4x4(scaling(1, 0.5, 1), rotation_z(math.pi/5))
    s = rt.Sphere(m)
    n = s.normal_at(rt.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
    assert n == rt.Vector(0, 0.97014, -0.24254)


def rtunittest_reflect1():
    # Reflecting a vector approaching at 45 degrees
    v = rt.Vector(1, -1, 0)
    n = rt.Vector(0, 1, 0)
    assert rt.reflect(v, n) == rt.Vector(1, 1, 0)


def rtunittest_reflect2():
    # Reflecting a vector off a slanted surface
    v = rt.Vector(0, -1, 0)
    n = rt.Vector(math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert rt.reflect(v, n) == rt.Vector(1, 0, 0)


def rtunittest_light1():
    # A point light has a position and intensity
    intensity = rt.Color(1, 1, 1)
    position = rt.Point(0, 0, 0)
    light = rt.PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity


def rtunittest_material1():
    # The default material
    m = rt.Material()
    assert m.color == rt.Color(1, 1, 1)
    assert math.isclose(m.ambient, 0.1)
    assert math.isclose(m.diffuse, 0.9)
    assert math.isclose(m.specular, 0.9)
    assert math.isclose(m.shininess, 200.0)


def rtunittest_spherematerial1():
    # A sphere has a default material
    s = rt.Sphere()
    m = s.material
    assert m == rt.Material()


def rtunittest_spherematerial2():
    # A sphere may be assigned a material
    s = rt.Sphere()
    m = rt.Material()
    m.ambient = 1.0
    s.material = m
    assert s.material is m


def rtunittest_lighting1():
    # Lighting with the eye between the light and the surface
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))
    assert lighting(m, rt.HittableObject(), light, position, eyev, normalv) == rt.Color(1.9, 1.9, 1.9)


def rtunittest_lighting2():
    # Lighting with the eye between light and surface, eye offset 45 degrees
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, math.sqrt(2)/2, -math.sqrt(2)/2)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))
    assert lighting(m, rt.HittableObject(), light, position, eyev, normalv) == rt.Color(1.0, 1.0, 1.0)


def rtunittest_lighting3():
    # Lighting with eye opposite surface, light offset 45 degrees
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 10, -10), rt.Color(1, 1, 1))
    assert lighting(m, rt.HittableObject(), light, position, eyev, normalv) == \
           rt.Color(0.7364, 0.7364, 0.7364)


def rtunittest_lighting4():
    # Lighting with eye in the path of the reflection vector
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, -math.sqrt(2) / 2, -math.sqrt(2) / 2)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 10, -10), rt.Color(1, 1, 1))
    assert lighting(m, rt.HittableObject(), light, position, eyev, normalv) == \
           rt.Color(1.6364, 1.6364, 1.6364)


def rtunittest_lighting5():
    # Lighting with the light behind the surface
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 0, 10), rt.Color(1, 1, 1))
    assert lighting(m, rt.HittableObject(), light, position, eyev, normalv) == rt.Color(0.1, 0.1, 0.1)


def rtunittest_lighting6():
    # Lighting with the surface in shadow
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))
    assert lighting(m, rt.HittableObject(), light, position, eyev, normalv, True) \
           == rt.Color(0.1, 0.1, 0.1)


def rtunittest_world1():
    # Creating a world
    w = rt.World()
    assert len(w.objects) == 0
    assert len(w.lights) == 0


def rtunittest_world2():
    # The default world
    w = default_world()
    assert len(w.objects) == 2
    assert len(w.lights) == 1
    assert w.objects[0].material.color == rt.Color(0.8, 1.0, 0.6)
    assert math.isclose(w.objects[0].material.ambient, 0.1)
    assert math.isclose(w.objects[0].material.diffuse, 0.7)
    assert math.isclose(w.objects[0].material.specular, 0.2)
    assert math.isclose(w.objects[0].material.shininess, 200.0)
    assert isinstance(w.objects[0], rt.Sphere)
    assert allclose4x4(w.objects[1].transform, scaling(0.5, 0.5, 0.5))
    assert isinstance(w.objects[1], rt.Sphere)
    assert isinstance(w.lights[0], rt.Light)
    assert w.lights[0].position == rt.Point(-10, 10, -10)
    assert w.lights[0].intensity == rt.Color(1, 1, 1)


def rtunittest_world3():
    # Intersect a world with a ray
    w = default_world()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    xs = w.intersect(r)
    assert len(xs) == 4
    assert math.isclose(xs[0].t, 4)
    assert math.isclose(xs[1].t, 4.5)
    assert math.isclose(xs[2].t, 5.5)
    assert math.isclose(xs[3].t, 6)


def rtunittest_preparecomputations1():
    # Precomputing the state of an intersection
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    i = rt.Intersection(s, 4)
    comps = prepare_computations(i, r, [i])
    assert math.isclose(comps.t, i.t)
    assert comps.objhit is i.objhit
    assert comps.point == rt.Point(0, 0, -1)
    assert comps.eyev == rt.Vector(0, 0, -1)
    assert comps.normalv == rt.Vector(0, 0, -1)
    assert not comps.inside


def rtunittest_preparecomputations2():
    # The hit, when an intersection occurs on the inside
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    i = rt.Intersection(s, 1)
    comps = prepare_computations(i, r, [i])
    assert comps.point == rt.Point(0, 0, 1)
    assert comps.eyev == rt.Vector(0, 0, -1)
    assert comps.inside
    assert comps.normalv == rt.Vector(0, 0, -1)


def rtunittest_preparecomputations3():
    # The hit should offset the point
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = rt.Sphere()
    s.transform = translation(0, 0, 1)
    i = rt.Intersection(s, 5)
    comps = prepare_computations(i, r, [i])
    assert comps.over_point.z < -EPSILON/2
    assert comps.point.z > comps.over_point.z


def rtunittest_preparecomputations4():
    # Precomputing the reflection vector
    s = rt.Plane()
    r = rt.Ray(rt.Point(0, 1, -1), rt.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    i = rt.Intersection(s, math.sqrt(2))
    comps = prepare_computations(i, r, [i])
    assert comps.reflectv == rt.Vector(0, math.sqrt(2)/2, math.sqrt(2)/2)


def rtunittest_preparecomputations5():
    # The under point is offset below the surface
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    shape = glass_sphere()
    shape.transform = translation(0, 0, 1)
    i = rt.Intersection(shape, 5)
    comps = prepare_computations(i, r, [i])
    assert comps.under_point.z > EPSILON/2
    assert comps.point.z < comps.under_point.z


def rtunittest_shadehit1():
    # Shading an intersection
    w = default_world()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = w.objects[0]
    i = rt.Intersection(s, 4)
    hitrecord = prepare_computations(i, r, [i])
    c = w.shade_hit(hitrecord, 0)
    assert c == rt.Color(0.38066, 0.47583, 0.2855)


def rtunittest_shadehit2():
    # shading an intersection from the inside
    w = default_world()
    light = rt.PointLight(rt.Point(0, 0.25, 0), rt.Color(1, 1, 1))
    w.lights = [light]
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    s = w.objects[1]
    i = rt.Intersection(s, 0.5)
    hitrecord = prepare_computations(i, r, [i])
    c = w.shade_hit(hitrecord, 0)
    assert c == rt.Color(0.90498, 0.90498, 0.90498)


def rtunittest_shadehit3():
    # shade_hit() with a reflective material
    w = default_world()
    s = rt.Plane()
    s.material.reflective = 0.5
    s.transform = translation(0, -1, 0)
    w.objects.append(s)
    r = rt.Ray(rt.Point(0, 0, -3), rt.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    i = rt.Intersection(s, math.sqrt(2))
    comps = prepare_computations(i, r, [i])
    color = w.shade_hit(comps, 1)
    assert color == rt.Color(0.87677, 0.92436, 0.82918)


def rtunittest_colorat1():
    # The color when a ray misses
    w = default_world()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 1, 0))
    c = w.color_at(r, 1)
    assert c == rt.Color(0, 0, 0)


def rtunittest_colorat2():
    # The color when a ray hits
    w = default_world()
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    c = w.color_at(r, 1)
    assert c == rt.Color(0.38066, 0.47583, 0.2855)


def rtunittest_colorat3():
    # The color with an intersection behind the ray
    w = default_world()
    outer = w.objects[0]
    outer.material.ambient = 1.0
    inner = w.objects[1]
    inner.material.ambient = 1.0
    r = rt.Ray(rt.Point(0, 0, 0.75), rt.Vector(0, 0, -1))
    c = w.color_at(r, 1)
    assert c == inner.material.color


def rtunittest_colorat4():
    # Color_at() with mutually reflective surfaces (validate we do not get into an infinite loop)
    w = rt.World()
    w.lights = [rt.PointLight(rt.Point(0, 0, 0), rt.Color(1, 1, 1))]
    lower = rt.Plane()
    lower.material.reflective = 1.0
    lower.transform = translation(0, -1, 0)
    upper = rt.Plane()
    upper.material.reflective = 1.0
    upper.transform = translation(0, 1, 0)
    w.objects = [lower, upper]
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 1, 0))
    w.color_at(r, 5)  # we don't do anything with the return value - we just validate we exit


def rtunittest_viewtransform1():
    # The transformation matrix for the default orientation
    from_pt = rt.Point(0, 0, 0)
    to_pt = rt.Point(0, 0, -1)
    up_vec = rt.Vector(0, 1, 0)
    t = view_transform(from_pt, to_pt, up_vec)
    assert allclose4x4(t, rt.identity4())


def rtunittest_viewtransform2():
    # A view transformation matrix looking in positive z direction
    from_pt = rt.Point(0, 0, 0)
    to_pt = rt.Point(0, 0, 1)
    up_vec = rt.Vector(0, 1, 0)
    t = view_transform(from_pt, to_pt, up_vec)
    assert allclose4x4(t, scaling(-1, 1, -1))


def rtunittest_viewtransform3():
    # The view transformation moves the world
    from_pt = rt.Point(0, 0, 8)
    to_pt = rt.Point(0, 0, 1)
    up_vec = rt.Vector(0, 1, 0)
    t = view_transform(from_pt, to_pt, up_vec)
    assert allclose4x4(t, translation(0, 0, -8))


def rtunittest_viewtransformation4():
    # An arbitrary view transformation
    from_pt = rt.Point(1, 3, 2)
    to_pt = rt.Point(4, -2, 8)
    up_vec = rt.Vector(1, 1, 0)
    t = view_transform(from_pt, to_pt, up_vec)
    res = [[-0.50709, 0.50709, 0.67612, -2.36643],
           [0.76772, 0.60609, 0.12122, -2.82843],
           [-0.35857, 0.59761, -0.71714, 0],
           [0, 0, 0, 1]]
    assert allclose4x4(t, res)


def rtunittest_camera1():
    # Constructing a camera
    c = rt.Camera(160, 120, math.pi/2)
    assert c.hsize == 160
    assert c.vsize == 120
    assert math.isclose(c.field_of_view, math.pi/2)
    assert allclose4x4(c.transform, rt.identity4())


def rtunittest_camera2():
    # The pixel size for a horizontal canvas
    c = rt.Camera(200, 125, math.pi/2)
    assert math.isclose(c.pixel_size, 0.01)


def rtunittest_camera3():
    # The pixel size for a vertical canvas
    c = rt.Camera(125, 200, math.pi/2)
    assert math.isclose(c.pixel_size, 0.01)


def rtunittest_camera4():
    # Constructing a ray through the center of the camera
    c = rt.Camera(201, 101, math.pi/2)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == rt.Point(0, 0, 0)
    assert r.direction == rt.Vector(0, 0, -1)


def rtunittest_camera5():
    # Constructing a ray through the corner of the canvas
    c = rt.Camera(201, 101, math.pi/2)
    r = c.ray_for_pixel(0, 0)
    assert r.origin == rt.Point(0, 0, 0)
    assert r.direction == rt.Vector(0.66519, 0.33259, -0.66851)


def rtunittest_camera6():
    # Constructing a ray when the camera is transformed
    trans = rt.matmul4x4(rotation_y(math.pi/4), translation(0, -2, 5))
    c = rt.Camera(201, 101, math.pi/2, trans)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == rt.Point(0, 2, -5)
    assert r.direction == rt.Vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2)


def rtunittest_render1():
    w = default_world()
    c = rt.Camera(11, 11, math.pi/2)
    fr = rt.Point(0, 0, -5)
    to = rt.Point(0, 0, 0)
    up = rt.Vector(0, 1, 0)
    c.transform = view_transform(fr, to, up)
    rt.mp_render(c, w, 1, 1)
    assert pixel_at(5, 5) == rt.Color(0.38066, 0.47583, 0.2855)


def rtunittest_shadowed1():
    # There is no shadow when nothing is collinear with point and light
    w = default_world()
    p = rt.Point(0, 10, 0)
    assert not w.is_shadowed(p)


def rtunittest_shadowed2():
    # There is no shadow when an object is between the point and the light
    w = default_world()
    p = rt.Point(10, -10, 10)
    assert w.is_shadowed(p)


def rtunittest_shadowed3():
    # There is no shadow when an object is behind the light
    w = default_world()
    p = rt.Point(-20, 20, -20)
    assert not w.is_shadowed(p)


def rtunittest_shadowed4():
    # There is no shadow when an object is behind the point
    w = default_world()
    p = rt.Point(-2, 2, -2)
    assert not w.is_shadowed(p)


def rtunittest_plane1():
    # The normal of a plane is constant everywhere
    p = rt.Plane()
    n1 = p.local_normal_at(rt.Point(0, 0, 0))
    n2 = p.local_normal_at(rt.Point(10, 0, -10))
    n3 = p.local_normal_at(rt.Point(-5, 0, 150))
    assert n1 == rt.Vector(0, 1, 0)
    assert n2 == rt.Vector(0, 1, 0)
    assert n3 == rt.Vector(0, 1, 0)


def rtunittest_plane2():
    # Intersect with a ray parallel to the plane
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, 10, 0), rt.Vector(0, 0, 1))
    xs = p.local_intersect(r)
    assert len(xs) == 0


def rtunittest_plane3():
    # Intersect with a coplanar ray
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    xs = p.local_intersect(r)
    assert len(xs) == 0


def rtunittest_plane4():
    # A ray intersecting a plane from above
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, 1, 0), rt.Vector(0, -1, 0))
    xs = p.local_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].objhit == p


def rtunittest_plane5():
    # A ray intersecting a plane from below
    p = rt.Plane()
    r = rt.Ray(rt.Point(0, -2, 0), rt.Vector(0, 1, 0))
    xs = p.local_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 2
    assert xs[0].objhit == p


def rtunittest_stripepattern1():
    b = rt.Color(0, 0, 0)
    w = rt.Color(1, 1, 1)
    sp = rt.StripePattern(None, w, b)
    assert sp.color1 is w
    assert sp.color2 is b


def rtunittest_stripepattern2():
    # A stripe pattern is constant in y
    b = rt.Color(0, 0, 0)
    w = rt.Color(1, 1, 1)
    sp = rt.StripePattern(None, w, b)
    assert sp.color_at(rt.Point(0, 0, 0)) == w
    assert sp.color_at(rt.Point(0, 1, 0)) == w
    assert sp.color_at(rt.Point(0, 2, 0)) == w


def rtunittest_stripepattern3():
    # A stripe pattern is constant in z
    b = rt.Color(0, 0, 0)
    w = rt.Color(1, 1, 1)
    sp = rt.StripePattern(None, w, b)
    assert sp.color_at(rt.Point(0, 0, 1)) == w
    assert sp.color_at(rt.Point(0, 0, 2)) == w


def rtunittest_stripepattern4():
    # A stripe pattern alternates in x
    b = rt.Color(0, 0, 0)
    w = rt.Color(1, 1, 1)
    sp = rt.StripePattern(None, w, b)

    assert sp.color_at(rt.Point(0.9, 0, 0)) == w
    assert sp.color_at(rt.Point(1, 0, 0)) == b
    assert sp.color_at(rt.Point(-0.1, 0, 0)) == b
    assert sp.color_at(rt.Point(-1, 0, 0)) == b
    assert sp.color_at(rt.Point(-1.1, 0, 0)) == w


def rtunittest_stripepattern5():
    # Lighting with a pattern applied
    b = rt.Color(0, 0, 0)
    w = rt.Color(1, 1, 1)
    sp = rt.StripePattern(None, w, b)

    m = rt.Material()
    m.ambient = 1
    m.diffuse = 0
    m.specular = 0
    m.pattern = sp

    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)

    light = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))

    c1 = lighting(m, rt.HittableObject(), light, rt.Point(0.9, 0, 0), eyev, normalv, False)
    c2 = lighting(m, rt.HittableObject(), light, rt.Point(1.1, 0, 0), eyev, normalv, False)

    assert c1 == w
    assert c2 == b


def rtunittest_checkerspattern1():
    b = rt.Color(0, 0, 0)
    w = rt.Color(1, 1, 1)
    cp = rt.CheckersPattern(None, w, b)

    assert cp.color_at(rt.Point(0, 0, 0)) == w
    assert cp.color_at(rt.Point(0.99, 0, 0)) == w
    assert cp.color_at(rt.Point(1.01, 0, 0)) == b
    assert cp.color_at(rt.Point(0, 0.99, 0)) == w
    assert cp.color_at(rt.Point(0, 1.01, 0)) == b
    assert cp.color_at(rt.Point(0, 0, 0.99)) == w
    assert cp.color_at(rt.Point(0, 0, 1.01)) == b


def rtunittest_reflective1():
    m = rt.Material()
    assert math.isclose(m.reflective, 0)


def rtunittest_reflective2():
    # The reflected color for a non-reflective material
    w = default_world()
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    shape = w.objects[1]
    shape.material.ambient = 1
    i = rt.Intersection(shape, 1)
    comps = prepare_computations(i, r, [i])
    color = w.reflected_color(comps, 1)
    assert color == rt.Color(0, 0, 0)


def rtunittest_reflective3():
    # The reflected color for a reflective material
    w = default_world()
    s = rt.Plane()
    s.material.reflective = 0.5
    s.transform = translation(0, -1, 0)
    w.objects.append(s)
    r = rt.Ray(rt.Point(0, 0, -3), rt.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    i = rt.Intersection(s, math.sqrt(2))
    comps = prepare_computations(i, r, [i])
    color = w.reflected_color(comps, 1)
    assert color == rt.Color(0.19034, 0.23793, 0.14276)  # I had to change the numbers from the book


def rtunittest_reflective4():
    # The reflected color at the maximum recursive depth
    w = default_world()
    s = rt.Plane()
    s.material.reflective = 0.5
    s.transform = translation(0, -1, 0)
    w.objects.append(s)
    r = rt.Ray(rt.Point(0, 0, -3), rt.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    i = rt.Intersection(s, math.sqrt(2))
    comps = prepare_computations(i, r, [i])
    color = w.reflected_color(comps, 0)
    assert color == rt.Color(0, 0, 0)


def rtunittest_refraction1():
    m = rt.Material()
    assert math.isclose(m.transparency, 0.0)
    assert math.isclose(m.refractive_index, 1.0)


def rtunittest_refraction2():
    A = glass_sphere()
    A.transform = scaling(2, 2, 2)
    B = glass_sphere()
    B.transform = translation(0, 0, -0.25)
    B.material.refractive_index = 2.0
    C = glass_sphere()
    C.transform = translation(0, 0, 0.25)
    C.material.refractive_index = 2.5

    r = rt.Ray(rt.Point(0, 0, -4), rt.Vector(0, 0, 1))

    xs = [rt.Intersection(A, 2), rt.Intersection(B, 2.75), rt.Intersection(C, 3.25),
          rt.Intersection(B, 4.75), rt.Intersection(C, 5.25), rt.Intersection(A, 6)]

    n1answers = [1.0, 1.5, 2.0, 2.5, 2.5, 1.5]
    n2answers = [1.5, 2.0, 2.5, 2.5, 1.5, 1.0]

    for i in range(len(xs)):
        comps = prepare_computations(xs[i], r, xs)
        assert math.isclose(comps.n1, n1answers[i])
        assert math.isclose(comps.n2, n2answers[i])


def rtunittest_refraction3():
    # The refracted color with an opaque surface
    w = default_world()
    s = w.objects[0]
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    xs = [rt.Intersection(s, 4), rt.Intersection(s, 6)]
    comps = prepare_computations(xs[0], r, xs)
    c = w.refracted_color(comps, 5)
    assert c == rt.Color(0, 0, 0)


def rtunittest_refraction4():
    # The refracted color at the maximum recursive depth
    w = default_world()
    s = w.objects[0]
    s.material.transparency = 1.0
    s.material.refractive_index = 1.5
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    xs = [rt.Intersection(s, 4), rt.Intersection(s, 6)]
    comps = prepare_computations(xs[0], r, xs)
    c = w.refracted_color(comps, 0)
    assert c == rt.Color(0, 0, 0)


def rtunittest_refraction5():
    # The refracted color under total internal reflection
    w = default_world()
    s = w.objects[0]
    s.material.transparency = 1.0
    s.material.refractive_index = 1.5
    r = rt.Ray(rt.Point(0, 0, -math.sqrt(2)/2), rt.Vector(0, 1, 0))
    xs = [rt.Intersection(s, -math.sqrt(2)/2), rt.Intersection(s, math.sqrt(2)/2)]
    # because we're inside the sphere we look at second intersection
    comps = prepare_computations(xs[1], r, xs)
    c = w.refracted_color(comps, 5)
    assert c == rt.Color(0, 0, 0)


def rtunittest_refraction6():
    # The refracted color with a refracted ray
    w = default_world()
    A = w.objects[0]
    A.material.ambient = 1.0
    A.material.pattern = rt.TestPattern()
    B = w.objects[1]
    B.material.transparency = 1.0
    B.material.refractive_index = 1.5
    r = rt.Ray(rt.Point(0, 0, 0.1), rt.Vector(0, 1, 0))
    xs = [rt.Intersection(A, -0.9899), rt.Intersection(B, -0.4899),
          rt.Intersection(B, 0.4899), rt.Intersection(A, 0.9899)]
    comps = prepare_computations(xs[2], r, xs)
    c = w.refracted_color(comps, 5)
    assert c == rt.Color(0, 0.99888, 0.04725)


def rtunittest_refraction7():
    # shade_hit() with a transparent material
    w = default_world()
    floor = rt.Plane()
    floor.transform = translation(0, -1, 0)
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.objects.append(floor)

    ball = rt.Sphere()
    ball.material.color = rt.Color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = translation(0, -3.5, -0.5)
    w.objects.append(ball)

    r = rt.Ray(rt.Point(0, 0, -3), rt.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
    xs = [rt.Intersection(floor, math.sqrt(2))]
    comps = prepare_computations(xs[0], r, xs)
    color = w.shade_hit(comps, 5)
    assert color == rt.Color(0.93642, 0.68642, 0.68642)


def rtunittest_schlick1():
    # The Schlick approximation under total internal reflection
    s = glass_sphere()
    r = rt.Ray(rt.Point(0, 0, math.sqrt(2)/2), rt.Vector(0, 1, 0))
    xs = [rt.Intersection(s, -math.sqrt(2)/2), rt.Intersection(s, math.sqrt(2)/2)]
    comps = prepare_computations(xs[1], r, xs)
    assert math.isclose(schlick_reflectance(comps), 1.0)


def rtunittest_schlick2():
    # The Schlick approximation with a perpendicular viewing angle
    s = glass_sphere()
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 1, 0))
    xs = [rt.Intersection(s, -1), rt.Intersection(s, 1)]
    comps = prepare_computations(xs[1], r, xs)
    assert math.isclose(schlick_reflectance(comps), 0.04)


def rtunittest_schlick3():
    # The Schlick approximation with small angle and n2 > n1
    s = glass_sphere()
    r = rt.Ray(rt.Point(0, 0.99, -2), rt.Vector(0, 0, 1))
    xs = [rt.Intersection(s, 1.8589)]
    comps = prepare_computations(xs[0], r, xs)
    s_r = schlick_reflectance(comps)
    assert math.isclose(s_r, 0.48873, rel_tol=1e-05, abs_tol=1e-05)


def rtunittest_schlick4():
    # shade_hit() with a reflective, transparent material
    w = default_world()
    r = rt.Ray(rt.Point(0, 0, -3), rt.Vector(0, -math.sqrt(2) / 2, math.sqrt(2) / 2))

    floor = rt.Plane()
    floor.transform = translation(0, -1, 0)
    floor.material.reflective = 0.5
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.objects.append(floor)

    ball = rt.Sphere()
    ball.material.color = rt.Color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = translation(0, -3.5, -0.5)
    w.objects.append(ball)

    xs = [rt.Intersection(floor, math.sqrt(2))]
    comps = prepare_computations(xs[0], r, xs)
    color = w.shade_hit(comps, 5)
    assert color == rt.Color(0.93391, 0.69643, 0.69243)


def rtunittest_testpattern1():
    # A pattern with an object transformation
    s = rt.Sphere()
    s.transform = scaling(2, 2, 2)
    s.material.pattern = rt.TestPattern()
    # this logic is in lighting().  Book assumed it would be in the Pattern object.
    object_point = rt.matmul4xTuple(s.inversetransform, rt.Point(2, 3, 4))
    pattern_point = rt.matmul4xTuple(s.material.pattern.inversetransform, object_point)
    c = s.material.pattern.color_at(pattern_point)
    assert c == rt.Color(1, 1.5, 2)


def rtunittest_testpattern2():
    # A pattern with a pattern transformation
    s = rt.Sphere()
    s.material.pattern = rt.TestPattern()
    s.material.pattern.transform = scaling(2, 2, 2)
    # this logic is in lighting().  Book assumed it would be in the Pattern object.
    object_point = rt.matmul4xTuple(s.inversetransform, rt.Point(2, 3, 4))
    pattern_point = rt.matmul4xTuple(s.material.pattern.inversetransform, object_point)
    c = s.material.pattern.color_at(pattern_point)
    assert c == rt.Color(1, 1.5, 2)


def rtunittest_testpattern3():
    # A pattern with both an object and a pattern transformation
    s = rt.Sphere()
    s.transform = scaling(2, 2, 2)
    s.material.pattern = rt.TestPattern()
    s.material.pattern.transform = translation(0.5, 1, 1.5)
    # this logic is in lighting().  Book assumed it would be in the Pattern object.
    object_point = rt.matmul4xTuple(s.inversetransform, rt.Point(2.5, 3, 3.5))
    pattern_point = rt.matmul4xTuple(s.material.pattern.inversetransform, object_point)
    c = s.material.pattern.color_at(pattern_point)
    assert c == rt.Color(0.75, 0.5, 0.25)


def run_unit_tests():
    count = 0

    # some tests take longer and we can skip unless we're explicitly testing a change to that feature.
    # tests_to_skip = ['test_canvas3', 'test_transformchain3', 'test_render1']
    tests_to_skip = []
    
    timestart = time.time()

    for f in globals().values():
        if type(f) == type(lambda *args: None):  # if f is a function
            n = f.__name__
            if n[:11] == 'rtunittest_':
                if n not in tests_to_skip:
                    eval(n + '()')
                    print('{} complete'.format(n))
                    count += 1
                else:
                    print('{} skipped'.format(n))

    print('{} tests completed.'.format(count))
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))
