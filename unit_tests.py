import raytracer3 as rt
import math
import time

def test_point1():
    # A tuple with w=1.0 is a point
    t = rt.RT_Tuple(4.3, -4.2, 3.1, 1.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert t.ispoint()
    assert not t.isvector()


def test_vector1():
    # A tuple with w=0 is a vector
    t = rt.RT_Tuple(4.3, -4.2, 3.1, 0.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert not t.ispoint()
    assert t.isvector()


def test_point2():
    # Point() creates tuples with w=1
    p = rt.Point(4.0, -4.0, 3.0)
    assert isinstance(p, rt.RT_Tuple)
    assert p == rt.RT_Tuple(4.0, -4.0, 3.0, 1.0)


def test_vector2():
    # Vector() creates tuples with w=0
    p = rt.Vector(4, -4, 3)
    assert isinstance(p, rt.RT_Tuple)
    assert p == rt.RT_Tuple(4.0, -4.0, 3.0, 0.0)


def test_add1():
    # Adding two tuples
    p1 = rt.RT_Tuple(3, -2, 5, 1)
    p2 = rt.RT_Tuple(-2, 3, 1, 0)
    assert p1 + p2 == rt.RT_Tuple(1, 1, 6, 1)


def test_sub1():
    # Subtracting two points
    p1 = rt.Point(3, 2, 1)
    p2 = rt.Point(5, 6, 7)
    assert p1 - p2 == rt.Vector(-2, -4, -6)


def test_sub2():
    # Subtracting a vector from a point
    p = rt.Point(3, 2, 1)
    v = rt.Vector(5, 6, 7)
    assert p - v == rt.Point(-2, -4, -6)


def test_sub3():
    # Subtracting two vectors
    v1 = rt.Vector(3, 2, 1)
    v2 = rt.Vector(5, 6, 7)
    assert v1 - v2 == rt.Vector(-2, -4, -6)


def test_negation1():
    # Subtracting a vector from the zero vector
    zero = rt.Vector(0, 0, 0)
    v = rt.Vector(1, -2, 3)
    assert zero - v == rt.Vector(-1, 2, -3)


def test_negation2():
    # Negating a tuple
    a = rt.RT_Tuple(1, -2, 3, -4)
    assert -a == rt.RT_Tuple(-1, 2, -3, 4)


def test_scalarmult1():
    # Multiplying a tuple by a scalar
    a = rt.RT_Tuple(1, -2, 3, -4)
    assert a * 3.5 == rt.RT_Tuple(3.5, -7, 10.5, -14)


def run_tests():
    test_point1()
    test_vector1()
    test_point2()
    test_vector2()
    test_add1()
    test_sub1()
    test_sub2()
    test_sub3()
    test_negation1()
    test_negation2()
    test_scalarmult1()

if __name__ == '__main__':
    run_tests()
    print('Success!')