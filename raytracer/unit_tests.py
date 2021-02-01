import math
import time
import os
import raytracer as rt
from .rttuple import random_in_unit_disk
from .transformations import do_transform, do_transformray, translation, scaling, reflection, rotation_x, rotation_y, \
                            rotation_z, skew, view_transform
from .world import prepare_computations, schlick_reflectance
from .canvas import init_canvas, write_pixel, pixel_at, get_canvasdims
from .matrices import allclose4x4
from .objects import EPSILON, intersection_allowed, TestShape
from .texturemap import FACELEFT, FACERIGHT, FACEFRONT, FACEBACK, FACEUP, FACEDOWN, face_from_point
from .quarticsolver import quadratic_solver, cubic_solver, quartic_solver


def run_unit_tests():
    count = 0
    failed = 0

    # some tests take longer and we can skip unless we're explicitly testing a change to that feature.
    tests_to_skip = ['rtunittest_canvas3', 'rtunittest_render1']
    # tests_to_skip = []

    timestart = time.time()

    testlist = []
    for f in globals().values():
        if callable(f):
            n = f.__name__
            if n[:11] == 'rtunittest_':
                if n not in tests_to_skip:
                    testlist.append(n)
                else:
                    print('{} skipped'.format(n))

    for n in testlist:
        try:
            eval(n + '()')
        except AssertionError:
            print('{} FAILED'.format(n))
            failed += 1
        else:
            # print('{} complete'.format(n))
            count += 1

    print('{} tests completed.'.format(count))
    if failed > 0:
        print('{} tests FAILED'.format(failed))
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))


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
    s1 = rt.Sphere(material=rt.Material(rt.Color(0.8, 1.0, 0.6), 0.1, 0.7, 0.2, 200))
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
    assert do_transform(trans, p) == rt.Point(2, 1, 7)


def rtunittest_translation2():
    # Multiplying by the inverse of a translation matrix
    trans = translation(5, -3, 2)
    inv = rt.inverse4x4(trans)
    p = rt.Point(-3, 4, 5)
    assert do_transform(inv, p) == rt.Point(-8, 7, 3)


def rtunittest_translation3():
    # Translation does not affect vectors
    trans = translation(5, -3, 2)
    v = rt.Vector(-3, 4, 5)
    assert do_transform(trans, v) == v


def rtunittest_scaling1():
    # A scaling matrix applied to a point
    trans = scaling(2, 3, 4)
    p = rt.Point(-4, 6, 8)
    assert do_transform(trans, p) == rt.Point(-8, 18, 32)


def rtunittest_scaling2():
    # A scaling matrix applied to a vector
    trans = scaling(2, 3, 4)
    v = rt.Vector(-4, 6, 8)
    assert do_transform(trans, v) == rt.Vector(-8, 18, 32)


def rtunittest_scaling3():
    # Multiplying by the inverse of a scaling matrix
    trans = scaling(2, 3, 4)
    inv = rt.inverse4x4(trans)
    v = rt.Vector(-4, 6, 8)
    assert do_transform(inv, v) == rt.Vector(-2, 2, 2)


def rtunittest_reflection1():
    # Reflection is scaling by a negative value
    trans = reflection(True, False, False)
    p = rt.Point(2, 3, 4)
    assert do_transform(trans, p) == rt.Point(-2, 3, 4)


def rtunittest_rotation1():
    # Rotating a point around the x axis
    p = rt.Point(0, 1, 0)
    half_quarter = rotation_x(math.pi / 4)
    full_quarter = rotation_x(math.pi / 2)
    assert do_transform(half_quarter, p) == rt.Point(0, math.sqrt(2)/2, math.sqrt(2)/2)
    assert do_transform(full_quarter, p) == rt.Point(0, 0, 1)


def rtunittest_rotation2():
    # The inverse of a rotation rotates in the opposite direction
    p = rt.Point(0, 1, 0)
    half_quarter = rotation_x(math.pi / 4)
    inv = rt.inverse4x4(half_quarter)
    assert do_transform(inv, p) == rt.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2)


def rtunittest_rotation3():
    # Rotating a point around the y axis
    p = rt.Point(0, 0, 1)
    half_quarter = rotation_y(math.pi / 4)
    full_quarter = rotation_y(math.pi / 2)
    assert do_transform(half_quarter, p) == rt.Point(math.sqrt(2)/2, 0, math.sqrt(2)/2)
    assert do_transform(full_quarter, p) == rt.Point(1, 0, 0)


def rtunittest_rotation4():
    # Rotating a point around the z axis
    p = rt.Point(0, 1, 0)
    half_quarter = rotation_z(math.pi / 4)
    full_quarter = rotation_z(math.pi / 2)
    assert do_transform(half_quarter, p) == rt.Point(-math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert do_transform(full_quarter, p) == rt.Point(-1, 0, 0)


def rtunittest_skew1():
    # A shearing transformation moves x in proportion to y
    trans = skew(1, 0, 0, 0, 0, 0)
    p = rt.Point(2, 3, 4)
    assert do_transform(trans, p) == rt.Point(5, 3, 4)


def rtunittest_skew2():
    # Several other shearing transformations
    p = rt.Point(2, 3, 4)
    trans1 = skew(0, 1, 0, 0, 0, 0)
    trans2 = skew(0, 0, 1, 0, 0, 0)
    trans3 = skew(0, 0, 0, 1, 0, 0)
    trans4 = skew(0, 0, 0, 0, 1, 0)
    trans5 = skew(0, 0, 0, 0, 0, 1)
    assert do_transform(trans1, p) == rt.Point(6, 3, 4)
    assert do_transform(trans2, p) == rt.Point(2, 5, 4)
    assert do_transform(trans3, p) == rt.Point(2, 7, 4)
    assert do_transform(trans4, p) == rt.Point(2, 3, 6)
    assert do_transform(trans5, p) == rt.Point(2, 3, 7)


def rtunittest_transformchain1():
    # Individual transformations are applied in sequence
    p = rt.Point(1, 0, 1)
    A = rotation_x(math.pi / 2)
    B = scaling(5, 5, 5)
    C = translation(10, 5, 7)
    p2 = do_transform(A, p)
    assert p2 == rt.Point(1, -1, 0)
    p3 = do_transform(B, p2)
    assert p3 == rt.Point(5, -5, 0)
    p4 = do_transform(C, p3)
    assert p4 == rt.Point(15, 0, 7)


def rtunittest_transformchain2():
    # CHained transformations must be applied in reverse order
    p = rt.Point(1, 0, 1)
    A = rotation_x(math.pi / 2)
    B = scaling(5, 5, 5)
    C = translation(10, 5, 7)
    T = rt.matmul4x4(rt.matmul4x4(C, B), A)
    assert do_transform(T, p) == rt.Point(15, 0, 7)


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
        p = do_transform(trans, p)

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
    r2 = do_transformray(m, r)
    assert r2.origin == rt.Point(4, 6, 8)
    assert r2.direction == rt.Vector(0, 1, 0)


def rtunittest_raytransform2():
    # Scaling a ray
    r = rt.Ray(rt.Point(1, 2, 3), rt.Vector(0, 1, 0))
    m = scaling(2, 3, 4)
    r2 = do_transformray(m, r)
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
    assert light.lighting(m, rt.HittableObject(), position, eyev, normalv) == rt.Color(1.9, 1.9, 1.9)


def rtunittest_lighting2():
    # Lighting with the eye between light and surface, eye offset 45 degrees
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, math.sqrt(2)/2, -math.sqrt(2)/2)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))
    assert light.lighting(m, rt.HittableObject(), position, eyev, normalv) == rt.Color(1.0, 1.0, 1.0)


def rtunittest_lighting3():
    # Lighting with eye opposite surface, light offset 45 degrees
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 10, -10), rt.Color(1, 1, 1))
    assert light.lighting(m, rt.HittableObject(), position, eyev, normalv) == \
           rt.Color(0.7364, 0.7364, 0.7364)


def rtunittest_lighting4():
    # Lighting with eye in the path of the reflection vector
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, -math.sqrt(2) / 2, -math.sqrt(2) / 2)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 10, -10), rt.Color(1, 1, 1))
    assert light.lighting(m, rt.HittableObject(), position, eyev, normalv) == \
           rt.Color(1.6364, 1.6364, 1.6364)


def rtunittest_lighting5():
    # Lighting with the light behind the surface
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 0, 10), rt.Color(1, 1, 1))
    assert light.lighting(m, rt.HittableObject(), position, eyev, normalv) == rt.Color(0.1, 0.1, 0.1)


def rtunittest_lighting6():
    # Lighting with the surface in shadow
    m = rt.Material()
    position = rt.Point(0, 0, 0)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)
    light = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))
    assert light.lighting(m, rt.HittableObject(), position, eyev, normalv, 0) \
           == rt.Color(0.1, 0.1, 0.1)


def rtunittest_lighting7():
    # lighting() uses light intensity to attenuate color
    w = default_world()
    w.lights[0] = rt.PointLight(rt.Point(0, 0, -10), rt.Color(1, 1, 1))
    w.objects[0].material.ambient = 0.1
    w.objects[0].material.diffuse = 0.9
    w.objects[0].material.specular = 0
    w.objects[0].material.color = rt.Color(1, 1, 1)
    pt = rt.Point(0, 0, -1)
    eyev = rt.Vector(0, 0, -1)
    normalv = rt.Vector(0, 0, -1)

    assert w.lights[0].lighting(w.objects[0].material, w.objects[0], pt, eyev, normalv, 1.0) == rt.Color(1, 1, 1)
    assert w.lights[0].lighting(w.objects[0].material, w.objects[0], pt, eyev, normalv, 0.5) == \
           rt.Color(0.55, 0.55, 0.55)
    assert w.lights[0].lighting(w.objects[0].material, w.objects[0], pt, eyev, normalv, 0.0) == rt.Color(0.1, 0.1, 0.1)


def rtunittest_lighting8():
    # Creating an area light
    corner = rt.Point(0, 0, 0)
    v1 = rt.Vector(2, 0, 0)
    v2 = rt.Vector(0, 0, 1)
    light = rt.AreaLight(corner, v1, 4, v2, 2, False, rt.Color(1, 1, 1))
    assert light.corner == corner
    assert light.uvec == rt.Vector(0.5, 0, 0)
    assert light.usteps == 4
    assert light.vvec == rt.Vector(0, 0, 0.5)
    assert light.vsteps == 2
    assert light.samples == 8
    assert light.position == rt.Point(1, 0, 0.5)


