import math
import rttuple
import canvas
import transformations
import objects
import lights
import materials
import world
import matrices


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
    t = rttuple.RT_Tuple(4.3, -4.2, 3.1, 1.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert t.ispoint()
    assert not t.isvector()


def test_vector1():
    # A tuple with w=0 is a vector
    t = rttuple.RT_Tuple(4.3, -4.2, 3.1, 0.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert not t.ispoint()
    assert t.isvector()


def test_point2():
    # Point() creates tuples with w=1
    p = rttuple.Point(4.0, -4.0, 3.0)
    assert isinstance(p, rttuple.RT_Tuple)
    assert p == rttuple.RT_Tuple(4.0, -4.0, 3.0, 1.0)


def test_vector2():
    # Vector() creates tuples with w=0
    p = rttuple.Vector(4, -4, 3)
    assert isinstance(p, rttuple.RT_Tuple)
    assert p == rttuple.RT_Tuple(4.0, -4.0, 3.0, 0.0)


def test_add1():
    # Adding two tuples
    p1 = rttuple.RT_Tuple(3, -2, 5, 1)
    p2 = rttuple.RT_Tuple(-2, 3, 1, 0)
    assert p1 + p2 == rttuple.RT_Tuple(1, 1, 6, 1)


def test_sub1():
    # Subtracting two points
    p1 = rttuple.Point(3, 2, 1)
    p2 = rttuple.Point(5, 6, 7)
    assert p1 - p2 == rttuple.Vector(-2, -4, -6)


def test_sub2():
    # Subtracting a vector from a point
    p = rttuple.Point(3, 2, 1)
    v = rttuple.Vector(5, 6, 7)
    assert p - v == rttuple.Point(-2, -4, -6)


def test_sub3():
    # Subtracting two vectors
    v1 = rttuple.Vector(3, 2, 1)
    v2 = rttuple.Vector(5, 6, 7)
    assert v1 - v2 == rttuple.Vector(-2, -4, -6)


def test_negation1():
    # Subtracting a vector from the zero vector
    zero = rttuple.Vector(0, 0, 0)
    v = rttuple.Vector(1, -2, 3)
    assert zero - v == rttuple.Vector(-1, 2, -3)


def test_negation2():
    # Negating a tuple
    a = rttuple.RT_Tuple(1, -2, 3, -4)
    assert -a == rttuple.RT_Tuple(-1, 2, -3, 4)


def test_scalarmult1():
    # Multiplying a tuple by a scalar
    a = rttuple.RT_Tuple(1, -2, 3, -4)
    assert a * 3.5 == rttuple.RT_Tuple(3.5, -7, 10.5, -14)


def test_scalarmult2():
    # Multiplying a tuple by a fraction
    a = rttuple.RT_Tuple(1, -2, 3, -4)
    assert a * 0.5 == rttuple.RT_Tuple(0.5, -1, 1.5, -2)


def test_tuplemult1():
    # Multiplying a tuple by a tuple
    a = rttuple.RT_Tuple(2, 3, 4, 5)
    b = rttuple.RT_Tuple(0.5, 4, -1.2, 1.5)
    assert a * b == rttuple.RT_Tuple(1, 12, -4.8, 7.5)


def test_scalardiv1():
    # Dividing a tuple by a scalar
    a = rttuple.RT_Tuple(1, -2, 3, -4)
    assert a / 2 == rttuple.RT_Tuple(0.5, -1, 1.5, -2)


def test_tuplediv1():
    # Dividing a tuple by a tuple
    a = rttuple.RT_Tuple(3, 4, 5, 6)
    b = rttuple.RT_Tuple(1, 2, -2.5, 4)
    assert a / b == rttuple.RT_Tuple(3, 2, -2, 1.5)


def test_magnitude1():
    # Computing the magnitude of vector (1,0,0)
    v = rttuple.Vector(1, 0, 0)
    assert v.magnitude() == 1


def test_magnitude2():
    # Computing the magnitude of vector (0,1,0)
    v = rttuple.Vector(0, 1, 0)
    assert v.magnitude() == 1


def test_magnitude3():
    # Computing the magnitude of vector (0,0,1)
    v = rttuple.Vector(0, 0, 1)
    assert v.magnitude() == 1


def test_magnitude4():
    # Computing the magnitude of vector (1,2,3)
    v = rttuple.Vector(1, 2, 3)
    assert v.magnitude() == math.sqrt(14)


def test_magnitude5():
    # Computing the magnitude of vector (-1, -2, -3)
    v = rttuple.Vector(-1, -2, -3)
    assert v.magnitude() == math.sqrt(14)


def test_normalize1():
    # Normalizing vector (4,0,0) gives (1,0,0)
    v = rttuple.Vector(4, 0, 0)
    assert rttuple.normalize(v) == rttuple.Vector(1, 0, 0)


def test_normalize2():
    # Normalizing vector (1, 2, 3)
    v = rttuple.Vector(1, 2, 3)
    assert rttuple.normalize(v) == rttuple.Vector(0.26726, 0.53452, 0.80178)


def test_dot1():
    # The dot product of two tuples
    a = rttuple.RT_Tuple(1, 2, 3)
    b = rttuple.RT_Tuple(2, 3, 4)
    assert rttuple.dot(a, b) == 20


def test_cross1():
    # The cross product of two vectors
    a = rttuple.Vector(1, 2, 3)
    b = rttuple.Vector(2, 3, 4)
    assert rttuple.cross(a, b) == rttuple.Vector(-1, 2, -1)
    assert rttuple.cross(b, a) == rttuple.Vector(1, -2, 1)


def test_color1():
    # Adding colors
    c1 = rttuple.Color(0.9, 0.6, 0.75)
    c2 = rttuple.Color(0.7, 0.1, 0.25)
    assert c1 + c2 == rttuple.Color(1.6, 0.7, 1.0)


def test_color2():
    # Subtracting colors
    c1 = rttuple.Color(0.9, 0.6, 0.75)
    c2 = rttuple.Color(0.7, 0.1, 0.25)
    assert c1 - c2 == rttuple.Color(0.2, 0.5, 0.5)


def test_color3():
    # Multiplying a color by a scalar
    c = rttuple.Color(0.2, 0.3, 0.4)
    assert c * 2 == rttuple.Color(0.4, 0.6, 0.8)


def test_color4():
    # Mutiplying colors
    c1 = rttuple.Color(1, 0.2, 0.4)
    c2 = rttuple.Color(0.9, 1, 0.1)
    assert c1 * c2 == rttuple.Color(0.9, 0.2, 0.04)


def test_canvas1():
    # Creating a canvas
    canvas.init_canvas(10, 20)
    assert canvas.CANVASWIDTH == 10
    assert canvas.CANVASHEIGHT == 20
    black = rttuple.Color(0, 0, 0)
    for w in range(10):
        for h in range(20):
            assert canvas.pixel_at(w, h) == black


def test_canvas2():
    # Writing pixels to a canvas
    canvas.init_canvas(10, 20)
    red = rttuple.Color(1, 0, 0)
    canvas.write_pixel(2, 3, red)
    assert canvas.pixel_at(2, 3) == red


def test_canvas3():
    # This is the final exercise from chapter 2; will test the ppm generated against a "good" ppm.
    # Note I use different variables, etc, but still get the parabola.
    canvas.init_canvas(900, 550)
    gravity = rttuple.Vector(0, -0.1, 0)
    wind = rttuple.Vector(-0.01, 0, 0)
    velocity = rttuple.normalize(rttuple.Vector(1, 1.8, 0)) * 11.25
    red = rttuple.Color(1, 0, 0)
    position = rttuple.Point(0, 1, 0)

    while 0 <= position.x <= 900 and 0 <= position.y <= 550:
        canvas.write_pixel(int(position.x), int(position.y), red)
        position += velocity
        velocity = velocity + (gravity + wind)  # parens stop Pycharm from complaining about wrong type for gravity.

    canvas.canvas_to_ppm('test_canvas3.ppm')
    compare_ppms('test_canvas3.ppm', 'test_canvas3_success.ppm')


def test_matrix1():
    # A matrix mutliplied by a tuple
    A = [[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]]
    b = rttuple.RT_Tuple(1, 2, 3, 1)
    assert matrices.matmul4xTuple(A, b) == rttuple.RT_Tuple(18, 24, 33, 1)


def test_matrices():
    # Replaced numpy as straight Python was faster

    A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    B = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    assert matrices.allclose4x4(A, B)

    A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    B = [[2, 3, 4, 5], [6, 7, 8, 9], [8, 7, 6, 5], [4, 3, 2, 1]]
    assert (not matrices.allclose4x4(A, B))

    A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]]
    B = [[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]]
    res = [[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]]
    assert matrices.allclose4x4(matrices.matmul4x4(A, B), res)

    A = [[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]]
    assert matrices.allclose4x4(matrices.matmul4x4(A, matrices.identity4()), A)

    A = [[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]]
    AT = [[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]]
    assert matrices.allclose4x4(matrices.transpose4x4(A), AT)

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
    B = matrices.inverse4x4(A)
    assert matrices.allclose4x4(B, res)
    assert math.isclose(B[3][2], -160.0/532.0)
    assert math.isclose(B[2][3], 105.0/532.0)
    assert matrices.allclose4x4(matrices.matmul4x4(A, B), matrices.identity4())

    A = [[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]]
    B = [[8, 2, 2, 2], [3, -1, 7, 0], [7, 0, 5, 4], [6, -2, 0, 5]]
    C = matrices.matmul4x4(A, B)
    assert matrices.allclose4x4(matrices.matmul4x4(C, matrices.inverse4x4(B)), A)


