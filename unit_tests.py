import tuple
import canvas
import math


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

    # now compare the file we wrote here to the good file that is saved locally
    f = open('test_canvas3.ppm', 'r')
    f1 = open('test_canvas3_success.ppm', 'r')

    fline = f.readline()
    f1line = f1.readline()
    linenumber = 1

    while fline != '' or f1line != '':
        assert fline == f1line, "file difference in line {}".format(linenumber)
        fline = f.readline()
        f1line = f1.readline()
        linenumber += 1