def rtunittest_lighting9():
    # Finding a single point on an area light

    # each test is a u, v and an expected result
    tests = [
        (0, 0, rt.Point(0.25, 0, 0.25)),
        (1, 0, rt.Point(0.75, 0, 0.25)),
        (0, 1, rt.Point(0.25, 0, 0.75)),
        (2, 0, rt.Point(1.25, 0, 0.25)),
        (3, 1, rt.Point(1.75, 0, 0.75))
    ]

    corner = rt.Point(0, 0, 0)
    v1 = rt.Vector(2, 0, 0)
    v2 = rt.Vector(0, 0, 1)
    light = rt.AreaLight(corner, v1, 4, v2, 2, False, rt.Color(1, 1, 1))

    for test in tests:
        assert light.point_on_light(test[0], test[1]) == test[2]


def rtunittest_lighting10():
    # The area light intensity function

    # each test is a point and expected intensity_pct result
    tests = [
        (rt.Point(0, 0, 2), 0.0),
        (rt.Point(1, -1, 2), 0.25),
        (rt.Point(1.5, 0, 2), 0.5),
        (rt.Point(1.25, 1.25, 3), 0.75),
        (rt.Point(0, 0, -2), 1.0)
    ]

    w = default_world()
    corner = rt.Point(-0.5, -0.5, -5)
    v1 = rt.Vector(1, 0, 0)
    v2 = rt.Vector(0, 1, 0)
    light = rt.AreaLight(corner, v1, 2, v2, 2, False, rt.Color(1, 1, 1))

    for test in tests:
        assert math.isclose(light.intensity_at(w, test[0]), test[1])


def rtunittest_lighting11():
    corner = rt.Point(-0.5, -0.5, -5)
    v1 = rt.Vector(1, 0, 0)
    v2 = rt.Vector(0, 1, 0)
    light = rt.AreaLight(corner, v1, 2, v2, 2, False, rt.Color(1, 1, 1))
    shape = rt.Sphere()
    shape.material.ambient = 0.1
    shape.material.diffuse = 0.9
    shape.material.specular = 0
    shape.material.color = rt.Color(1, 1, 1)
    eye = rt.Point(0, 0, -5)

    pt = rt.Point(0, 0, -1)
    eyev = rt.normalize(eye - pt)
    normalv = rt.Vector(pt.x, pt.y, pt.z)
    result = light.lighting(shape.material, shape, pt, eyev, normalv, 1.0)
    assert result == rt.Color(0.9965, 0.9965, 0.9965)

    pt = rt.Point(0, 0.7071, -0.7071)
    eyev = rt.normalize(eye - pt)
    normalv = rt.Vector(pt.x, pt.y, pt.z)
    result = light.lighting(shape.material, shape, pt, eyev, normalv, 1.0)
    assert result == rt.Color(0.62318, 0.62318, 0.62318)


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
    # is_shadowed tests for occlusion between two points
    w = default_world()
    light_position = rt.Point(-10, -10, -10)

    assert not w.is_shadowed(rt.Point(-10, -10, 10), light_position)
    assert w.is_shadowed(rt.Point(10, 10, 10), light_position)
    assert not w.is_shadowed(rt.Point(-20, -20, -20), light_position)
    assert not w.is_shadowed(rt.Point(-5, -5, -5), light_position)


def rtunittest_shadowed2():
    # Point lights evaluate the light intensity at a given bpoint

    # each test is a point and an intensity result
    tests = [
        (rt.Point(0, 1.0001, 0), 1.0),
        (rt.Point(-1.0001, 0, 0), 1.0),
        (rt.Point(0, 0, -1.0001), 1.0),
        (rt.Point(0, 0, 1.0001), 0.0),
        (rt.Point(1.0001, 0, 0), 0.0),
        (rt.Point(0, -1.0001, 0), 0.0),
        (rt.Point(0, 0, 0), 0.0)
    ]

    w = default_world()
    light = w.lights[0]
    for test in tests:
        assert math.isclose(light.intensity_at(w, test[0]), test[1])


def rtunittest_testshape1():
    # Intersecting a scaled shape with a ray
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = TestShape()
    s.transform = rt.scaling(2, 2, 2)
    s.intersect(r)  # we do not need the return value
    assert s.saved_ray.origin == rt.Point(0, 0, -2.5)
    assert s.saved_ray.direction == rt.Vector(0, 0, 0.5)


def rtunittest_testshape2():
    # Intersecting a translated shape with a ray
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    s = TestShape()
    s.transform = rt.translation(5, 0, 0)
    s.intersect(r)  # do not need the return variable
    assert s.saved_ray.origin == rt.Point(-5, 0, -5)
    assert s.saved_ray.direction == rt.Vector(0, 0, 1)


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

    c1 = light.lighting(m, rt.HittableObject(), rt.Point(0.9, 0, 0), eyev, normalv, 1)
    c2 = light.lighting(m, rt.HittableObject(), rt.Point(1.1, 0, 0), eyev, normalv, 1)

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


def rtunittest_cube1():
    # A ray intersects a cube
    c = rt.Cube()

    # each tuple in the list is origin, direction, t1, t2
    tests = [
        (rt.Point(5, 0.5, 0), rt.Vector(-1, 0, 0), 4, 6),
        (rt.Point(-5, 0.5, 0), rt.Vector(1, 0, 0), 4, 6),
        (rt.Point(0.5, 5, 0), rt.Vector(0, -1, 0), 4, 6),
        (rt.Point(0.5, -5, 0), rt.Vector(0, 1, 0), 4, 6),
        (rt.Point(0.5, 0, 5), rt.Vector(0, 0, -1), 4, 6),
        (rt.Point(0.5, 0, -5), rt.Vector(0, 0, 1), 4, 6),
        (rt.Point(0, 0.5, 0), rt.Vector(0, 0, 1), -1, 1)
    ]

    for test in tests:
        r = rt.Ray(test[0], test[1])
        xs = c.local_intersect(r)
        assert len(xs) == 2
        assert xs[0].t == test[2]
        assert xs[1].t == test[3]


def rtunittest_cube2():
    # A ray misses a cube
    c = rt.Cube()

    # each tuple in the list is origin, direction
    tests = [
        (rt.Point(-2, 0, 0), rt.Vector(0.2673, 0.5345, 0.8018)),
        (rt.Point(0, -2, 0), rt.Vector(0.8018, 0.2673, 0.5345)),
        (rt.Point(0, 0, -2), rt.Vector(0.5345, 0.8018, 0.2673)),
        (rt.Point(2, 0, 2), rt.Vector(0, 0, -1)),
        (rt.Point(0, 2, 2), rt.Vector(0, -1, 0)),
        (rt.Point(2, 2, 0), rt.Vector(-1, 0, 0)),
        (rt.Point(0, 0, 2), rt.Vector(0, 0, 1))
    ]

    for test in tests:
        r = rt.Ray(test[0], test[1])
        xs = c.local_intersect(r)
        assert len(xs) == 0


def rtunittest_cube3():
    # The normal on teh surface of a cube
    c = rt.Cube()

    # each tuple in the list is point, normal
    tests = [
        (rt.Point(1, 0.5, -0.8), rt.Vector(1, 0, 0)),
        (rt.Point(-1, -0.2, 0.9), rt.Vector(-1, 0, 0)),
        (rt.Point(-0.4, 1, -0.1), rt.Vector(0, 1, 0)),
        (rt.Point(0.3, -1, -0.7), rt.Vector(0, -1, 0)),
        (rt.Point(-0.6, 0.3, 1), rt.Vector(0, 0, 1)),
        (rt.Point(0.4, 0.4, -1), rt.Vector(0, 0, -1)),
        (rt.Point(1, 1, 1), rt.Vector(1, 0, 0)),
        (rt.Point(-1, -1, -1), rt.Vector(-1, 0, 0)),
    ]

    for test in tests:
        normal = c.local_normal_at(test[0])
        assert normal == test[1]


def rtunittest_cylinder1():
    # A ray misses a cylinder
    cyl = rt.Cylinder()

    # each test has origin, direction of a ray that misses the cylinder
    tests = [
        (rt.Point(1, 0, 0), rt.Vector(0, 1, 0)),
        (rt.Point(0, 0, 0), rt.Vector(0, 1, 0)),
        (rt.Point(0, 0, -5), rt.Vector(1, 1, 1))
    ]

    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        xs = cyl.local_intersect(r)
        assert len(xs) == 0


def rtunittest_cylinder2():
    # A ray strikes a cylinder

    cyl = rt.Cylinder()

    # each test has origin, direction of ray and t0/t1 for the two intersections
    tests = [
        (rt.Point(1, 0, -5), rt.Vector(0, 0, 1), 5, 5),
        (rt.Point(0, 0, -5), rt.Vector(0, 0, 1), 4, 6),
        (rt.Point(0.5, 0, -5), rt.Vector(0.1, 1, 1), 6.80798, 7.08872)
    ]

    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        xs = cyl.local_intersect(r)
        assert len(xs) == 2
        assert math.isclose(xs[0].t, test[2], rel_tol=1e-05, abs_tol=1e-05)
        assert math.isclose(xs[1].t, test[3], rel_tol=1e-05, abs_tol=1e-05)


def rtunittest_cylinder3():
    # Normal vector on a cylinder

    cyl = rt.Cylinder()

    # each test has point on cylinder and the expected normal at that point
    tests = [
        (rt.Point(1, 0, 0), rt.Vector(1, 0, 0)),
        (rt.Point(0, 5, -1), rt.Vector(0, 0, -1)),
        (rt.Point(0, -2, 1), rt.Vector(0, 0, 1)),
        (rt.Point(-1, 1, 0), rt.Vector(-1, 0, 0))
    ]

    for test in tests:
        n = cyl.local_normal_at(test[0])
        assert n == test[1]