def test_translation1():
    # Multiplying by a translation matrix
    trans = transformations.translation(5, -3, 2)
    p = rttuple.Point(-3, 4, 5)
    assert transformations.transform(trans, p) == rttuple.Point(2, 1, 7)


def test_translation2():
    # Multiplying by the inverse of a translation matrix
    trans = transformations.translation(5, -3, 2)
    inv = matrices.inverse4x4(trans)
    p = rttuple.Point(-3, 4, 5)
    assert transformations.transform(inv, p) == rttuple.Point(-8, 7, 3)


def test_translation3():
    # Translation does not affect vectors
    trans = transformations.translation(5, -3, 2)
    v = rttuple.Vector(-3, 4, 5)
    assert transformations.transform(trans, v) == v


def test_scaling1():
    # A scaling matrix applied to a point
    trans = transformations.scaling(2, 3, 4)
    p = rttuple.Point(-4, 6, 8)
    assert transformations.transform(trans, p) == rttuple.Point(-8, 18, 32)


def test_scaling2():
    # A scaling matrix applied to a vector
    trans = transformations.scaling(2, 3, 4)
    v = rttuple.Vector(-4, 6, 8)
    assert transformations.transform(trans, v) == rttuple.Vector(-8, 18, 32)


def test_scaling3():
    # Multiplying by the inverse of a scaling matrix
    trans = transformations.scaling(2, 3, 4)
    inv = matrices.inverse4x4(trans)
    v = rttuple.Vector(-4, 6, 8)
    assert transformations.transform(inv, v) == rttuple.Vector(-2, 2, 2)


