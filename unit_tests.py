import math
import numpy as np
import tuple
import canvas
import transformations
import objects
import lights
import materials
import world


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


def test_point1():
    # A tuple with w=1.0 is a point
    t = tuple.RT_Tuple(4.3, -4.2, 3.1, 1.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert t.ispoint()
    assert not t.isvector()


def test_vector1():
    # A tuple with w=0 is a vector
    t = tuple.RT_Tuple(4.3, -4.2, 3.1, 0.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert not t.ispoint()
    assert t.isvector()


def test_point2():
    # Point() creates tuples with w=1
    p = tuple.Point(4.0, -4.0, 3.0)
    assert isinstance(p, tuple.RT_Tuple)
    assert p == tuple.RT_Tuple(4.0, -4.0, 3.0, 1.0)


def test_vector2():
    # Vector() creates tuples with w=0
    p = tuple.Vector(4, -4, 3)
    assert isinstance(p, tuple.RT_Tuple)
    assert p == tuple.RT_Tuple(4.0, -4.0, 3.0, 0.0)


def test_add1():
    # Adding two tuples
    p1 = tuple.RT_Tuple(3, -2, 5, 1)
    p2 = tuple.RT_Tuple(-2, 3, 1, 0)
    assert p1 + p2 == tuple.RT_Tuple(1, 1, 6, 1)


def test_sub1():
    # Subtracting two points
    p1 = tuple.Point(3, 2, 1)
    p2 = tuple.Point(5, 6, 7)
    assert p1 - p2 == tuple.Vector(-2, -4, -6)


def test_sub2():
    # Subtracting a vector from a point
    p = tuple.Point(3, 2, 1)
    v = tuple.Vector(5, 6, 7)
    assert p - v == tuple.Point(-2, -4, -6)


def test_sub3():
    # Subtracting two vectors
    v1 = tuple.Vector(3, 2, 1)
    v2 = tuple.Vector(5, 6, 7)
    assert v1 - v2 == tuple.Vector(-2, -4, -6)


def test_negation1():
    # Subtracting a vector from the zero vector
    zero = tuple.Vector(0, 0, 0)
    v = tuple.Vector(1, -2, 3)
    assert zero - v == tuple.Vector(-1, 2, -3)


def test_negation2():
    # Negating a tuple
    a = tuple.RT_Tuple(1, -2, 3, -4)
    assert -a == tuple.RT_Tuple(-1, 2, -3, 4)


def test_scalarmult1():
    # Multiplying a tuple by a scalar
    a = tuple.RT_Tuple(1, -2, 3, -4)
    assert a * 3.5 == tuple.RT_Tuple(3.5, -7, 10.5, -14)


def test_scalarmult2():
    # Multiplying a tuple by a fraction
    a = tuple.RT_Tuple(1, -2, 3, -4)
    assert a * 0.5 == tuple.RT_Tuple(0.5, -1, 1.5, -2)


def test_tuplemult1():
    # Multiplying a tuple by a tuple
    a = tuple.RT_Tuple(2, 3, 4, 5)
    b = tuple.RT_Tuple(0.5, 4, -1.2, 1.5)
    assert a * b == tuple.RT_Tuple(1, 12, -4.8, 7.5)


def test_scalardiv1():
    # Dividing a tuple by a scalar
    a = tuple.RT_Tuple(1, -2, 3, -4)
    assert a / 2 == tuple.RT_Tuple(0.5, -1, 1.5, -2)


def test_tuplediv1():
    # Dividing a tuple by a tuple
    a = tuple.RT_Tuple(3, 4, 5, 6)
    b = tuple.RT_Tuple(1, 2, -2.5, 4)
    assert a / b == tuple.RT_Tuple(3, 2, -2, 1.5)


def test_magnitude1():
    # Computing the magnitude of vector (1,0,0)
    v = tuple.Vector(1, 0, 0)
    assert v.magnitude() == 1


def test_magnitude2():
    # Computing the magnitude of vector (0,1,0)
    v = tuple.Vector(0, 1, 0)
    assert v.magnitude() == 1


def test_magnitude3():
    # Computing the magnitude of vector (0,0,1)
    v = tuple.Vector(0, 0, 1)
    assert v.magnitude() == 1


def test_magnitude4():
    # Computing the magnitude of vector (1,2,3)
    v = tuple.Vector(1, 2, 3)
    assert v.magnitude() == math.sqrt(14)


def test_magnitude5():
    # Computing the magnitude of vector (-1, -2, -3)
    v = tuple.Vector(-1, -2, -3)
    assert v.magnitude() == math.sqrt(14)


def test_normalize1():
    # Normalizing vector (4,0,0) gives (1,0,0)
    v = tuple.Vector(4, 0, 0)
    assert tuple.normalize(v) == tuple.Vector(1, 0, 0)


def test_normalize2():
    # Normalizing vector (1, 2, 3)
    v = tuple.Vector(1, 2, 3)
    assert tuple.normalize(v) == tuple.Vector(0.26726, 0.53452, 0.80178)


def test_dot1():
    # The dot product of two tuples
    a = tuple.RT_Tuple(1, 2, 3)
    b = tuple.RT_Tuple(2, 3, 4)
    assert tuple.dot(a, b) == 20


def test_cross1():
    # The cross product of two vectors
    a = tuple.Vector(1, 2, 3)
    b = tuple.Vector(2, 3, 4)
    assert tuple.cross(a, b) == tuple.Vector(-1, 2, -1)
    assert tuple.cross(b, a) == tuple.Vector(1, -2, 1)


def test_color1():
    # Adding colors
    c1 = tuple.Color(0.9, 0.6, 0.75)
    c2 = tuple.Color(0.7, 0.1, 0.25)
    assert c1 + c2 == tuple.Color(1.6, 0.7, 1.0)


def test_color2():
    # Subtracting colors
    c1 = tuple.Color(0.9, 0.6, 0.75)
    c2 = tuple.Color(0.7, 0.1, 0.25)
    assert c1 - c2 == tuple.Color(0.2, 0.5, 0.5)


def test_color3():
    # Multiplying a color by a scalar
    c = tuple.Color(0.2, 0.3, 0.4)
    assert c * 2 == tuple.Color(0.4, 0.6, 0.8)


def test_color4():
    # Mutiplying colors
    c1 = tuple.Color(1, 0.2, 0.4)
    c2 = tuple.Color(0.9, 1, 0.1)
    assert c1 * c2 == tuple.Color(0.9, 0.2, 0.04)


def test_canvas1():
    # Creating a canvas
    canvas.init_canvas(10, 20)
    assert canvas.CANVASWIDTH == 10
    assert canvas.CANVASHEIGHT == 20
    black = tuple.Color(0, 0, 0)
    for w in range(10):
        for h in range(20):
            assert canvas.pixel_at(w, h) == black


def test_canvas2():
    # Writing pixels to a canvas
    canvas.init_canvas(10, 20)
    red = tuple.Color(1, 0, 0)
    canvas.write_pixel(2, 3, red)
    assert canvas.pixel_at(2, 3) == red


def test_canvas3():
    # This is the final exercise from chapter 2; will test the ppm generated against a "good" ppm.
    # Note I use different variables, etc, but still get the parabola.
    canvas.init_canvas(900, 550)
    gravity = tuple.Vector(0, -0.1, 0)
    wind = tuple.Vector(-0.01, 0, 0)
    velocity = tuple.normalize(tuple.Vector(1, 1.8, 0)) * 11.25
    red = tuple.Color(1, 0, 0)
    position = tuple.Point(0, 1, 0)

    while 0 <= position.x <= 900 and 0 <= position.y <= 550:
        canvas.write_pixel(int(position.x), int(position.y), red)
        position += velocity
        velocity = velocity + (gravity + wind)  # parens stop Pycharm from complaining about wrong type for gravity.

    canvas.canvas_to_ppm('test_canvas3.ppm')
    compare_ppms('test_canvas3.ppm', 'test_canvas3_success.ppm')


def test_matrix1():
    # A matrix mutliplied by a tuple
    A = np.array([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
    b = tuple.RT_Tuple(1, 2, 3, 1)
    assert tuple.matrix_mult_tuple(A, b) == tuple.RT_Tuple(18, 24, 33, 1)


def test_numpy():
    # These are tests of core numpy methods, mostly here as a reference for me

    A = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    B = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    assert np.allclose(A, B)

    A = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    B = np.array([[2, 3, 4, 5], [6, 7, 8, 9], [8, 7, 6, 5], [4, 3, 2, 1]])
    assert (not np.allclose(A, B))

    A = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    B = np.array([[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]])
    res = np.array([[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]])
    assert np.allclose(np.matmul(A, B), res)

    A = np.array([[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]])
    assert np.allclose(np.matmul(A, np.identity(4)), A)

    A = np.array([[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
    AT = np.array([[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]])
    assert np.allclose(np.matrix.transpose(A), AT)

    A = np.array([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
    assert math.isclose(np.linalg.det(A), -2120)

    A = np.array([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
    assert math.isclose(np.linalg.det(A), 0)

    A = np.array([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
    res = np.array([[0.21805, 0.45113, 0.24060, -0.04511],
                    [-0.80827, -1.45677, -0.44361, 0.52068],
                    [-0.07895, -0.22368, -0.05263, 0.19737],
                    [-0.52256, -0.81391, -0.30075, 0.30639]])
    B = np.linalg.inv(A)
    assert math.isclose(np.linalg.det(A), 532)
    assert np.allclose(B, res, 1e-05, 1e-05)  # need to override the default atol for allclose() to match the book
    assert math.isclose(B[3, 2], -160.0/532.0)
    assert math.isclose(B[2, 3], 105.0/532.0)
    assert np.allclose(np.matmul(A, B), np.identity(4))

    A = np.array([[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]])
    B = np.array([[8, 2, 2, 2], [3, -1, 7, 0], [7, 0, 5, 4], [6, -2, 0, 5]])
    C = np.matmul(A, B)
    assert np.allclose(np.matmul(C, np.linalg.inv(B)), A)


def test_translation1():
    # Multiplying by a translation matrix
    trans = transformations.translation(5, -3, 2)
    p = tuple.Point(-3, 4, 5)
    assert transformations.transform(trans, p) == tuple.Point(2, 1, 7)


def test_translation2():
    # Multiplying by the inverse of a translation matrix
    trans = transformations.translation(5, -3, 2)
    inv = np.linalg.inv(trans)
    p = tuple.Point(-3, 4, 5)
    assert transformations.transform(inv, p) == tuple.Point(-8, 7, 3)


def test_translation3():
    # Translation does not affect vectors
    trans = transformations.translation(5, -3, 2)
    v = tuple.Vector(-3, 4, 5)
    assert transformations.transform(trans, v) == v


def test_scaling1():
    # A scaling matrix applied to a point
    trans = transformations.scaling(2, 3, 4)
    p = tuple.Point(-4, 6, 8)
    assert transformations.transform(trans, p) == tuple.Point(-8, 18, 32)


def test_scaling2():
    # A scaling matrix applied to a vector
    trans = transformations.scaling(2, 3, 4)
    v = tuple.Vector(-4, 6, 8)
    assert transformations.transform(trans, v) == tuple.Vector(-8, 18, 32)


def test_scaling3():
    # Multiplying by the inverse of a scaling matrix
    trans = transformations.scaling(2, 3, 4)
    inv = np.linalg.inv(trans)
    v = tuple.Vector(-4, 6, 8)
    assert transformations.transform(inv, v) == tuple.Vector(-2, 2, 2)


def test_reflection1():
    # Reflection is scaling by a negative value
    trans = transformations.reflection(True, False, False)
    p = tuple.Point(2, 3, 4)
    assert transformations.transform(trans, p) == tuple.Point(-2, 3, 4)


def test_rotation1():
    # Rotating a point around the x axis
    p = tuple.Point(0, 1, 0)
    half_quarter = transformations.rotation_x(math.pi / 4)
    full_quarter = transformations.rotation_x(math.pi / 2)
    assert transformations.transform(half_quarter, p) == tuple.Point(0, math.sqrt(2)/2, math.sqrt(2)/2)
    assert transformations.transform(full_quarter, p) == tuple.Point(0, 0, 1)


def test_rotation2():
    # The inverse of a rotation rotates in the opposite direction
    p = tuple.Point(0, 1, 0)
    half_quarter = transformations.rotation_x(math.pi / 4)
    inv = np.linalg.inv(half_quarter)
    assert transformations.transform(inv, p) == tuple.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2)


def test_rotation3():
    # Rotating a point around the y axis
    p = tuple.Point(0, 0, 1)
    half_quarter = transformations.rotation_y(math.pi / 4)
    full_quarter = transformations.rotation_y(math.pi / 2)
    assert transformations.transform(half_quarter, p) == tuple.Point(math.sqrt(2)/2, 0, math.sqrt(2)/2)
    assert transformations.transform(full_quarter, p) == tuple.Point(1, 0, 0)


def test_rotation4():
    # Rotating a point around the z axis
    p = tuple.Point(0, 1, 0)
    half_quarter = transformations.rotation_z(math.pi / 4)
    full_quarter = transformations.rotation_z(math.pi / 2)
    assert transformations.transform(half_quarter, p) == tuple.Point(-math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert transformations.transform(full_quarter, p) == tuple.Point(-1, 0, 0)


def test_skew1():
    # A shearing transformation moves x in proportion to y
    trans = transformations.skew(1, 0, 0, 0, 0, 0)
    p = tuple.Point(2, 3, 4)
    assert transformations.transform(trans, p) == tuple.Point(5, 3, 4)


def test_skew2():
    # Several other shearing transformations
    p = tuple.Point(2, 3, 4)
    trans1 = transformations.skew(0, 1, 0, 0, 0, 0)
    trans2 = transformations.skew(0, 0, 1, 0, 0, 0)
    trans3 = transformations.skew(0, 0, 0, 1, 0, 0)
    trans4 = transformations.skew(0, 0, 0, 0, 1, 0)
    trans5 = transformations.skew(0, 0, 0, 0, 0, 1)
    assert transformations.transform(trans1, p) == tuple.Point(6, 3, 4)
    assert transformations.transform(trans2, p) == tuple.Point(2, 5, 4)
    assert transformations.transform(trans3, p) == tuple.Point(2, 7, 4)
    assert transformations.transform(trans4, p) == tuple.Point(2, 3, 6)
    assert transformations.transform(trans5, p) == tuple.Point(2, 3, 7)


def test_transformchain1():
    # Individual transformations are applied in sequence
    p = tuple.Point(1, 0, 1)
    A = transformations.rotation_x(math.pi / 2)
    B = transformations.scaling(5, 5, 5)
    C = transformations.translation(10, 5, 7)
    p2 = transformations.transform(A, p)
    assert p2 == tuple.Point(1, -1, 0)
    p3 = transformations.transform(B, p2)
    assert p3 == tuple.Point(5, -5, 0)
    p4 = transformations.transform(C, p3)
    assert p4 == tuple.Point(15, 0, 7)


def test_transformchain2():
    # CHained transformations must be applied in reverse order
    p = tuple.Point(1, 0, 1)
    A = transformations.rotation_x(math.pi / 2)
    B = transformations.scaling(5, 5, 5)
    C = transformations.translation(10, 5, 7)
    T = np.matmul(np.matmul(C, B), A)
    assert transformations.transform(T, p) == tuple.Point(15, 0, 7)


def test_transformchain3():
    # This is the final exercise from chapter 4.
    halfcanvas = 12
    canvas.init_canvas(2 * halfcanvas, 2 * halfcanvas)
    clockradius = int(0.75 * halfcanvas)
    trans = transformations.rotation_y(math.pi / 6)

    gold = tuple.Color(1, 0.84314, 0)
    p = tuple.RT_Tuple(0, 0, 1)  # start at 12 o'clock
    for i in range(13):
        dot = p * clockradius
        canvas.write_pixel(int(dot.x) + halfcanvas, int(dot.z) + halfcanvas, gold)
        p = transformations.transform(trans, p)

    canvas.canvas_to_ppm('test_transformchain3.ppm')
    compare_ppms('test_transformchain3.ppm', 'test_transformchain3_success.ppm')


def test_ray1():
    # Creating and querying a ray
    origin = tuple.Point(1, 2, 3)
    direction = tuple.Vector(4, 5, 6)
    r = tuple.Ray(origin, direction)
    assert r.origin == origin
    assert r.direction == direction


def test_ray2():
    # Computing a point from a distance
    r = tuple.Ray(tuple.Point(2, 3, 4), tuple.Vector(1, 0, 0))
    assert r.at(0) == tuple.Point(2, 3, 4)
    assert r.at(1) == tuple.Point(3, 3, 4)
    assert r.at(-1) == tuple.Point(1, 3, 4)
    assert r.at(2.5) == tuple.Point(4.5, 3, 4)


def test_sphereintersect1():
    # A ray intersects a sphere at two points
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 4.0)
    assert math.isclose(xs[1].t, 6.0)


def test_sphereintersect2():
    # A ray intersects a sphere at a tangent
    r = tuple.Ray(tuple.Point(0, 1, -5), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 5.0)
    assert math.isclose(xs[1].t, 5.0)


def test_sphereintersect3():
    # A ray misses a sphere
    r = tuple.Ray(tuple.Point(0, 2, -5), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 0


def test_sphereintersect4():
    # A ray originates inside a sphere
    r = tuple.Ray(tuple.Point(0, 0, 0), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, -1.0)
    assert math.isclose(xs[1].t, 1.0)


def test_sphereintersect5():
    # A sphere is behind a ray
    r = tuple.Ray(tuple.Point(0, 0, 5), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, -6.0)
    assert math.isclose(xs[1].t, -4.0)


def test_intersection1():
    # An intersection encapsulates t and object
    s = objects.Sphere()
    i = objects.Intersection(s, 3.5)
    assert math.isclose(i.t, 3.5)
    assert i.objhit is s


def test_intersection2():
    # Intersect sets the object on the intersection
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].objhit is s
    assert xs[1].objhit is s


def test_hit1():
    # The hit, when all intersections have positive t
    s = objects.Sphere()
    i1 = objects.Intersection(s, 1)
    i2 = objects.Intersection(s, 2)
    xs = [i1, i2]
    assert objects.hit(xs) is i1


def test_hit2():
    # The hit, when some intersections have negative t
    s = objects.Sphere()
    i1 = objects.Intersection(s, -1)
    i2 = objects.Intersection(s, 1)
    xs = [i1, i2]
    assert objects.hit(xs) is i2


def test_hit3():
    # The hit, when all intersections have negative t
    s = objects.Sphere()
    i1 = objects.Intersection(s, -2)
    i2 = objects.Intersection(s, -1)
    xs = [i1, i2]
    assert objects.hit(xs) is None


def test_hit4():
    # The hit is always the lowest nonnegative intersection
    s = objects.Sphere()
    i1 = objects.Intersection(s, 5)
    i2 = objects.Intersection(s, 7)
    i3 = objects.Intersection(s, -3)
    i4 = objects.Intersection(s, 2)
    xs = [i1, i2, i3, i4]
    assert objects.hit(xs) is i4


def test_raytransform1():
    # Translating a ray
    r = tuple.Ray(tuple.Point(1, 2, 3), tuple.Vector(0, 1, 0))
    m = transformations.translation(3, 4, 5)
    r2 = transformations.transformray(m, r)
    assert r2.origin == tuple.Point(4, 6, 8)
    assert r2.direction == tuple.Vector(0, 1, 0)


def test_raytransform2():
    # Scaling a ray
    r = tuple.Ray(tuple.Point(1, 2, 3), tuple.Vector(0, 1, 0))
    m = transformations.scaling(2, 3, 4)
    r2 = transformations.transformray(m, r)
    assert r2.origin == tuple.Point(2, 6, 12)
    assert r2.direction == tuple.Vector(0, 3, 0)


def test_spheretransform1():
    # A sphere's default transformation
    s = objects.Sphere()
    assert np.allclose(s.transform, np.identity(4))


def test_spheretransform2():
    # Changing a sphere's transformation
    t = transformations.translation(2, 3, 4)
    s = objects.Sphere(t)
    assert np.allclose(s.transform, t)


def test_sphereintersect6():
    # Intersecting a scaled sphere with a ray
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    t = transformations.scaling(2, 2, 2)
    s = objects.Sphere(t)
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 3.0)
    assert math.isclose(xs[1].t, 7.0)


def test_sphereintersect7():
    # Intersecting a translated sphere with a ray
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    t = transformations.translation(5, 0, 0)
    s = objects.Sphere(t)
    xs = s.intersect(r)
    assert len(xs) == 0


def test_normalat1():
    # The normal on a sphere at a point on the x axis
    s = objects.Sphere()
    n = s.normal_at(tuple.Point(1, 0, 0))
    assert n == tuple.Vector(1, 0, 0)


def test_normalat2():
    # The normal on a sphere at a point on the y axis
    s = objects.Sphere()
    n = s.normal_at(tuple.Point(0, 1, 0))
    assert n == tuple.Vector(0, 1, 0)


def test_normalat3():
    # The normal on a sphere at a point on the z axis
    s = objects.Sphere()
    n = s.normal_at(tuple.Point(0, 0, 1))
    assert n == tuple.Vector(0, 0, 1)


def test_normalat4():
    # The normal on a sphere at a nonaxial point
    s = objects.Sphere()
    rt3over3 = math.sqrt(3) / 3.0
    n = s.normal_at(tuple.Point(rt3over3, rt3over3, rt3over3))
    assert n == tuple.Vector(rt3over3, rt3over3, rt3over3)


def test_normalat5():
    # Computing the normal on a translated sphere
    s = objects.Sphere(transformations.translation(0, 1, 0))
    n = s.normal_at(tuple.Point(0, 1.70711, -0.70711))
    assert n == tuple.Vector(0, 0.70711, -0.70711)


def test_normalat6():
    # Computing the normal on a transformed sphere
    m = np.matmul(transformations.scaling(1, 0.5, 1), transformations.rotation_z(math.pi/5))
    s = objects.Sphere(m)
    n = s.normal_at(tuple.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
    assert n == tuple.Vector(0, 0.97014, -0.24254)


def test_reflect1():
    # Reflecting a vector approaching at 45 degrees
    v = tuple.Vector(1, -1, 0)
    n = tuple.Vector(0, 1, 0)
    assert tuple.reflect(v, n) == tuple.Vector(1, 1, 0)


def test_reflect2():
    # Reflecting a vector off a slanted surface
    v = tuple.Vector(0, -1, 0)
    n = tuple.Vector(math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert tuple.reflect(v, n) == tuple.Vector(1, 0, 0)


def test_light1():
    # A point light has a position and intensity
    intensity = tuple.Color(1, 1, 1)
    position = tuple.Point(0, 0, 0)
    light = lights.PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity


def test_material1():
    # The default material
    m = materials.Material()
    assert m.color == tuple.Color(1, 1, 1)
    assert math.isclose(m.ambient, 0.1)
    assert math.isclose(m.diffuse, 0.9)
    assert math.isclose(m.specular, 0.9)
    assert math.isclose(m.shininess, 200.0)


def test_spherematerial1():
    # A sphere has a default material
    s = objects.Sphere()
    m = s.material
    assert m == materials.Material()


def test_spherematerial2():
    # A sphere may be assigned a material
    s = objects.Sphere()
    m = materials.Material()
    m.ambient = 1.0
    s.material = m
    assert s.material is m


def test_lighting1():
    # Lighting with the eye between the light and the surface
    m = materials.Material()
    position = tuple.Point(0, 0, 0)
    eyev = tuple.Vector(0, 0, -1)
    normalv = tuple.Vector(0, 0, -1)
    light = lights.PointLight(tuple.Point(0, 0, -10), tuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == tuple.Color(1.9, 1.9, 1.9)


def test_lighting2():
    # Lighting with the eye between light and surface, eye offset 45 degrees
    m = materials.Material()
    position = tuple.Point(0, 0, 0)
    eyev = tuple.Vector(0, math.sqrt(2)/2, -math.sqrt(2)/2)
    normalv = tuple.Vector(0, 0, -1)
    light = lights.PointLight(tuple.Point(0, 0, -10), tuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == tuple.Color(1.0, 1.0, 1.0)


def test_lighting3():
    # Lighting with eye opposite surface, light offset 45 degrees
    m = materials.Material()
    position = tuple.Point(0, 0, 0)
    eyev = tuple.Vector(0, 0, -1)
    normalv = tuple.Vector(0, 0, -1)
    light = lights.PointLight(tuple.Point(0, 10, -10), tuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == tuple.Color(0.7364, 0.7364, 0.7364)


def test_lighting4():
    # Lighting with eye in the path of the reflection vector
    m = materials.Material()
    position = tuple.Point(0, 0, 0)
    eyev = tuple.Vector(0, -math.sqrt(2) / 2, -math.sqrt(2) / 2)
    normalv = tuple.Vector(0, 0, -1)
    light = lights.PointLight(tuple.Point(0, 10, -10), tuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == tuple.Color(1.6364, 1.6364, 1.6364)


def test_lighting5():
    # Lighting with the light behind the surface
    m = materials.Material()
    position = tuple.Point(0, 0, 0)
    eyev = tuple.Vector(0, 0, -1)
    normalv = tuple.Vector(0, 0, -1)
    light = lights.PointLight(tuple.Point(0, 0, 10), tuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == tuple.Color(0.1, 0.1, 0.1)


def test_lighting6():
    # Lighting with the surface in shadow
    m = materials.Material()
    position = tuple.Point(0, 0, 0)
    eyev = tuple.Vector(0, 0, -1)
    normalv = tuple.Vector(0, 0, -1)
    light = lights.PointLight(tuple.Point(0, 0, -10), tuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv, True) == tuple.Color(0.1, 0.1, 0.1)


def test_world1():
    # Creating a world
    w = world.World()
    assert len(w.objects) == 0
    assert len(w.lights) == 0


def test_world2():
    # The default world
    w = world.default_world()
    assert len(w.objects) == 2
    assert len(w.lights) == 1
    assert w.objects[0].material.color == tuple.Color(0.8, 1.0, 0.6)
    assert math.isclose(w.objects[0].material.ambient, 0.1)
    assert math.isclose(w.objects[0].material.diffuse, 0.7)
    assert math.isclose(w.objects[0].material.specular, 0.2)
    assert math.isclose(w.objects[0].material.shininess, 200.0)
    assert isinstance(w.objects[0], objects.Sphere)
    assert np.allclose(w.objects[1].transform, transformations.scaling(0.5, 0.5, 0.5))
    assert isinstance(w.objects[1], objects.Sphere)
    assert isinstance(w.lights[0], lights.Light)
    assert w.lights[0].position == tuple.Point(-10, 10, -10)
    assert w.lights[0].intensity == tuple.Color(1, 1, 1)


def test_world3():
    # Intersect a world with a ray
    w = world.default_world()
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    xs = w.intersect(r)
    assert len(xs) == 4
    assert math.isclose(xs[0].t, 4)
    assert math.isclose(xs[1].t, 4.5)
    assert math.isclose(xs[2].t, 5.5)
    assert math.isclose(xs[3].t, 6)


def test_hitrecord1():
    # Precomputing the state of an intersection
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    i = objects.Intersection(s, 4)
    comps = world.prepare_computations(i, r)
    assert math.isclose(comps.t, i.t)
    assert comps.objhit is i.objhit
    assert comps.point == tuple.Point(0, 0, -1)
    assert comps.eyev == tuple.Vector(0, 0, -1)
    assert comps.normalv == tuple.Vector(0, 0, -1)
    assert not comps.inside


def test_hitrecord2():
    # The hit, when an intersection occurs on the inside
    r = tuple.Ray(tuple.Point(0, 0, 0), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    i = objects.Intersection(s, 1)
    comps = world.prepare_computations(i, r)
    assert comps.point == tuple.Point(0, 0, 1)
    assert comps.eyev == tuple.Vector(0, 0, -1)
    assert comps.inside
    assert comps.normalv == tuple.Vector(0, 0, -1)


def test_hitrecord3():
    # The hit should offset the point
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    s = objects.Sphere()
    s.transform = transformations.translation(0, 0, 1)
    i = objects.Intersection(s, 5)
    comps = world.prepare_computations(i, r)
    assert comps.over_point.z < -objects.EPSILON/2
    assert comps.point.z > comps.over_point.z


def test_shadehit1():
    # Shading an intersection
    w = world.default_world()
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    s = w.objects[0]
    i = objects.Intersection(s, 4)
    hitrecord = world.prepare_computations(i, r)
    c = w.shade_hit(hitrecord)
    assert c == tuple.Color(0.38066, 0.47583, 0.2855)


def test_shadehit2():
    # shading an intersection from the inside
    w = world.default_world()
    light = lights.PointLight(tuple.Point(0, 0.25, 0), tuple.Color(1, 1, 1))
    w.lights = [light]
    r = tuple.Ray(tuple.Point(0, 0, 0), tuple.Vector(0, 0, 1))
    s = w.objects[1]
    i = objects.Intersection(s, 0.5)
    hitrecord = world.prepare_computations(i, r)
    c = w.shade_hit(hitrecord)
    assert c == tuple.Color(0.90498, 0.90498, 0.90498)


def test_colorat1():
    # The color when a ray misses
    w = world.default_world()
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 1, 0))
    c = w.color_at(r)
    assert c == tuple.Color(0, 0, 0)


def test_colorat2():
    # The color when a ray hits
    w = world.default_world()
    r = tuple.Ray(tuple.Point(0, 0, -5), tuple.Vector(0, 0, 1))
    c = w.color_at(r)
    assert c == tuple.Color(0.38066, 0.47583, 0.2855)


def test_colorat3():
    # The color with an intersection behind the ray
    w = world.default_world()
    outer = w.objects[0]
    outer.material.ambient = 1.0
    inner = w.objects[1]
    inner.material.ambient = 1.0
    r = tuple.Ray(tuple.Point(0, 0, 0.75), tuple.Vector(0, 0, -1))
    c = w.color_at(r)
    assert c == inner.material.color


def test_viewtransform1():
    # The transformation matrix for the default orientation
    from_pt = tuple.Point(0, 0, 0)
    to_pt = tuple.Point(0, 0, -1)
    up_vec = tuple.Vector(0, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    assert np.allclose(t, np.identity(4))


def test_viewtransform2():
    # A view transformation matrix looking in positive z direction
    from_pt = tuple.Point(0, 0, 0)
    to_pt = tuple.Point(0, 0, 1)
    up_vec = tuple.Vector(0, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    assert np.allclose(t, transformations.scaling(-1, 1, -1))


def test_viewtransform3():
    # The view transformation moves the world
    from_pt = tuple.Point(0, 0, 8)
    to_pt = tuple.Point(0, 0, 1)
    up_vec = tuple.Vector(0, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    assert np.allclose(t, transformations.translation(0, 0, -8))


def test_viewtransformation4():
    # An arbitrary view transformation
    from_pt = tuple.Point(1, 3, 2)
    to_pt = tuple.Point(4, -2, 8)
    up_vec = tuple.Vector(1, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    res = np.array([[-0.50709, 0.50709, 0.67612, -2.36643],
                    [0.76772, 0.60609, 0.12122, -2.82843],
                    [-0.35857, 0.59761, -0.71714, 0],
                    [0, 0, 0, 1]])
    assert np.allclose(t, res, 1e-05, 1e-05)


def test_camera1():
    # Constructing a camera
    c = canvas.Camera(160, 120, math.pi/2)
    assert c.hsize == 160
    assert c.vsize == 120
    assert math.isclose(c.field_of_view, math.pi/2)
    assert np.allclose(c.transform, np.identity(4))


def test_camera2():
    # The pixel size for a horizontal canvas
    c = canvas.Camera(200, 125, math.pi/2)
    assert math.isclose(c.pixel_size, 0.01)


def test_camera3():
    # The pixel size for a vertical canvas
    c = canvas.Camera(125, 200, math.pi/2)
    assert math.isclose(c.pixel_size, 0.01)


def test_camera4():
    # Constructing a ray through the center of the camera
    c = canvas.Camera(201, 101, math.pi/2)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == tuple.Point(0, 0, 0)
    assert r.direction == tuple.Vector(0, 0, -1)


def test_camera5():
    # Constructing a ray through the corner of the canvas
    c = canvas.Camera(201, 101, math.pi/2)
    r = c.ray_for_pixel(0, 0)
    assert r.origin == tuple.Point(0, 0, 0)
    assert r.direction == tuple.Vector(0.66519, 0.33259, -0.66851)


def test_camera6():
    # Constructing a ray when the camera is transformed
    trans = np.matmul(transformations.rotation_y(math.pi/4), transformations.translation(0, -2, 5))
    c = canvas.Camera(201, 101, math.pi/2, trans)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == tuple.Point(0, 2, -5)
    assert r.direction == tuple.Vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2)


def test_render1():
    w = world.default_world()
    c = canvas.Camera(11, 11, math.pi/2)
    fr = tuple.Point(0, 0, -5)
    to = tuple.Point(0, 0, 0)
    up = tuple.Vector(0, 1, 0)
    c.transform = transformations.view_transform(fr, to, up)
    canvas.render(c, w)
    assert canvas.pixel_at(5, 5) == tuple.Color(0.38066, 0.47583, 0.2855)


def test_shadowed1():
    # There is no shadow when nothing is collinear with point and light
    w = world.default_world()
    p = tuple.Point(0, 10, 0)
    assert not w.is_shadowed(p)


def test_shadowed2():
    # There is no shadow when an object is between the point and the light
    w = world.default_world()
    p = tuple.Point(10, -10, 10)
    assert w.is_shadowed(p)


def test_shadowed3():
    # There is no shadow when an object is behind the light
    w = world.default_world()
    p = tuple.Point(-20, 20, -20)
    assert not w.is_shadowed(p)


def test_shadowed4():
    # There is no shadow when an object is behind the point
    w = world.default_world()
    p = tuple.Point(-2, 2, -2)
    assert not w.is_shadowed(p)