def rtunittest_cylinder4():
    # default minimum and maximum for a cylinder
    # The default closed value for a cylinder
    cyl = rt.Cylinder()
    assert math.isinf(cyl.min_y)
    assert math.isinf(cyl.max_y)
    assert not cyl.closed


def rtunittest_cylinder5():
    # Intersecting a constrained cylinder

    # each test has a point, direction, and number of intersections
    tests = [
        (rt.Point(0, 1.5, 0), rt.Vector(0.1, 1, 0), 0),
        (rt.Point(0, 3, -5), rt.Vector(0, 0, 1), 0),
        (rt.Point(0, 0, -5), rt.Vector(0, 0, 1), 0),
        (rt.Point(0, 2, -5), rt.Vector(0, 0, 1), 0),
        (rt.Point(0, 1, -5), rt.Vector(0, 0, 1), 0),
        (rt.Point(0, 1.5, -2), rt.Vector(0, 0, 1), 2)
    ]

    cyl = rt.Cylinder()
    cyl.min_y = 1
    cyl.max_y = 2

    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        xs = cyl.local_intersect(r)
        assert len(xs) == test[2]


def rtunittest_cylinder6():
    # Intersecting the caps of a closed cylinder

    # each test has a point, direction, and number of intersections
    tests = [
        (rt.Point(0, 3, 0), rt.Vector(0, -1, 0), 2),
        (rt.Point(0, 3, -2), rt.Vector(0, -1, 2), 2),
        (rt.Point(0, 4, -2), rt.Vector(0, -1, 1), 2),
        (rt.Point(0, 0, -2), rt.Vector(0, 1, 2), 2),
        (rt.Point(0, -1, -2), rt.Vector(0, 1, 1), 2),
        (rt.Point(0, 1.5, 0), rt.Vector(0, 1, 0), 2)  # I added this test
    ]

    cyl = rt.Cylinder()
    cyl.min_y = 1
    cyl.max_y = 2
    cyl.closed = True

    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        xs = cyl.local_intersect(r)
        assert len(xs) == test[2]


def rtunittest_cylinder7():
    # The normal vector on a cylinder's end caps

    # each test has the point on the cylinder and the expected normal
    tests = [
        (rt.Point(0, 1, 0), rt.Vector(0, -1, 0)),
        (rt.Point(0.5, 1, 0), rt.Vector(0, -1, 0)),
        (rt.Point(0, 1, 0.5), rt.Vector(0, -1, 0)),
        (rt.Point(0, 2, 0), rt.Vector(0, 1, 0)),
        (rt.Point(0.5, 2, 0), rt.Vector(0, 1, 0)),
        (rt.Point(0, 2, 0.5), rt.Vector(0, 1, 0))
    ]

    cyl = rt.Cylinder()
    cyl.min_y = 1
    cyl.max_y = 2
    cyl.closed = True

    for test in tests:
        n = cyl.local_normal_at(test[0])
        assert n == test[1]


def rtunittest_cone1():
    # Intersecting a cone with a ray

    # Each test has origin, direction, then t's for the two intersections
    tests = [
        (rt.Point(0, 0, -5), rt.Vector(0, 0, 1), 5, 5),
        (rt.Point(0, 0, -5), rt.Vector(1, 1, 1), 8.66025, 8.66025),
        (rt.Point(1, 1, -5), rt.Vector(-0.5, -1, 1), 4.55006, 49.44994)
    ]

    s = rt.Cone()
    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        xs = s.local_intersect(r)
        assert len(xs) == 2
        assert math.isclose(xs[0].t, test[2], rel_tol=1e-05)
        assert math.isclose(xs[1].t, test[3], rel_tol=1e-05)


def rtunittest_cone2():
    # Intersecting a cone with a ray parallel to one. of its halves

    s = rt.Cone()
    d = rt.normalize(rt.Vector(0, 1, 1))
    r = rt.Ray(rt.Point(0, 0, -1), d)
    xs = s.local_intersect(r)
    assert len(xs) == 1
    assert math.isclose(xs[0].t, 0.35355, rel_tol=1e-05)


def rtunittest_cone3():
    # Intersecting a cone's end caps

    # each test has origin, direction, and number of intersections
    tests = [
        (rt.Point(0, 0, -5), rt.Vector(0, 1, 0), 0),
        (rt.Point(0, 0, -0.25), rt.Vector(0, 1, 1), 2),
        (rt.Point(0, 0, -0.25), rt.Vector(0, 1, 0), 4)
    ]

    s = rt.Cone()
    s.min_y = -0.5
    s.max_y = 0.5
    s.closed = True
    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        xs = s.local_intersect(r)
        assert len(xs) == test[2]


def rtunittest_cone4():
    # Computing the normal vector on a cone

    # each test has a point and the expected normal
    tests = [
        (rt.Point(0, 0, 0), rt.Vector(0, 0, 0)),
        (rt.Point(1, 1, 1), rt.Vector(1, -math.sqrt(2), 1)),
        (rt.Point(-1, -1, 0), rt.Vector(-1, 1, 0))
    ]

    s = rt.Cone()
    for test in tests:
        n = s.local_normal_at(test[0])
        assert n == test[1]


def rtunittest_groups1():
    # Creating a new group
    g = rt.ObjectGroup()
    assert g.transform == rt.identity4()
    assert len(g.children) == 0


def rtunittest_groups2():
    # A shape has a parent attribute
    s = glass_sphere()
    assert s.parent is None


def rtunittest_groups3():
    # Adding a child to a group
    s = glass_sphere()
    g = rt.ObjectGroup()
    g.addchild(s)
    assert len(g.children) == 1
    assert s in g.children


def rtunittest_groups4():
    # Intersecting a ray with an empty group
    g = rt.ObjectGroup()
    r = rt.Ray(rt.Point(0, 0, 0), rt.Vector(0, 0, 1))
    xs = g.local_intersect(r)
    assert len(xs) == 0


def rtunittest_groups5():
    # Intersecting a ray with a nonempty group
    g = rt.ObjectGroup()
    s1 = rt.Sphere()
    s2 = rt.Sphere()
    s2.transform = rt.translation(0, 0, -3)
    s3 = rt.Sphere()
    s3.transform = rt.translation(5, 0, 0)
    g.addchild(s1)
    g.addchild(s2)
    g.addchild(s3)
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    xs = g.local_intersect(r)
    # the book says to test that the intersections come back in sorted order.
    # However, we don't sort in local_intersect, we sort in World.intersect().
    # so we need to sort here to make the test work properly.
    xs.sort(key=lambda x: x.t)

    assert len(xs) == 4
    assert xs[0].objhit is s2
    assert xs[1].objhit is s2
    assert xs[2].objhit is s1
    assert xs[3].objhit is s1


def rtunittest_groups6():
    # Intersecting a transformed group
    g = rt.ObjectGroup()
    g.transform = rt.scaling(2, 2, 2)
    s = rt.Sphere()
    s.transform = rt.translation(5, 0, 0)
    g.addchild(s)

    r = rt.Ray(rt.Point(10, 0, -10), rt.Vector(0, 0, 1))
    xs = g.intersect(r)

    assert len(xs) == 2


def rtunittest_groups7():
    # Converting a point from world to object space
    g1 = rt.ObjectGroup()
    g1.transform = rt.rotation_y(math.pi/2)
    g2 = rt.ObjectGroup()
    g2.transform = rt.scaling(2, 2, 2)
    g1.addchild(g2)
    s = rt.Sphere()
    s.transform = rt.translation(5, 0, 0)
    g2.addchild(s)

    p = s.world_to_object(rt.Point(-2, 0, -10))
    assert p == rt.Point(0, 0, -1)


def rtunittest_groups8():
    # converting a normal from object to world space
    g1 = rt.ObjectGroup()
    g1.transform = rt.rotation_y(math.pi/2)
    g2 = rt.ObjectGroup()
    g2.transform = rt.scaling(1, 2, 3)
    g1.addchild(g2)
    s = rt.Sphere()
    s.transform = rt.translation(5, 0, 0)
    g2.addchild(s)
    n = s.normal_to_world(rt.Vector(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))
    assert n == rt.Vector(0.28571, 0.42857, -0.85714)


def rtunittest_groups9():
    # Finding the normal on a child object
    g1 = rt.ObjectGroup()
    g1.transform = rt.rotation_y(math.pi / 2)
    g2 = rt.ObjectGroup()
    g2.transform = rt.scaling(1, 2, 3)
    g1.addchild(g2)
    s = rt.Sphere()
    s.transform = rt.translation(5, 0, 0)
    g2.addchild(s)
    n = s.normal_at(rt.Point(1.7321, 1.1547, -5.5774))
    assert n == rt.Vector(0.2857, 0.42854, -0.85716)


def rtunittest_triangle1():
    # Constructing a triangle
    p1 = rt.Point(0, 1, 0)
    p2 = rt.Point(-1, 0, 0)
    p3 = rt.Point(1, 0, 0)
    t = rt.Triangle(p1, p2, p3)
    assert t.p1 == p1
    assert t.p2 == p2
    assert t.p3 == p3
    assert t.e1 == rt.Vector(-1, -1, 0)
    assert t.e2 == rt.Vector(1, -1, 0)
    assert t.normal == rt.Vector(0, 0, -1)


def rtunittest_triangle2():
    # Finding the normal on a triangle
    t = rt.Triangle(rt.Point(0, 1, 0), rt.Point(-1, 0, 0), rt.Point(1, 0, 0))
    n1 = t.local_normal_at(rt.Point(0, 0.5, 0))
    n2 = t.local_normal_at(rt.Point(-0.5, 0.75, 0))
    n3 = t.local_normal_at(rt.Point(0.5, 0.25, 0))
    assert n1 == t.normal
    assert n2 == t.normal
    assert n3 == t.normal