def test_reflection1():
    # Reflection is scaling by a negative value
    trans = transformations.reflection(True, False, False)
    p = rttuple.Point(2, 3, 4)
    assert transformations.transform(trans, p) == rttuple.Point(-2, 3, 4)


def test_rotation1():
    # Rotating a point around the x axis
    p = rttuple.Point(0, 1, 0)
    half_quarter = transformations.rotation_x(math.pi / 4)
    full_quarter = transformations.rotation_x(math.pi / 2)
    assert transformations.transform(half_quarter, p) == rttuple.Point(0, math.sqrt(2)/2, math.sqrt(2)/2)
    assert transformations.transform(full_quarter, p) == rttuple.Point(0, 0, 1)


def test_rotation2():
    # The inverse of a rotation rotates in the opposite direction
    p = rttuple.Point(0, 1, 0)
    half_quarter = transformations.rotation_x(math.pi / 4)
    inv = matrices.inverse4x4(half_quarter)
    assert transformations.transform(inv, p) == rttuple.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2)


def test_rotation3():
    # Rotating a point around the y axis
    p = rttuple.Point(0, 0, 1)
    half_quarter = transformations.rotation_y(math.pi / 4)
    full_quarter = transformations.rotation_y(math.pi / 2)
    assert transformations.transform(half_quarter, p) == rttuple.Point(math.sqrt(2)/2, 0, math.sqrt(2)/2)
    assert transformations.transform(full_quarter, p) == rttuple.Point(1, 0, 0)


