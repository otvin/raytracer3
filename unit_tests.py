import tuple
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