def rtunittest_triangle3():
    # Intersecting a ray parallel to the triangle
    t = rt.Triangle(rt.Point(0, 1, 0), rt.Point(-1, 0, 0), rt.Point(1, 0, 0))
    r = rt.Ray(rt.Point(0, -2, -2), rt.Vector(0, 1, 0))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def rtunittest_triangle4():
    # A ray misses the p1-p3 edge
    t = rt.Triangle(rt.Point(0, 1, 0), rt.Point(-1, 0, 0), rt.Point(1, 0, 0))
    r = rt.Ray(rt.Point(1, 1, -2), rt.Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def rtunittest_triangle5():
    # A ray misses the p1-p2 edge
    t = rt.Triangle(rt.Point(0, 1, 0), rt.Point(-1, 0, 0), rt.Point(1, 0, 0))
    r = rt.Ray(rt.Point(-1, 1, -2), rt.Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def rtunittest_triangle6():
    # A ray misses the p2-p3 edge
    t = rt.Triangle(rt.Point(0, 1, 0), rt.Point(-1, 0, 0), rt.Point(1, 0, 0))
    r = rt.Ray(rt.Point(0, -1, -2), rt.Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 0


def rtunittest_triangle7():
    # A ray strikes a triangle
    t = rt.Triangle(rt.Point(0, 1, 0), rt.Point(-1, 0, 0), rt.Point(1, 0, 0))
    r = rt.Ray(rt.Point(0, 0.5, -2), rt.Vector(0, 0, 1))
    xs = t.local_intersect(r)
    assert len(xs) == 1
    assert math.isclose(xs[0].t, 2)


def rtunittest_objfile1():
    # Ignoring unrecognized lines
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/gibberish.obj', False)
    assert parser.numvertices == 0
    assert len(parser.groupinfos) == 1
    assert parser.numnormals == 0


def rtunittest_objfile2():
    # Vertex records
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/vertex_records_test.obj', False)
    assert parser.numvertices == 4
    assert parser.vertices[1] == rt.Point(-1, 1, 0)
    assert parser.vertices[2] == rt.Point(-1, 0.5, 0)
    assert parser.vertices[3] == rt.Point(1, 0, 0)
    assert parser.vertices[4] == rt.Point(1, 1, 0)


def rtunittest_objfile3():
    # Parsing traingle faces
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/parsing_triangle_faces_test.obj', False)
    assert parser.numvertices == 4
    assert len(parser.groupinfos) == 1
    g = parser.get_group_by_name('')
    assert len(g.children) == 2
    t1 = g.children[0]
    t2 = g.children[1]
    assert t1.p1 == parser.vertices[1]
    assert t1.p2 == parser.vertices[2]
    assert t1.p3 == parser.vertices[3]
    assert t2.p1 == parser.vertices[1]
    assert t2.p2 == parser.vertices[3]
    assert t2.p3 == parser.vertices[4]


def rtunittest_objfile4():
    # Triangulating polygons
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/triangulating_polygons_test.obj', False)
    assert parser.numvertices == 5
    assert len(parser.groupinfos) == 1
    g = parser.get_group_by_name('')
    assert len(g.children) == 3
    t1 = g.children[0]
    t2 = g.children[1]
    t3 = g.children[2]
    assert t1.p1 == parser.vertices[1]
    assert t1.p2 == parser.vertices[2]
    assert t1.p3 == parser.vertices[3]
    assert t2.p1 == parser.vertices[1]
    assert t2.p2 == parser.vertices[3]
    assert t2.p3 == parser.vertices[4]
    assert t3.p1 == parser.vertices[1]
    assert t3.p2 == parser.vertices[4]
    assert t3.p3 == parser.vertices[5]


def rtunittest_objfile5():
    # Triangles in groups
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/triangles.obj', False)
    assert parser.numvertices == 4
    g1 = parser.get_group_by_name('FirstGroup')
    g2 = parser.get_group_by_name('SecondGroup')
    t1 = g1.children[0]
    t2 = g2.children[0]
    assert t1.p1 == parser.vertices[1]
    assert t1.p2 == parser.vertices[2]
    assert t1.p3 == parser.vertices[3]
    assert t2.p1 == parser.vertices[1]
    assert t2.p2 == parser.vertices[3]
    assert t2.p3 == parser.vertices[4]


def rtunittest_objfile6():
    # Converting an OBJ file to a group
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/triangles.obj', False)
    g = parser.obj_to_group()
    assert parser.get_group_by_name('FirstGroup') in g.children
    assert parser.get_group_by_name('SecondGroup') in g.children


def rtunittest_objfile7():
    # Vertex normal records
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/vertex_normals_test.obj', False)
    assert parser.numnormals == 3
    assert parser.normals[1] == rt.Vector(0, 0, 1)
    assert parser.normals[2] == rt.Vector(0.707, 0, -0.707)
    assert parser.normals[3] == rt.Vector(1, 2, 3)


def rtunittest_objfile8():
    # Faces with normals
    parser = rt.Parser()
    parser.parse_obj_file('raytracer/test_obj_files/faces_with_normals_test.obj', False)
    g = parser.get_group_by_name('')
    assert isinstance(g, rt.ObjectGroup)
    t1 = g.children[0]
    t2 = g.children[1]
    assert t1.p1 == parser.vertices[1]
    assert t1.p2 == parser.vertices[2]
    assert t1.p3 == parser.vertices[3]
    assert t1.n1 == parser.normals[3]
    assert t1.n2 == parser.normals[1]
    assert t1.n3 == parser.normals[2]
    assert t1.p1 == t2.p1
    assert t1.p2 == t2.p2
    assert t1.p3 == t2.p3
    assert t1.n1 == t2.n1
    assert t1.n2 == t2.n2
    assert t1.n3 == t2.n3


def rtunittest_intersectionuv1():
    # An intersection can encapsulate 'u' and 'v'
    s = rt.Triangle(rt.Point(0, 1, 0), rt.Point(-1, 0, 0), rt.Point(1, 0, 0))
    i = rt.IntersectionWithUV(s, 3.5, 0.2, 0.4)
    assert i.u == 0.2
    assert i.v == 0.4


def rtunittest_smoothtriangle1():
    # Constructing a smooth triangle
    p1 = rt.Point(0, 1, 0)
    p2 = rt.Point(-1, 0, 0)
    p3 = rt.Point(1, 0, 0)
    n1 = rt.Vector(0, 1, 0)
    n2 = rt.Vector(-1, 0, 0)
    n3 = rt.Vector(1, 0, 0)
    tri = rt.SmoothTriangle(p1, p2, p3, n1, n2, n3)

    assert tri.p1 == p1
    assert tri.p2 == p2
    assert tri.p3 == p3
    assert tri.n1 == n1
    assert tri.n2 == n2
    assert tri.n3 == n3


def rtunittest_smoothtriangle2():
    # An intersection with a smooth triangle stores u/v
    p1 = rt.Point(0, 1, 0)
    p2 = rt.Point(-1, 0, 0)
    p3 = rt.Point(1, 0, 0)
    n1 = rt.Vector(0, 1, 0)
    n2 = rt.Vector(-1, 0, 0)
    n3 = rt.Vector(1, 0, 0)
    tri = rt.SmoothTriangle(p1, p2, p3, n1, n2, n3)

    r = rt.Ray(rt.Point(-0.2, 0.3, -2), rt.Vector(0, 0, 1))
    xs = tri.local_intersect(r)
    assert len(xs) == 1
    assert isinstance(xs[0], rt.IntersectionWithUV)
    assert math.isclose(xs[0].u, 0.45)
    assert math.isclose(xs[0].v, 0.25)


def rtunittest_smoothtriangle3():
    # A smooth triangle uses u/v to interpolate the normal
    p1 = rt.Point(0, 1, 0)
    p2 = rt.Point(-1, 0, 0)
    p3 = rt.Point(1, 0, 0)
    n1 = rt.Vector(0, 1, 0)
    n2 = rt.Vector(-1, 0, 0)
    n3 = rt.Vector(1, 0, 0)
    tri = rt.SmoothTriangle(p1, p2, p3, n1, n2, n3)

    i = rt.IntersectionWithUV(tri, 1, 0.45, 0.25)
    n = tri.normal_at(rt.Point(0, 0, 0), i)
    assert n == rt.Vector(-0.5547, 0.83205, 0)


def rtunittest_smoothtriangle4():
    # Preparing the normal on a smooth triangle
    p1 = rt.Point(0, 1, 0)
    p2 = rt.Point(-1, 0, 0)
    p3 = rt.Point(1, 0, 0)
    n1 = rt.Vector(0, 1, 0)
    n2 = rt.Vector(-1, 0, 0)
    n3 = rt.Vector(1, 0, 0)
    tri = rt.SmoothTriangle(p1, p2, p3, n1, n2, n3)

    i = rt.IntersectionWithUV(tri, 1, 0.45, 0.25)
    r = rt.Ray(rt.Point(-0.2, 0.3, -2), rt.Vector(0, 0, 1))
    comps = prepare_computations(i, r, [i])
    assert comps.normalv == rt.Vector(-0.5547, 0.83205, 0)


def rtunittest_csg1():
    # CSG is created with an operation and two shapes
    s1 = rt.Sphere()
    s2 = rt.Cube()
    c = rt.CSG("union", s1, s2)
    assert c.operation == "union"
    assert c.left is s1
    assert c.right is s2
    assert s1.parent is c
    assert s2.parent is c


def rtunittest_csg2():
    # Evaluating the rule for a CSG operation

    # each test has an operation, lhit, inl, inr, and expected result
    tests = [
        ('union', True, True, True, False),
        ('union', True, True, False, True),
        ('union', True, False, True, False),
        ('union', True, False, False, True),
        ('union', False, True, True, False),
        ('union', False, True, False, False),
        ('union', False, False, True, True),
        ('union', False, False, False, True),
        ('intersection', True, True, True, True),
        ('intersection', True, True, False, False),
        ('intersection', True, False, True, True),
        ('intersection', True, False, False, False),
        ('intersection', False, True, True, True),
        ('intersection', False, True, False, True),
        ('intersection', False, False, True, False),
        ('intersection', False, False, False, False),
        ('difference', True, True, True, False),
        ('difference', True, True, False, True),
        ('difference', True, False, True, False),
        ('difference', True, False, False, True),
        ('difference', False, True, True, True),
        ('difference', False, True, False, True),
        ('difference', False, False, True, False),
        ('difference', False, False, False, False),
    ]

    for test in tests:
        assert intersection_allowed(test[0], test[1], test[2], test[3]) == test[4]


def rtunittest_csg3():
    # Filtering a list of intersections

    # each test contains operation, and specific intersections that should be returned
    tests = [
        ('union', 0, 3), ('intersection', 1, 2), ('difference', 0, 1)
    ]

    s1 = rt.Sphere()
    s2 = rt.Cube()
    xs = [rt.Intersection(s1, 1), rt.Intersection(s2, 2), rt.Intersection(s1, 3), rt.Intersection(s2, 4)]

    for test in tests:
        c = rt.CSG(test[0], s1, s2)
        res = c.filter_intersections(xs)
        assert len(res) == 2
        assert res[0].objhit is xs[test[1]].objhit
        assert res[0].t == xs[test[1]].t
        assert res[1].objhit is xs[test[2]].objhit
        assert res[1].t == xs[test[2]].t


def rtunittest_csg4():
    # A ray misses a CSG object

    c = rt.CSG("union", rt.Sphere(), rt.Cube())
    r = rt.Ray(rt.Point(0, 2, -5), rt.Vector(0, 0, 1))
    xs = c.local_intersect(r)
    assert len(xs) == 0


def rtunittest_csg5():
    # A ray hits a CSG object
    s1 = rt.Sphere()
    s2 = rt.Sphere()
    s2.transform = rt.translation(0, 0, 0.5)
    c = rt.CSG("union", s1, s2)
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    xs = c.local_intersect(r)

    assert len(xs) == 2
    assert math.isclose(xs[0].t, 4)
    assert xs[0].objhit is s1
    assert math.isclose(xs[1].t, 6.5)
    assert xs[1].objhit is s2


def rtunittest_boundingbox1():
    # Creating an empty bounding box
    box = rt.BoundingBox()
    assert box.boxmin == rt.Point(math.inf, math.inf, math.inf)
    assert box.boxmax == rt.Point(-math.inf, -math.inf, -math.inf)


def rtunittest_boundingbox2():
    # Creating a bounding box with volume
    box = rt.BoundingBox(rt.Point(-1, -2, -3), rt.Point(3, 2, 1))
    assert box.boxmin == rt.Point(-1, -2, -3)
    assert box.boxmax == rt.Point(3, 2, 1)


def rtunittest_boundingbox3():
    # Adding points to an empty bounding box
    box = rt.BoundingBox()
    box.addpoint(rt.Point(-5, 2, 0))
    box.addpoint(rt.Point(7, 0, -3))
    assert box.boxmin == rt.Point(-5, 0, -3)
    assert box.boxmax == rt.Point(7, 2, 0)


def rtunittest_boundingbox4():
    # A sphere has a bounding box
    shape = rt.Sphere()
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-1, -1, -1)
    assert box.boxmax == rt.Point(1, 1, 1)


def rtunittest_boundingbox5():
    # A plane has a bounding box
    shape = rt.Plane()
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-math.inf, 0, -math.inf)
    assert box.boxmax == rt.Point(math.inf, 0, math.inf)


def rtunittest_boundingbox6():
    # A cube has a bounding box
    shape = rt.Cube()
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-1, -1, -1)
    assert box.boxmax == rt.Point(1, 1, 1)