def test_rotation4():
    # Rotating a point around the z axis
    p = rttuple.Point(0, 1, 0)
    half_quarter = transformations.rotation_z(math.pi / 4)
    full_quarter = transformations.rotation_z(math.pi / 2)
    assert transformations.transform(half_quarter, p) == rttuple.Point(-math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert transformations.transform(full_quarter, p) == rttuple.Point(-1, 0, 0)


def test_skew1():
    # A shearing transformation moves x in proportion to y
    trans = transformations.skew(1, 0, 0, 0, 0, 0)
    p = rttuple.Point(2, 3, 4)
    assert transformations.transform(trans, p) == rttuple.Point(5, 3, 4)


def test_skew2():
    # Several other shearing transformations
    p = rttuple.Point(2, 3, 4)
    trans1 = transformations.skew(0, 1, 0, 0, 0, 0)
    trans2 = transformations.skew(0, 0, 1, 0, 0, 0)
    trans3 = transformations.skew(0, 0, 0, 1, 0, 0)
    trans4 = transformations.skew(0, 0, 0, 0, 1, 0)
    trans5 = transformations.skew(0, 0, 0, 0, 0, 1)
    assert transformations.transform(trans1, p) == rttuple.Point(6, 3, 4)
    assert transformations.transform(trans2, p) == rttuple.Point(2, 5, 4)
    assert transformations.transform(trans3, p) == rttuple.Point(2, 7, 4)
    assert transformations.transform(trans4, p) == rttuple.Point(2, 3, 6)
    assert transformations.transform(trans5, p) == rttuple.Point(2, 3, 7)


def test_transformchain1():
    # Individual transformations are applied in sequence
    p = rttuple.Point(1, 0, 1)
    A = transformations.rotation_x(math.pi / 2)
    B = transformations.scaling(5, 5, 5)
    C = transformations.translation(10, 5, 7)
    p2 = transformations.transform(A, p)
    assert p2 == rttuple.Point(1, -1, 0)
    p3 = transformations.transform(B, p2)
    assert p3 == rttuple.Point(5, -5, 0)
    p4 = transformations.transform(C, p3)
    assert p4 == rttuple.Point(15, 0, 7)


def test_transformchain2():
    # CHained transformations must be applied in reverse order
    p = rttuple.Point(1, 0, 1)
    A = transformations.rotation_x(math.pi / 2)
    B = transformations.scaling(5, 5, 5)
    C = transformations.translation(10, 5, 7)
    T = matrices.matmul4x4(matrices.matmul4x4(C, B), A)
    assert transformations.transform(T, p) == rttuple.Point(15, 0, 7)


def test_transformchain3():
    # This is the final exercise from chapter 4.
    halfcanvas = 12
    canvas.init_canvas(2 * halfcanvas, 2 * halfcanvas)
    clockradius = int(0.75 * halfcanvas)
    trans = transformations.rotation_y(math.pi / 6)

    gold = rttuple.Color(1, 0.84314, 0)
    p = rttuple.RT_Tuple(0, 0, 1)  # start at 12 o'clock
    for i in range(13):
        dot = p * clockradius
        canvas.write_pixel(int(dot.x) + halfcanvas, int(dot.z) + halfcanvas, gold)
        p = transformations.transform(trans, p)

    canvas.canvas_to_ppm('test_transformchain3.ppm')
    compare_ppms('test_transformchain3.ppm', 'test_transformchain3_success.ppm')


def test_ray1():
    # Creating and querying a ray
    origin = rttuple.Point(1, 2, 3)
    direction = rttuple.Vector(4, 5, 6)
    r = rttuple.Ray(origin, direction)
    assert r.origin == origin
    assert r.direction == direction


def test_ray2():
    # Computing a point from a distance
    r = rttuple.Ray(rttuple.Point(2, 3, 4), rttuple.Vector(1, 0, 0))
    assert r.at(0) == rttuple.Point(2, 3, 4)
    assert r.at(1) == rttuple.Point(3, 3, 4)
    assert r.at(-1) == rttuple.Point(1, 3, 4)
    assert r.at(2.5) == rttuple.Point(4.5, 3, 4)


def test_sphereintersect1():
    # A ray intersects a sphere at two points
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 4.0)
    assert math.isclose(xs[1].t, 6.0)


def test_sphereintersect2():
    # A ray intersects a sphere at a tangent
    r = rttuple.Ray(rttuple.Point(0, 1, -5), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 5.0)
    assert math.isclose(xs[1].t, 5.0)


