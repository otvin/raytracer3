import raytracer3 as rt
import math

def test_point1():
    t = rt.RT_Tuple(4.3, -4.2, 3.1, 1.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert t.ispoint()
    assert not t.isvector()


def test_vector1():
    t = rt.RT_Tuple(4.3, -4.2, 3.1, 0.0)
    assert math.isclose(t.x, 4.3)
    assert math.isclose(t.y, -4.2)
    assert math.isclose(t.z, 3.1)
    assert not t.ispoint()
    assert t.isvector()


def test_point2():
    p = rt.Point(4.0, -4.0, 3.0)
    assert isinstance(p, rt.RT_Tuple)
    assert p == rt.RT_Tuple(4.0, -4.0, 3.0, 1.0)


def test_vector2():
    p = rt.Vector(4, -4, 3)
    assert isinstance(p, rt.RT_Tuple)
    assert p == rt.RT_Tuple(4.0, -4.0, 3.0, 0.0)


def run_tests():
    test_point1()
    test_vector1()
    test_point2()
    test_vector2()


if __name__ == '__main__':
    run_tests()
    print('Success!')