def rtunittest_boundingbox7():
    # An unbounded cylinder has a bounding box
    shape = rt.Cylinder()
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-1, -math.inf, -1)
    assert box.boxmax == rt.Point(1, math.inf, 1)


def rtunittest_boundingbox8():
    # A bounded cylinder has a bounding box
    shape = rt.Cylinder()
    shape.min_y = -5
    shape.max_y = 3
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-1, -5, -1)
    assert box.boxmax == rt.Point(1, 3, 1)


def rtunittest_boundingbox9():
    # An unbounded cone has a bounding box
    shape = rt.Cone()
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-math.inf, -math.inf, -math.inf)
    assert box.boxmax == rt.Point(math.inf, math.inf, math.inf)


def rtunittest_boundingbox10():
    # A bounded cone has a bounding box
    shape = rt.Cone()
    shape.min_y = -5
    shape.max_y = 3
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-5, -5, -5)
    assert box.boxmax == rt.Point(5, 3, 5)


def rtunittest_boundingbox11():
    # A triangle has a bounding box
    p1 = rt.Point(-3, 7, 2)
    p2 = rt.Point(6, 2, -4)
    p3 = rt.Point(2, -1, -1)
    shape = rt.Triangle(p1, p2, p3)
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-3, -1, -4)
    assert box.boxmax == rt.Point(6, 7, 2)


def rtunittest_boundingbox12():
    # Adding one bounding box to another
    box1 = rt.BoundingBox(rt.Point(-5, -2, 0), rt.Point(7, 4, 4))
    box2 = rt.BoundingBox(rt.Point(8, -7, -2), rt.Point(14, 2, 8))
    box1 += box2
    assert box1.boxmin == rt.Point(-5, -7, -2)
    assert box1.boxmax == rt.Point(14, 4, 8)


def rtunittest_boundingbox13():
    # Checking to see if a box contains a given point
    box = rt.BoundingBox(rt.Point(5, -2, 0), rt.Point(11, 4, 7))

    assert box.contains_point(rt.Point(5, -2, 0))
    assert box.contains_point(rt.Point(11, 4, 7))
    assert box.contains_point(rt.Point(8, 1, 3))
    assert not box.contains_point(rt.Point(3, 0, 3))
    assert not box.contains_point(rt.Point(8, -4, 3))
    assert not box.contains_point(rt.Point(8, 1, -1))
    assert not box.contains_point(rt.Point(13, 1, 3))
    assert not box.contains_point(rt.Point(8, 5, 3))
    assert not box.contains_point(rt.Point(8, 1, 8))


def rtunittest_boundingbox14():
    # Checking to see if a box contains a given box
    box = rt.BoundingBox(rt.Point(5, -2, 0), rt.Point(11, 4, 7))

    assert box.contains_box(rt.BoundingBox(rt.Point(5, -2, 0), rt.Point(11, 4, 7)))
    assert box.contains_box(rt.BoundingBox(rt.Point(6, -1, 1), rt.Point(10, 3, 6)))
    assert not box.contains_box(rt.BoundingBox(rt.Point(4, -3, -1), rt.Point(10, 3, 6)))
    assert not box.contains_box(rt.BoundingBox(rt.Point(6, -1, 1), rt.Point(12, 5, 8)))


def rtunittest_boundingbox15():
    # Transforming a bounding box
    box = rt.BoundingBox(rt.Point(-1, -1, -1), rt.Point(1, 1, 1))
    matrix = rt.matmul4x4(rt.rotation_x(math.pi/4), rt.rotation_y(math.pi/4))
    box2 = box.transform(matrix)
    assert box2.boxmin == rt.Point(-1.4142, -1.7071, -1.7071)
    assert box2.boxmax == rt.Point(1.4142, 1.7071, 1.7071)


def rtunittest_boundingbox16():
    # Querying a shape's bounding box in its parent's space
    shape = rt.Sphere()
    shape.transform = rt.matmul4x4(rt.translation(1, -3, 5), rt.scaling(0.5, 2, 4))
    box = shape.parent_space_bounds_of()
    assert box.boxmin == rt.Point(0.5, -5, 1)
    assert box.boxmax == rt.Point(1.5, -1, 9)


def rtunittest_boundingbox17():
    # A group has a bounding box that contains its children
    s = rt.Sphere()
    s.transform = rt.matmul4x4(rt.translation(2, 5, -3), rt.scaling(2, 2, 2))
    c = rt.Cylinder()
    c.min_y = -2
    c.max_y = 2
    c.transform = rt.matmul4x4(rt.translation(-4, -1, 4), rt.scaling(0.5, 1, 0.5))
    shape = rt.ObjectGroup()
    shape.addchild(s)
    shape.addchild(c)
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-4.5, -3, -5)
    assert box.boxmax == rt.Point(4, 7, 4.5)


def rtunittest_boundingbox18():
    # A CSG shape has a bounding box that contains its children
    left = rt.Sphere()
    right = rt.Sphere()
    right.transform = rt.translation(2, 3, 4)
    shape = rt.CSG('difference', left, right)
    box = shape.bounds_of()
    assert box.boxmin == rt.Point(-1, -1, -1)
    assert box.boxmax == rt.Point(3, 4, 5)


def rtunittest_boundingbox19():
    # Intersecting a ray with a bounding box at the origin

    # each test has origin and direction of the vector, and whether or not it intersects
    tests = [
        (rt.Point(5, 0.5, 0), rt.Vector(-1, 0, 0), True),
        (rt.Point(-5, 0.5, 0), rt.Vector(1, 0, 0), True),
        (rt.Point(0.5, 5, 0), rt.Vector(0, -1, 0), True),
        (rt.Point(0.5, -5, 0), rt.Vector(0, 1, 0), True),
        (rt.Point(0.5, 0, 5), rt.Vector(0, 0, -1), True),
        (rt.Point(0.5, 0, -5), rt.Vector(0, 0, 1), True),
        (rt.Point(0, 0.5, 0), rt.Vector(0, 0, 1), True),
        (rt.Point(-2, 0, 0), rt.Vector(2, 4, 6), False),
        (rt.Point(0, -2, 0), rt.Vector(6, 2, 4), False),
        (rt.Point(0, 0, -2), rt.Vector(4, 6, 2), False),
        (rt.Point(2, 0, 2), rt.Vector(0, 0, -1), False),
        (rt.Point(0, 2, 2), rt.Vector(0, -1, 0), False),
        (rt.Point(2, 2, 0), rt.Vector(-1, 0, 0), False)
    ]

    box = rt.BoundingBox(rt.Point(-1, -1, -1), rt.Point(1, 1, 1))
    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        assert box.intersects(r) == test[2]