def test_sphereintersect3():
    # A ray misses a sphere
    r = rttuple.Ray(rttuple.Point(0, 2, -5), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 0


def test_sphereintersect4():
    # A ray originates inside a sphere
    r = rttuple.Ray(rttuple.Point(0, 0, 0), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, -1.0)
    assert math.isclose(xs[1].t, 1.0)


def test_sphereintersect5():
    # A sphere is behind a ray
    r = rttuple.Ray(rttuple.Point(0, 0, 5), rttuple.Vector(0, 0, 1))
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
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    xs = s.intersect(r)
    assert len(xs) == 2
    assert xs[0].objhit is s
    assert xs[1].objhit is s


def test_raytransform1():
    # Translating a ray
    r = rttuple.Ray(rttuple.Point(1, 2, 3), rttuple.Vector(0, 1, 0))
    m = transformations.translation(3, 4, 5)
    r2 = transformations.transformray(m, r)
    assert r2.origin == rttuple.Point(4, 6, 8)
    assert r2.direction == rttuple.Vector(0, 1, 0)


def test_raytransform2():
    # Scaling a ray
    r = rttuple.Ray(rttuple.Point(1, 2, 3), rttuple.Vector(0, 1, 0))
    m = transformations.scaling(2, 3, 4)
    r2 = transformations.transformray(m, r)
    assert r2.origin == rttuple.Point(2, 6, 12)
    assert r2.direction == rttuple.Vector(0, 3, 0)


def test_spheretransform1():
    # A sphere's default transformation
    s = objects.Sphere()
    assert matrices.allclose4x4(s.transform, matrices.identity4())


def test_spheretransform2():
    # Changing a sphere's transformation
    t = transformations.translation(2, 3, 4)
    s = objects.Sphere(t)
    assert matrices.allclose4x4(s.transform, t)


def test_sphereintersect6():
    # Intersecting a scaled sphere with a ray
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    t = transformations.scaling(2, 2, 2)
    s = objects.Sphere(t)
    xs = s.intersect(r)
    assert len(xs) == 2
    assert math.isclose(xs[0].t, 3.0)
    assert math.isclose(xs[1].t, 7.0)


def test_sphereintersect7():
    # Intersecting a translated sphere with a ray
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    t = transformations.translation(5, 0, 0)
    s = objects.Sphere(t)
    xs = s.intersect(r)
    assert len(xs) == 0


def test_normalat1():
    # The normal on a sphere at a point on the x axis
    s = objects.Sphere()
    n = s.normal_at(rttuple.Point(1, 0, 0))
    assert n == rttuple.Vector(1, 0, 0)


def test_normalat2():
    # The normal on a sphere at a point on the y axis
    s = objects.Sphere()
    n = s.normal_at(rttuple.Point(0, 1, 0))
    assert n == rttuple.Vector(0, 1, 0)


def test_normalat3():
    # The normal on a sphere at a point on the z axis
    s = objects.Sphere()
    n = s.normal_at(rttuple.Point(0, 0, 1))
    assert n == rttuple.Vector(0, 0, 1)


def test_normalat4():
    # The normal on a sphere at a nonaxial point
    s = objects.Sphere()
    rt3over3 = math.sqrt(3) / 3.0
    n = s.normal_at(rttuple.Point(rt3over3, rt3over3, rt3over3))
    assert n == rttuple.Vector(rt3over3, rt3over3, rt3over3)


def test_normalat5():
    # Computing the normal on a translated sphere
    s = objects.Sphere(transformations.translation(0, 1, 0))
    n = s.normal_at(rttuple.Point(0, 1.70711, -0.70711))
    assert n == rttuple.Vector(0, 0.70711, -0.70711)


def test_normalat6():
    # Computing the normal on a transformed sphere
    m = matrices.matmul4x4(transformations.scaling(1, 0.5, 1), transformations.rotation_z(math.pi/5))
    s = objects.Sphere(m)
    n = s.normal_at(rttuple.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
    assert n == rttuple.Vector(0, 0.97014, -0.24254)


def test_reflect1():
    # Reflecting a vector approaching at 45 degrees
    v = rttuple.Vector(1, -1, 0)
    n = rttuple.Vector(0, 1, 0)
    assert rttuple.reflect(v, n) == rttuple.Vector(1, 1, 0)


def test_reflect2():
    # Reflecting a vector off a slanted surface
    v = rttuple.Vector(0, -1, 0)
    n = rttuple.Vector(math.sqrt(2)/2, math.sqrt(2)/2, 0)
    assert rttuple.reflect(v, n) == rttuple.Vector(1, 0, 0)


def test_light1():
    # A point light has a position and intensity
    intensity = rttuple.Color(1, 1, 1)
    position = rttuple.Point(0, 0, 0)
    light = lights.PointLight(position, intensity)
    assert light.position == position
    assert light.intensity == intensity


def test_material1():
    # The default material
    m = materials.Material()
    assert m.color == rttuple.Color(1, 1, 1)
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
    position = rttuple.Point(0, 0, 0)
    eyev = rttuple.Vector(0, 0, -1)
    normalv = rttuple.Vector(0, 0, -1)
    light = lights.PointLight(rttuple.Point(0, 0, -10), rttuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == rttuple.Color(1.9, 1.9, 1.9)


def test_lighting2():
    # Lighting with the eye between light and surface, eye offset 45 degrees
    m = materials.Material()
    position = rttuple.Point(0, 0, 0)
    eyev = rttuple.Vector(0, math.sqrt(2)/2, -math.sqrt(2)/2)
    normalv = rttuple.Vector(0, 0, -1)
    light = lights.PointLight(rttuple.Point(0, 0, -10), rttuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == rttuple.Color(1.0, 1.0, 1.0)


def test_lighting3():
    # Lighting with eye opposite surface, light offset 45 degrees
    m = materials.Material()
    position = rttuple.Point(0, 0, 0)
    eyev = rttuple.Vector(0, 0, -1)
    normalv = rttuple.Vector(0, 0, -1)
    light = lights.PointLight(rttuple.Point(0, 10, -10), rttuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == rttuple.Color(0.7364, 0.7364, 0.7364)


def test_lighting4():
    # Lighting with eye in the path of the reflection vector
    m = materials.Material()
    position = rttuple.Point(0, 0, 0)
    eyev = rttuple.Vector(0, -math.sqrt(2) / 2, -math.sqrt(2) / 2)
    normalv = rttuple.Vector(0, 0, -1)
    light = lights.PointLight(rttuple.Point(0, 10, -10), rttuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == rttuple.Color(1.6364, 1.6364, 1.6364)


def test_lighting5():
    # Lighting with the light behind the surface
    m = materials.Material()
    position = rttuple.Point(0, 0, 0)
    eyev = rttuple.Vector(0, 0, -1)
    normalv = rttuple.Vector(0, 0, -1)
    light = lights.PointLight(rttuple.Point(0, 0, 10), rttuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv) == rttuple.Color(0.1, 0.1, 0.1)


def test_lighting6():
    # Lighting with the surface in shadow
    m = materials.Material()
    position = rttuple.Point(0, 0, 0)
    eyev = rttuple.Vector(0, 0, -1)
    normalv = rttuple.Vector(0, 0, -1)
    light = lights.PointLight(rttuple.Point(0, 0, -10), rttuple.Color(1, 1, 1))
    assert lights.lighting(m, light, position, eyev, normalv, True) == rttuple.Color(0.1, 0.1, 0.1)


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
    assert w.objects[0].material.color == rttuple.Color(0.8, 1.0, 0.6)
    assert math.isclose(w.objects[0].material.ambient, 0.1)
    assert math.isclose(w.objects[0].material.diffuse, 0.7)
    assert math.isclose(w.objects[0].material.specular, 0.2)
    assert math.isclose(w.objects[0].material.shininess, 200.0)
    assert isinstance(w.objects[0], objects.Sphere)
    assert matrices.allclose4x4(w.objects[1].transform, transformations.scaling(0.5, 0.5, 0.5))
    assert isinstance(w.objects[1], objects.Sphere)
    assert isinstance(w.lights[0], lights.Light)
    assert w.lights[0].position == rttuple.Point(-10, 10, -10)
    assert w.lights[0].intensity == rttuple.Color(1, 1, 1)


def test_world3():
    # Intersect a world with a ray
    w = world.default_world()
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    xs = w.intersect(r)
    assert len(xs) == 4
    assert math.isclose(xs[0].t, 4)
    assert math.isclose(xs[1].t, 4.5)
    assert math.isclose(xs[2].t, 5.5)
    assert math.isclose(xs[3].t, 6)


def test_hitrecord1():
    # Precomputing the state of an intersection
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    i = objects.Intersection(s, 4)
    comps = world.prepare_computations(i, r)
    assert math.isclose(comps.t, i.t)
    assert comps.objhit is i.objhit
    assert comps.point == rttuple.Point(0, 0, -1)
    assert comps.eyev == rttuple.Vector(0, 0, -1)
    assert comps.normalv == rttuple.Vector(0, 0, -1)
    assert not comps.inside


def test_hitrecord2():
    # The hit, when an intersection occurs on the inside
    r = rttuple.Ray(rttuple.Point(0, 0, 0), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    i = objects.Intersection(s, 1)
    comps = world.prepare_computations(i, r)
    assert comps.point == rttuple.Point(0, 0, 1)
    assert comps.eyev == rttuple.Vector(0, 0, -1)
    assert comps.inside
    assert comps.normalv == rttuple.Vector(0, 0, -1)


def test_hitrecord3():
    # The hit should offset the point
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    s = objects.Sphere()
    s.transform = transformations.translation(0, 0, 1)
    i = objects.Intersection(s, 5)
    comps = world.prepare_computations(i, r)
    assert comps.over_point.z < -objects.EPSILON/2
    assert comps.point.z > comps.over_point.z


def test_shadehit1():
    # Shading an intersection
    w = world.default_world()
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    s = w.objects[0]
    i = objects.Intersection(s, 4)
    hitrecord = world.prepare_computations(i, r)
    c = w.shade_hit(hitrecord)
    assert c == rttuple.Color(0.38066, 0.47583, 0.2855)


def test_shadehit2():
    # shading an intersection from the inside
    w = world.default_world()
    light = lights.PointLight(rttuple.Point(0, 0.25, 0), rttuple.Color(1, 1, 1))
    w.lights = [light]
    r = rttuple.Ray(rttuple.Point(0, 0, 0), rttuple.Vector(0, 0, 1))
    s = w.objects[1]
    i = objects.Intersection(s, 0.5)
    hitrecord = world.prepare_computations(i, r)
    c = w.shade_hit(hitrecord)
    assert c == rttuple.Color(0.90498, 0.90498, 0.90498)


def test_colorat1():
    # The color when a ray misses
    w = world.default_world()
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 1, 0))
    c = w.color_at(r)
    assert c == rttuple.Color(0, 0, 0)


def test_colorat2():
    # The color when a ray hits
    w = world.default_world()
    r = rttuple.Ray(rttuple.Point(0, 0, -5), rttuple.Vector(0, 0, 1))
    c = w.color_at(r)
    assert c == rttuple.Color(0.38066, 0.47583, 0.2855)


def test_colorat3():
    # The color with an intersection behind the ray
    w = world.default_world()
    outer = w.objects[0]
    outer.material.ambient = 1.0
    inner = w.objects[1]
    inner.material.ambient = 1.0
    r = rttuple.Ray(rttuple.Point(0, 0, 0.75), rttuple.Vector(0, 0, -1))
    c = w.color_at(r)
    assert c == inner.material.color


def test_viewtransform1():
    # The transformation matrix for the default orientation
    from_pt = rttuple.Point(0, 0, 0)
    to_pt = rttuple.Point(0, 0, -1)
    up_vec = rttuple.Vector(0, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    assert matrices.allclose4x4(t, matrices.identity4())


def test_viewtransform2():
    # A view transformation matrix looking in positive z direction
    from_pt = rttuple.Point(0, 0, 0)
    to_pt = rttuple.Point(0, 0, 1)
    up_vec = rttuple.Vector(0, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    assert matrices.allclose4x4(t, transformations.scaling(-1, 1, -1))


def test_viewtransform3():
    # The view transformation moves the world
    from_pt = rttuple.Point(0, 0, 8)
    to_pt = rttuple.Point(0, 0, 1)
    up_vec = rttuple.Vector(0, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    assert matrices.allclose4x4(t, transformations.translation(0, 0, -8))


def test_viewtransformation4():
    # An arbitrary view transformation
    from_pt = rttuple.Point(1, 3, 2)
    to_pt = rttuple.Point(4, -2, 8)
    up_vec = rttuple.Vector(1, 1, 0)
    t = transformations.view_transform(from_pt, to_pt, up_vec)
    res = [[-0.50709, 0.50709, 0.67612, -2.36643],
           [0.76772, 0.60609, 0.12122, -2.82843],
           [-0.35857, 0.59761, -0.71714, 0],
           [0, 0, 0, 1]]
    assert matrices.allclose4x4(t, res)


def test_camera1():
    # Constructing a camera
    c = canvas.Camera(160, 120, math.pi/2)
    assert c.hsize == 160
    assert c.vsize == 120
    assert math.isclose(c.field_of_view, math.pi/2)
    assert matrices.allclose4x4(c.transform, matrices.identity4())


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
    assert r.origin == rttuple.Point(0, 0, 0)
    assert r.direction == rttuple.Vector(0, 0, -1)


def test_camera5():
    # Constructing a ray through the corner of the canvas
    c = canvas.Camera(201, 101, math.pi/2)
    r = c.ray_for_pixel(0, 0)
    assert r.origin == rttuple.Point(0, 0, 0)
    assert r.direction == rttuple.Vector(0.66519, 0.33259, -0.66851)


def test_camera6():
    # Constructing a ray when the camera is transformed
    trans = matrices.matmul4x4(transformations.rotation_y(math.pi/4), transformations.translation(0, -2, 5))
    c = canvas.Camera(201, 101, math.pi/2, trans)
    r = c.ray_for_pixel(100, 50)
    assert r.origin == rttuple.Point(0, 2, -5)
    assert r.direction == rttuple.Vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2)


def test_render1():
    w = world.default_world()
    c = canvas.Camera(11, 11, math.pi/2)
    fr = rttuple.Point(0, 0, -5)
    to = rttuple.Point(0, 0, 0)
    up = rttuple.Vector(0, 1, 0)
    c.transform = transformations.view_transform(fr, to, up)
    canvas.mp_render(c, w, 1, 1)
    assert canvas.pixel_at(5, 5) == rttuple.Color(0.38066, 0.47583, 0.2855)


def test_shadowed1():
    # There is no shadow when nothing is collinear with point and light
    w = world.default_world()
    p = rttuple.Point(0, 10, 0)
    assert not w.is_shadowed(p)


def test_shadowed2():
    # There is no shadow when an object is between the point and the light
    w = world.default_world()
    p = rttuple.Point(10, -10, 10)
    assert w.is_shadowed(p)


def test_shadowed3():
    # There is no shadow when an object is behind the light
    w = world.default_world()
    p = rttuple.Point(-20, 20, -20)
    assert not w.is_shadowed(p)


def test_shadowed4():
    # There is no shadow when an object is behind the point
    w = world.default_world()
    p = rttuple.Point(-2, 2, -2)
    assert not w.is_shadowed(p)


def test_plane1():
    # The normal of a plane is constant everywhere
    p = objects.Plane()
    n1 = p.local_normal_at(rttuple.Point(0, 0, 0))
    n2 = p.local_normal_at(rttuple.Point(10, 0, -10))
    n3 = p.local_normal_at(rttuple.Point(-5, 0, 150))
    assert n1 == rttuple.Vector(0, 1, 0)
    assert n2 == rttuple.Vector(0, 1, 0)
    assert n3 == rttuple.Vector(0, 1, 0)


def test_plane2():
    # Intersect with a ray parallel to the plane
    p = objects.Plane()
    r = rttuple.Ray(rttuple.Point(0, 10, 0), rttuple.Vector(0, 0, 1))
    xs = p.local_intersect(r)
    assert len(xs) == 0


def test_plane3():
    # Intersect with a coplanar ray
    p = objects.Plane()
    r = rttuple.Ray(rttuple.Point(0, 0, 0), rttuple.Vector(0, 0, 1))
    xs = p.local_intersect(r)
    assert len(xs) == 0


def test_plane4():
    # A ray intersecting a plane from above
    p = objects.Plane()
    r = rttuple.Ray(rttuple.Point(0, 1, 0), rttuple.Vector(0, -1, 0))
    xs = p.local_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].objhit == p


def test_plane5():
    # A ray intersecting a plane from below
    p = objects.Plane()
    r = rttuple.Ray(rttuple.Point(0, -2, 0), rttuple.Vector(0, 1, 0))
    xs = p.local_intersect(r)
    assert len(xs) == 1
    assert xs[0].t == 2
    assert xs[0].objhit == p