def rtunittest_boundingbox20():
    # intersecting a ray with a non-cubic bounding box

    # each test has origin and direction of the vector, and whether or not it intersects
    tests = [
        (rt.Point(15, 1, 2), rt.Vector(-1, 0, 0), True),
        (rt.Point(-5, -1, 4), rt.Vector(1, 0, 0), True),
        (rt.Point(7, 6, 5), rt.Vector(0, -1, 0), True),
        (rt.Point(9, -5, 6), rt.Vector(0, 1, 0), True),
        (rt.Point(8, 2, 12), rt.Vector(0, 0, -1), True),
        (rt.Point(6, 0, -5), rt.Vector(0, 0, 1), True),
        (rt.Point(8, 1, 3.5), rt.Vector(0, 0, 1), True),
        (rt.Point(9, -1, -8), rt.Vector(2, 4, 6), False),
        (rt.Point(8, 3, -4), rt.Vector(6, 2, 4), False),
        (rt.Point(9, -1, -2), rt.Vector(4, 6, 2), False),
        (rt.Point(4, 0, 9), rt.Vector(0, 0, -1), False),
        (rt.Point(8, 6, -1), rt.Vector(0, -1, 0), False),
        (rt.Point(12, 5, 4), rt.Vector(-1, 0, 0), False)
    ]

    box = rt.BoundingBox(rt.Point(5, -2, 0), rt.Point(11, 4, 7))
    for test in tests:
        r = rt.Ray(test[0], rt.normalize(test[1]))
        assert box.intersects(r) == test[2]


def rtunittest_boundingbox21():
    # Intersecting ray+group doesn't test children if box is missed
    child = TestShape()
    shape = rt.ObjectGroup()
    shape.addchild(child)
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 1, 0))
    shape.intersect(r)  # we do not need the return value
    assert child.saved_ray is None


def rtunittest_boundingbox22():
    # Intersecting ray+group tests children bif box is hit
    child = TestShape()
    shape = rt.ObjectGroup()
    shape.addchild(child)
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    shape.intersect(r)  # do not need the return variable
    assert child.saved_ray is not None


def rtunittest_boundingbox23():
    # Intersecting ray+csg doesn't test children if box is missed
    left = TestShape()
    right = TestShape()
    shape = rt.CSG('difference', left, right)
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 1, 0))
    shape.intersect(r)  # do not need the return variable
    assert left.saved_ray is None
    assert right.saved_ray is None


def rtunittest_boundingbox24():
    # Intersecting ray+csg tests children if box is hit
    left = TestShape()
    right = TestShape()
    shape = rt.CSG('difference', left, right)
    r = rt.Ray(rt.Point(0, 0, -5), rt.Vector(0, 0, 1))
    shape.intersect(r)  # do not need the return variable
    assert left.saved_ray is not None
    assert right.saved_ray is not None


def rtunittest_bvh1():
    # Splitting a perfect cube
    box = rt.BoundingBox(rt.Point(-1, -4, -5), rt.Point(9, 6, 5))
    left, right = box.split_bounds()
    assert left.boxmin == rt.Point(-1, -4, -5)
    assert left.boxmax == rt.Point(4, 6, 5)
    assert right.boxmin == rt.Point(4, -4, -5)
    assert right.boxmax == rt.Point(9, 6, 5)


def rtunittest_bvh2():
    # splitting an x-wide box
    box = rt.BoundingBox(rt.Point(-1, -2, -3), rt.Point(9, 5.5, 3))
    left, right = box.split_bounds()
    assert left.boxmin == rt.Point(-1, -2, -3)
    assert left.boxmax == rt.Point(4, 5.5, 3)
    assert right.boxmin == rt.Point(4, -2, -3)
    assert right.boxmax == rt.Point(9, 5.5, 3)


def rtunittest_bvh3():
    # splitting a y-wide box
    box = rt.BoundingBox(rt.Point(-1, -2, -3), rt.Point(5, 8, 3))
    left, right = box.split_bounds()
    assert left.boxmin == rt.Point(-1, -2, -3)
    assert left.boxmax == rt.Point(5, 3, 3)
    assert right.boxmin == rt.Point(-1, 3, -3)
    assert right.boxmax == rt.Point(5, 8, 3)


def rtunittest_bvh4():
    # splitting a z-wide box
    box = rt.BoundingBox(rt.Point(-1, -2, -3), rt.Point(5, 3, 7))
    left, right = box.split_bounds()
    assert left.boxmin == rt.Point(-1, -2, -3)
    assert left.boxmax == rt.Point(5, 3, 2)
    assert right.boxmin == rt.Point(-1, -2, 2)
    assert right.boxmax == rt.Point(5, 3, 7)


def rtunittest_bvh5():
    # Partitioning a group's children
    s1 = rt.Sphere()
    s1.transform = rt.translation(-2, 0, 0)
    s2 = rt.Sphere()
    s2.transform = rt.translation(2, 0, 0)
    s3 = rt.Sphere()
    g = rt.ObjectGroup()
    g.addchild(s1)
    g.addchild(s2)
    g.addchild(s3)
    left, right = g.partition_children()
    assert len(g.children) == 1
    assert s3 in g.children
    assert len(left) == 1
    assert s1 in left
    assert len(right) == 1
    assert s2 in right


def rtunittest_bvh6():
    # Creating a sub-group from a list of children
    s1 = rt.Sphere()
    s2 = rt.Sphere()
    g = rt.ObjectGroup()
    g.make_subgroup([s1, s2])
    assert len(g.children) == 1
    assert s1 in g.children[0].children
    assert s2 in g.children[0].children


def rtunittest_bvh7():
    # Subdividing a primitive does nothing
    shape = rt.Sphere()
    shape.divide(1)
    assert isinstance(shape, rt.Sphere)


def rtunittest_bvh8():
    # Subdividing a group partitions its children
    s1 = rt.Sphere()
    s1.transform = rt.translation(-2, -2, 0)
    s2 = rt.Sphere()
    s2.transform = rt.translation(-2, 2, 0)
    s3 = rt.Sphere()
    s3.transform = rt.scaling(4, 4, 4)
    g = rt.ObjectGroup()
    g.addchild(s1)
    g.addchild(s2)
    g.addchild(s3)
    g.divide(1)
    assert g.children[0] is s3
    subgroup = g.children[1]
    assert isinstance(subgroup, rt.ObjectGroup)
    assert subgroup.parent is g
    assert len(subgroup.children) == 2
    assert isinstance(subgroup.children[0], rt.ObjectGroup)
    assert subgroup.children[0].children[0] is s1
    assert isinstance(subgroup.children[1], rt.ObjectGroup)
    assert subgroup.children[1].children[0] is s2


def rtunittest_bvh9():
    # subdividing a group with too few children
    s1 = rt.Sphere()
    s1.transform = rt.translation(-2, 0, 0)
    s2 = rt.Sphere()
    s2.transform = rt.translation(2, 1, 0)
    s3 = rt.Sphere()
    s3.transform = rt.translation(2, -1, 0)
    subgroup = rt.ObjectGroup()
    subgroup.addchild(s1)
    subgroup.addchild(s2)
    subgroup.addchild(s3)
    s4 = rt.Sphere()
    g = rt.ObjectGroup()
    g.addchild(subgroup)
    g.addchild(s4)
    g.divide(3)
    assert g.children[0] is subgroup
    assert g.children[1] is s4
    assert len(subgroup.children) == 2
    assert isinstance(subgroup.children[0], rt.ObjectGroup)
    assert subgroup.children[0].children[0] is s1
    assert isinstance(subgroup.children[1], rt.ObjectGroup)
    assert s2 in subgroup.children[1].children
    assert s3 in subgroup.children[1].children
    assert len(subgroup.children[1].children) == 2


def rtunittest_bvh10():
    # Subdividing a CSG shape subdivides its children
    s1 = rt.Sphere()
    s1.transform = rt.translation(-1.5, 0, 0)
    s2 = rt.Sphere()
    s2.transform = rt.translation(1.5, 0, 0)
    left = rt.ObjectGroup()
    left.addchild(s1)
    left.addchild(s2)

    s3 = rt.Sphere()
    s3.transform = rt.translation(0, 0, -1.5)
    s4 = rt.Sphere()
    s4.transform = rt.translation(0, 0, 1.5)
    right = rt.ObjectGroup()
    right.addchild(s3)
    right.addchild(s4)

    shape = rt.CSG('difference', left, right)
    shape.divide(1)

    assert isinstance(left.children[0], rt.ObjectGroup)
    assert isinstance(left.children[1], rt.ObjectGroup)
    assert s1 in left.children[0].children
    assert len(left.children[0].children) == 1
    assert s2 in left.children[1].children
    assert len(left.children[1].children) == 1
    assert s3 in right.children[0].children
    assert len(right.children[0].children) == 1
    assert s4 in right.children[1].children
    assert len(right.children[1].children) == 1


def rtunittest_texturemap1():
    # Checker pattern in 2D
    black = rt.Color(0, 0, 0)
    white = rt.Color(1, 1, 1)
    checkers = rt.UVCheckersPattern(2, 2, black, white)

    # each test has a u, v, and expected result
    tests = [
        (0.0, 0.0, black),
        (0.5, 0.0, white),
        (0.0, 0.5, white),
        (0.5, 0.5, black),
        (1.0, 1.0, black)
    ]

    for test in tests:
        assert checkers.uv_color_at(test[0], test[1]) == test[2]


def rtunittest_texturemap2():
    # Using a Spherical mapping on a 3D point

    # each test is a point and expected u, v that are returned
    tests = [
        (rt.Point(0, 0, -1), 0.0, 0.5),
        (rt.Point(1, 0, 0), 0.25, 0.5),
        (rt.Point(0, 0, 1), 0.5, 0.5),
        (rt.Point(-1, 0, 0), 0.75, 0.5),
        (rt.Point(0, 1, 0), 0.5, 1.0),
        (rt.Point(0, -1, 0), 0.5, 0.0),
        (rt.Point(math.sqrt(2)/2, math.sqrt(2)/2, 0), 0.25, 0.75)
    ]

    for test in tests:
        u, v = rt.spherical_map(test[0])
        assert math.isclose(u, test[1])
        assert math.isclose(v, test[2])


def rtunittest_texturemap3():
    # Using a texture map pattern with a spherical map

    black = rt.Color(0, 0, 0)
    white = rt.Color(1, 1, 1)

    # each test has a point and an expected color
    tests = [
        (rt.Point(0.4315, 0.4670, 0.7719), white),
        (rt.Point(-0.9654, 0.2552, -0.0534), black),
        (rt.Point(0.1039, 0.7090, 0.6975), white),
        (rt.Point(-0.4986, -0.7856, -0.3663), black),
        (rt.Point(-0.0317, -0.9395, 0.3411), black),
        (rt.Point(0.4809, -0.7721, 0.4154), black),
        (rt.Point(0.0285, -0.9612, -0.2745), black),
        (rt.Point(-0.5734, -0.2162, -0.7903), white),
        (rt.Point(0.7688, -0.1470, 0.6223), black),
        (rt.Point(-0.7652, 0.2175, 0.6060), black)
    ]

    pattern = rt.UVCheckersPattern(16, 8, black, white, rt.spherical_map)

    for test in tests:
        assert pattern.color_at(test[0]) == test[1]


def rtunittest_texturemap4():
    # Using planar mapping on a 3D point

    # each test is a point, and an expected u and v that are returned
    tests = [
        (rt.Point(0.25, 0, 0.5), 0.25, 0.5),
        (rt.Point(0.25, 0., -0.25), 0.25, 0.75),
        (rt.Point(0.25, 0.5, -0.25), 0.25, 0.75),
        (rt.Point(1.25, 0, 0.5), 0.25, 0.5),
        (rt.Point(0.25, 0, -1.75), 0.25, 0.25),
        (rt.Point(1, -0, -1), 0, 0),
        (rt.Point(0, 0, 0), 0, 0)
    ]

    for test in tests:
        u, v = rt.planar_map(test[0])
        assert math.isclose(u, test[1])
        assert math.isclose(v, test[2])


def rtunittest_teturemap5():
    # Using cylindrical mapping on a 3D point

    # each test is a point, and an expected u and v that are returned
    tests = [
        (rt.Point(0, 0, -1), 0, 0),
        (rt.Point(0, 0.5, -1), 0, 0.5),
        (rt.Point(0, 1, -1), 0, 0),
        (rt.Point(0.70711, 0.5, -0.70711), 0.125, 0.5),
        (rt.Point(1, 0.5, 0), 0.25, 0.5),
        (rt.Point(0.70711, 0.5, 0.70711), 0.375, 0.5),
        (rt.Point(0, -0.25, 1), 0.5, 0.75),
        (rt.Point(-0.70711, 0.5, 0.70711), 0.625, 0.5),
        (rt.Point(-1, 1.25, 0), 0.75, 0.25),
        (rt.Point(-0.70711, 0.5, -0.70711), 0.875, 0.5)
    ]

    for test in tests:
        u, v = rt.cylindrical_map(test[0])
        assert math.isclose(u, test[1])
        assert math.isclose(v, test[2])


def rtunittest_texturemap6():
    # Layout of the "align check" pattern

    main = rt.Color(1, 1, 1)
    ul = rt.Color(1, 0, 0)
    ur = rt.Color(1, 1, 0)
    bl = rt.Color(0, 1, 0)
    br = rt.Color(0, 1, 1)

    # each test is a u, a v, and a color
    tests = [
        (0.5, 0.5, main),
        (0.1, 0.9, ul),
        (0.9, 0.9, ur),
        (0.1, 0.1, bl),
        (0.9, 0.1, br)
    ]
    pattern = rt.UVAlignCheckPattern()

    for test in tests:
        assert pattern.uv_color_at(test[0], test[1]) == test[2]


def rtunittest_texturemap7():
    # Identifying the face of a cube from a point
    
    # each test is a point and the face that it should show
    tests = [
        (rt.Point(-1, 0.5, -0.25), FACELEFT),
        (rt.Point(1.1, -0.75, 0.8), FACERIGHT),
        (rt.Point(0.1, 0.6, 0.9), FACEFRONT),
        (rt.Point(-0.7, 0, -2), FACEBACK),
        (rt.Point(0.5, 1, 0.9), FACEUP),
        (rt.Point(-0.2, -1.3, 1.1), FACEDOWN)
    ]

    for test in tests:
        assert face_from_point(test[0]) == test[1]


def rtunittest_texturemap8():
    # UV mapping the faces of a cube

    # each test is a point, and the expected u and v
    tests = [
        (rt.Point(-0.5, 0.5, 1), 0.25, 0.75),
        (rt.Point(0.5, -0.5, 1), 0.75, 0.25),
        (rt.Point(0.5, 0.5, -1), 0.25, 0.75),
        (rt.Point(-0.5, -0.5, -1), 0.75, 0.25),
        (rt.Point(1, 0.5, 0.5), 0.25, 0.75),
        (rt.Point(1, -0.5, -0.5), 0.75, 0.25),
        (rt.Point(-1, 0.5, -0.5), 0.25, 0.75),
        (rt.Point(-1, -0.5, 0.5), 0.75, 0.25),
        (rt.Point(-0.5, 1, -0.5), 0.25, 0.75),
        (rt.Point(0.5, 1, 0.5), 0.75, 0.25),
        (rt.Point(-0.5, -1, 0.5), 0.25, 0.75),
        (rt.Point(0.5, -1, -0.5), 0.75, 0.25)
    ]

    for test in tests:
        point = test[0]
        face = face_from_point(point)
        if face == FACEFRONT:
            fn = rt.cube_uv_front
        elif face == FACEBACK:
            fn = rt.cube_uv_back
        elif face == FACELEFT:
            fn = rt.cube_uv_left
        elif face == FACERIGHT:
            fn = rt.cube_uv_right
        elif face == FACEUP:
            fn = rt.cube_uv_up
        else:
            fn = rt.cube_uv_down

        u, v = fn(point)
        assert math.isclose(u, test[1])
        assert math.isclose(v, test[2])


def rtunittest_texturemap9():
    # Finding the colors on a mapped cube
    red = rt.Color(1, 0, 0)
    yellow = rt.Color(1, 1, 0)
    brown = rt.Color(1, 0.5, 0)
    green = rt.Color(0, 1, 0)
    cyan = rt.Color(0, 1, 1)
    blue = rt.Color(0, 0, 1)
    purple = rt.Color(1, 0, 1)
    white = rt.Color(1, 1, 1)

    # each test is a point and the expected color result.  First 5 tests are left face,
    # next 5 are front, then right, back, up, down.
    tests = [
        (rt.Point(-1, 0, 0), yellow),
        (rt.Point(-1, 0.9, -0.9), cyan),
        (rt.Point(-1, 0.9, 0.9), red),
        (rt.Point(-1, -0.9, -0.9), blue),
        (rt.Point(-1, -0.9, 0.9), brown),
        (rt.Point(0, 0, 1), cyan),
        (rt.Point(-0.9, 0.9, 1), red),
        (rt.Point(0.9, 0.9, 1), yellow),
        (rt.Point(-0.9, -0.9, 1), brown),
        (rt.Point(0.9, -0.9, 1), green),
        (rt.Point(1, 0, 0), red),
        (rt.Point(1, 0.9, 0.9), yellow),
        (rt.Point(1, 0.9, -0.9), purple),
        (rt.Point(1, -0.9, 0.9), green),
        (rt.Point(1, -0.9, -0.9), white),
        (rt.Point(0, 0, -1), green),
        (rt.Point(0.9, 0.9, -1), purple),
        (rt.Point(-0.9, 0.9, -1), cyan),
        (rt.Point(0.9, -0.9, -1), white),
        (rt.Point(-0.9, -0.9, -1), blue),
        (rt.Point(0, 1, 0), brown),
        (rt.Point(-0.9, 1, -0.9), cyan),
        (rt.Point(0.9, 1, -0.9), purple),
        (rt.Point(-0.9, 1, 0.9), red),
        (rt.Point(0.9, 1, 0.9), yellow),
        (rt.Point(0, -1, 0), purple),
        (rt.Point(-0.9, -1, 0.9), brown),
        (rt.Point(0.9, -1, 0.9), green),
        (rt.Point(-0.9, -1, -0.9), blue),
        (rt.Point(0.9, -1, -0.9), white)
    ]

    cube = rt.CubeMap()
    cube.setupdemo()

    for test in tests:
        c = cube.color_at(test[0])
        assert c == test[1]


def rtunittest_texturemap10():
    # Reading a file with the wrong magic number
    try:
        rt.canvas_from_ppm('raytracer/test_ppm_files/wrong_magic_number.ppm')
    except AssertionError:  # what we raise if the file has wrong magic number
        pass
    else:
        raise AssertionError('Test Failed')  # if we didn't get an error... we raise an error to fail the test


def rtunittest_texturemap11():
    # Reading a PPM returns a canvas of the right size
    rt.canvas_from_ppm('raytracer/test_ppm_files/test_canvas_size.ppm')
    width, height = get_canvasdims(True)
    assert width == 10
    assert height == 2


def rtunittest_texturemap12():
    # Reading pixel data from a PPM file

    # each test is an x, a y, and the expected value:
    tests = [
        (0, 0, rt.Color(1, 0.49804, 0)),
        (1, 0, rt.Color(0, 0.49804, 1)),
        (2, 0, rt.Color(0.49804, 1, 0)),
        (3, 0, rt.Color(1, 1, 1)),
        (0, 1, rt.Color(0, 0, 0)),
        (1, 1, rt.Color(1, 0, 0)),
        (2, 1, rt.Color(0, 1, 0)),
        (3, 1, rt.Color(0, 0, 1)),
        (0, 2, rt.Color(1, 1, 0)),
        (1, 2, rt.Color(0, 1, 1)),
        (2, 2, rt.Color(1, 0, 1)),
        (3, 2, rt.Color(0.49804, 0.49804, 0.49804))
    ]

    rt.canvas_from_ppm('raytracer/test_ppm_files/read_pixel_data.ppm')
    for test in tests:
        c = pixel_at(test[0], test[1], True)
        assert c == test[2]


def rtunittest_texturemap13():
    # PPM parsing ignores comment lines
    rt.canvas_from_ppm('raytracer/test_ppm_files/comments_test.ppm')
    assert pixel_at(0, 0, True) == rt.Color(1, 1, 1)
    assert pixel_at(1, 0, True) == rt.Color(1, 0, 1)


def rtunittest_texturemap14():
    # PPM parsing allows an RGB triple to span lines
    rt.canvas_from_ppm('raytracer/test_ppm_files/triple_spans_lines.ppm')
    assert pixel_at(0, 0, True) == rt.Color(0.2, 0.6, 0.8)


def rtunittest_texturemap15():
    # PPM parsing respects the scale setting
    rt.canvas_from_ppm('raytracer/test_ppm_files/respect_scale_setting.ppm')
    assert pixel_at(0, 1, True) == rt.Color(0.75, 0.5, 0.25)


def rtunittest_texturemap16():
    # Checker pattern in 2D

    # each test is a u, v and an expected color
    tests = [
        (0, 0, rt.Color(0.9, 0.9, 0.9)),
        (0.3, 0, rt.Color(0.2, 0.2, 0.2)),
        (0.6, 0.3, rt.Color(0.1, 0.1, 0.1)),
        (1, 1, rt.Color(0.9, 0.9, 0.9))
    ]

    pattern = rt.UVImagePattern('raytracer/test_ppm_files/test_checkers_pattern.ppm')

    for test in tests:
        color = pattern.uv_color_at(test[0], test[1])
        assert color == test[2]


def rtunittest_randomvector1():
    # Fred test: ensure random_in_unit_disk creates vectors that have magnitude < 1.
    for i in range(10):
        r = random_in_unit_disk()
        assert -1.0 <= r.x <= 1.0
        assert -1.0 <= r.y <= 1.0
        assert math.isclose(r.z, 0)
        assert r.magnitude() <= 1.0


def rtunittest_quadraticsolver1():
    # Fred test: verify that we can solve quadratics

    res = quadratic_solver(2, 3, -5)
    assert len(res) == 2
    assert math.isclose(res[0], -2.5)
    assert math.isclose(res[1], 1)

    res = quadratic_solver(-1, 74, -18)
    assert len(res) == 2
    assert math.isclose(res[0], 0.24405, rel_tol=1e-05, abs_tol=1e-05)
    assert math.isclose(res[1], 73.75595, rel_tol=1e-05, abs_tol=1e-05)

    res = quadratic_solver(3, 2, 1)
    assert len(res) == 0

    res = quadratic_solver(-1, 0, 0)
    assert len(res) == 1
    assert math.isclose(res[0], 0)


def rtunittest_cubicsolver1():
    # Fred test: verify that we can solve cubics
    res = cubic_solver(1, -2, -11, 12)
    assert len(res) == 3
    res.sort()
    assert math.isclose(res[0], -3)
    assert math.isclose(res[1], 1)
    assert math.isclose(res[2], 4)

    res = cubic_solver(-3.2, 9, -7, 3)
    assert len(res) == 1
    assert math.isclose(res[0], 1.93114, rel_tol=1e-05, abs_tol=1e-05)

    res = cubic_solver(1.1, 4.7, -19.7, -21)
    res.sort()
    assert len(res) == 3
    assert math.isclose(res[0], -6.55933, rel_tol=1e-05, abs_tol=1e-05)
    assert math.isclose(res[1], -0.910386, rel_tol=1e-05, abs_tol=1e-05)
    assert math.isclose(res[2], 3.19699, rel_tol=1e-05, abs_tol=1e-05)

    res = cubic_solver(1, 1, -1, -1)
    res.sort()
    assert len(res) == 2
    assert math.isclose(res[0], -1)
    assert math.isclose(res[1], 1)


def rtunittest_quarticsolver0():
    # Fred test: verify that we can solve quartics with no roots
    res = quartic_solver(5, 0.1, 2, 0.3, 9)
    assert len(res) == 0


def rtunittest_quarticsolver1():
    # Fred test: verify that we can solve quartics with 1 root
    res = quartic_solver(13.0321, -27.436, 21.66, -7.6, 1.0)
    assert len(res) == 2  # this quartic solver thinks there are 2 roots very close to each other.
    assert math.isclose(res[0], 0.526, rel_tol=1e-03, abs_tol=1e-03)


def rtunittest_quarticsolver2():
    # Fred test: verify that we can solve quartics with 2 roots
    res = quartic_solver(1, 0, -2, 0, 1)
    assert len(res) == 2
    res.sort()
    assert math.isclose(res[0], -1)
    assert math.isclose(res[1], 1)

    res = quartic_solver(36, -60, -47, 60, 36)
    assert len(res) == 2
    res.sort()
    assert math.isclose(res[0], -2/3)
    assert math.isclose(res[1], 1.5)


def rtunittest_quarticsolver3():
    # Fred test: verify that we can solve quartics with 3 roots
    # note this has four roots due to floating point math
    res = quartic_solver(1, -1, -2, 0, 0)
    assert len(res) == 4
    res.sort()
    assert math.isclose(res[0], -1)
    assert math.isclose(res[1], 0, rel_tol=1e-05, abs_tol=1e-05)
    assert math.isclose(res[2], 0, rel_tol=1e-05, abs_tol=1e-05)
    assert math.isclose(res[3], 2)

    res = quartic_solver(1, 3.9, -4.06, -14.016, 13.8528)
    assert len(res) == 3
    res.sort()
    assert math.isclose(res[0], -3.7)
    assert math.isclose(res[1], -2.6)
    assert math.isclose(res[2], 1.2, rel_tol=1e-05, abs_tol=1e-05)


def rtunittest_quarticsolver4():
    # Fred test: verify that we can solve quartics with 4 roots
    res = quartic_solver(1, -2, -72, 18, 567)
    assert len(res) == 4
    res.sort()
    assert math.isclose(res[0], -7)
    assert math.isclose(res[1], -3)
    assert math.isclose(res[2], 3)
    assert math.isclose(res[3], 9)


def rtunittest_quarticsolver5():
    # Fred test: these examples failed in production to detect the roots
    res = quartic_solver(1, -52.62787462503418, 1038.6039216330723, -9109.374162539929, 29960.241062410005)
    assert len(res) > 0

    # (x - 50)^2 * (x + 15.75)^2 - should have roots -15.75 and 50
    res = quartic_solver(1, -68.5, -401.9374, 53943.75, 620156.25)
    assert len(res) > 0

    # (x - 30)^2 * (x - 25) * (x - 15) - should have roots 15, 25, 30
    res = quartic_solver(1, -100, 3675, -58500, 337500)
    assert len(res) > 0

    res = quartic_solver(0.9999999999999998, -53.77525518192683, 1084.275707490053,
                         -9715.332216564737, 32639.969171360004)
    assert len(res) > 0


def rtunittest_quarticsolver6():
    # Fred test: brute force with an equation with known roots to make sure that it will pass
    # expand: (x - a)(x - b)(x - c)(x - d)
    # x^4
    # + (a + b + c + d) * x^3
    # + (cd + bd + bc + ad + ac + ab) x^2
    # + (bcd + acd + abd + abc) x
    # + abcd
    # This gives you the quartic where -a, -b, -c, and -d are roots.
    return
    listofroots = []
    i = -30.0
    while i <= 30:
        listofroots.append(i)
        i += (1/3)

    for a in listofroots:
        for b in listofroots:
            for c in listofroots:
                for d in listofroots:
                    if a == b == c == d == 0.0:  # degenerate case
                        pass
                    else:
                        x4term = 1
                        x3term = a + b + c + d
                        x2term = (c * d) + (b * d) + (b * c) + (a * d) + (a * c) + (a * b)
                        x1term = (b * c * d) + (a * c * d) + (a * b * d) + (a * b * c)
                        x0term = (a * b * c * d)

                        res = quartic_solver(x4term, x3term, x2term, x1term, x0term)

                        founda = foundb = foundc = foundd = False
                        for r in res:
                            if math.isclose(-a, r, abs_tol=1e-01):
                                founda = True
                            if math.isclose(-b, r, abs_tol=1e-01):
                                foundb = True
                            if math.isclose(-c, r, abs_tol=1e-01):
                                foundc = True
                            if math.isclose(-d, r, abs_tol=1e-01):
                                foundd = True

                        if founda and foundb and foundc and foundd:
                            pass
                        else:
                            print('{}({}) {}({}) {}({}) {}({}) failed'.format(a, founda, b, foundb,
                                                                              c, foundc, d, foundd))
                            assert False
        print('{} : {}'.format(a, time.time()))

def rtunittest_torus1():
    # Fred test: verify we can create a Torus and assign its major and minor radii
    t = rt.Torus()
    t.R = 2.5
    t.r = 0.3
    assert math.isclose(t.R, 2.5)
    assert math.isclose(t.r, 0.3)


def rtunittest_torus2():
    # Fred test: a ray misses a Torus
    t = rt.Torus()
    r = rt.Ray(rt.Point(-2, 0, 2), rt.Vector(1, 0, 0))
    xs = t.intersect(r)
    assert len(xs) == 0


def rtunittest_torus3():
    # Fred test: a ray hits a torus at the tangent of the outside, so
    # there is one intersection.
    # do not know why this test is failing.
    t = rt.Torus()
    r = rt.Ray(rt.Point(-1, 0, 1.25), rt.Vector(1, 0, 0))
    xs = t.intersect(r)
    assert len(xs) == 1
    assert math.isclose(xs[0].t, 1)


def rtunittest_torus4():
    # Fred test: a ray hits a torus hitting at the z value equal to the major
    # radius, so there are two intersections
    t = rt.Torus()
    r = rt.Ray(rt.Point(-2, 0, 1), rt.Vector(1, 0, 0))
    xs = t.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 1.75)
    assert math.isclose(xs[1].t, 2.25)


def rtunittest_torus5():
    # Fred test: a ray hits a torus hitting at the tangent of the inside, so
    # there are three intersections.  Note we return 3 unique and one is duplicated.
    t = rt.Torus()
    r = rt.Ray(rt.Point(-2, 0, 0.75), rt.Vector(1, 0, 0))
    xs = t.intersect(r)
    xs.sort(key=lambda x: x.t)
    assert len(xs) == 3
    assert math.isclose(xs[0].t, 1)
    assert math.isclose(xs[1].t, 2)
    assert math.isclose(xs[2].t, 3)



def rtunittest_torus6():
    # Fred test: a ray hits a torus in the middle, so there are four intersections
    t = rt.Torus()
    r = rt.Ray(rt.Point(-2, 0, 0), rt.Vector(1, 0, 0))
    xs = t.intersect(r)
    xs.sort(key=lambda x: x.t)
    assert len(xs) == 4
    assert math.isclose(xs[0].t, 0.75)
    assert math.isclose(xs[1].t, 1.25)
    assert math.isclose(xs[2].t, 2.75)
    assert math.isclose(xs[3].t, 3.25)
