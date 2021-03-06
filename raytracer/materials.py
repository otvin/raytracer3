import math
import raytracer as rt
from .objects import ONEMINUSEPSILON


class Pattern:
    __slots__ = ['__transform', 'inversetransform']

    def __init__(self, transform=None):
        if transform is None:
            self.transform = rt.identity4()
        else:
            self.transform = transform

    @property
    def transform(self):
        return self.__transform

    @transform.setter
    def transform(self, trans):
        self.__transform = trans
        self.inversetransform = rt.inverse4x4(self.__transform)

    def color_at(self, pattern_point):
        # point is in pattern space
        return rt.Color(1.0, 1.0, 1.0)


class TestPattern(Pattern):
    def __init__(self, transform=None):
        super().__init__(transform)

    def color_at(self, pattern_point):
        return rt.Color(pattern_point.x, pattern_point.y, pattern_point.z)


class StripePattern(Pattern):
    __slots__ = ['color1', 'color2']

    def __init__(self, transform=None, color1=None, color2=None):
        super().__init__(transform)
        if color1 is None:
            self.color1 = rt.Color(1.0, 1.0, 1.0)
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = rt.Color(0.0, 0.0, 0.0)
        else:
            self.color2 = color2

    def color_at(self, pattern_point):
        if pattern_point.x % 2 >= 1.0:
            return self.color2
        else:
            return self.color1


class GradientPattern(Pattern):
    __slots__ = ['color1', 'color2']

    def __init__(self, transform=None, color1=None, color2=None):
        super().__init__(transform)
        if color1 is None:
            self.color1 = rt.Color(1.0, 1.0, 1.0)
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = rt.Color(0.0, 0.0, 0.0)
        else:
            self.color2 = color2

    def color_at(self, pattern_point):
        distance = self.color2 - self.color1
        fraction = pattern_point.x - math.floor(pattern_point.x)
        return self.color1 + (distance * fraction)


class RingPattern(Pattern):
    __slots__ = ['color1', 'color2']

    def __init__(self, transform=None, color1=None, color2=None):
        super().__init__(transform)
        if color1 is None:
            self.color1 = rt.Color(1.0, 1.0, 1.0)
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = rt.Color(0.0, 0.0, 0.0)
        else:
            self.color2 = color2

    def color_at(self, pattern_point):
        if math.sqrt(pattern_point.x * pattern_point.x + pattern_point.z * pattern_point.z) % 2 >= 1.0:
            return self.color2
        else:
            return self.color1


class CheckersPattern(Pattern):
    __slots__ = ['color1', 'color2']

    def __init__(self, transform=None, color1=None, color2=None):
        super().__init__(transform)
        if color1 is None:
            self.color1 = rt.Color(1.0, 1.0, 1.0)
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = rt.Color(0.0, 0.0, 0.0)
        else:
            self.color2 = color2

    def color_at(self, pattern_point):

        x = math.floor(pattern_point.x)
        if pattern_point.x - x > ONEMINUSEPSILON:
            x = x + 1
        y = math.floor(pattern_point.y)
        if pattern_point.y - y > ONEMINUSEPSILON:
            y = y + 1
        z = math.floor(pattern_point.z)
        if pattern_point.z - z > ONEMINUSEPSILON:
            z = z + 1

        if (x + y + z) % 2 == 0:
            return self.color1
        else:
            return self.color2


class GridPattern(Pattern):
    __slots__ = ['color1', 'color2', 'thickness']

    def __init__(self, transform=None, color1=None, color2=None, thickness=0.05):
        assert 0 <= thickness <= 1
        super().__init__(transform)
        if color1 is None:
            self.color1 = rt.Color(1.0, 1.0, 1.0)
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = rt.Color(0.0, 0.0, 0.0)
        else:
            self.color2 = color2
        self.thickness = thickness

    def color_at(self, pattern_point):

        s = pattern_point.x - math.floor(pattern_point.x)
        if s < self.thickness or s > (1 - self.thickness):
            return self.color2
        s = pattern_point.z - math.floor(pattern_point.z)
        if s < self.thickness or s > (1 - self.thickness):
            return self.color2
        return self.color1


class BlendedPattern(Pattern):
    __slots__ = ['pattern1', 'pattern2']

    def __init__(self, transform=None, pattern1=None, pattern2=None):
        super().__init__(transform)
        if pattern1 is None:
            self.pattern1 = Pattern()
        else:
            self.pattern1 = pattern1
        if pattern2 is None:
            self.pattern2 = Pattern()
        else:
            self.pattern2 = pattern2

    def color_at(self, pattern_point):
        p1 = rt.matmul4xTuple(self.pattern1.inversetransform, pattern_point)
        p2 = rt.matmul4xTuple(self.pattern2.inversetransform, pattern_point)

        c1 = self.pattern1.color_at(p1)
        c2 = self.pattern2.color_at(p2)
        return (c1 + c2) / 2


class NestedCheckersPattern(BlendedPattern):
    def __init__(self, transform=None, pattern1=None, pattern2=None):
        super().__init__(transform, pattern1, pattern2)

    def color_at(self, pattern_point):
        x = math.floor(pattern_point.x)
        if pattern_point.x - x > ONEMINUSEPSILON:
            x = x + 1
        y = math.floor(pattern_point.y)
        if pattern_point.y - y > ONEMINUSEPSILON:
            y = y + 1
        z = math.floor(pattern_point.z)
        if pattern_point.z - z > ONEMINUSEPSILON:
            z = z + 1

        if (x + y + z) % 2 == 0:
            p1 = rt.matmul4xTuple(self.pattern1.inversetransform, pattern_point)
            return self.pattern1.color_at(p1)
        else:
            p2 = rt.matmul4xTuple(self.pattern2.inversetransform, pattern_point)
            return self.pattern2.color_at(p2)


class Material:
    __slots__ = ['color', 'pattern', 'ambient', 'diffuse', 'specular', 'shininess', 'reflective', 'transparency',
                 'refractive_index', 'fuzz']

    def __init__(self, color=None, ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0, reflective=0, pattern=None,
                 transparency=0.0, refractive_index=1.0, fuzz=0.0):
        if color is None:
            self.color = rt.Color(1, 1, 1)
        else:
            self.color = color
        self.pattern = pattern
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflective = reflective
        self.transparency = transparency
        self.refractive_index = refractive_index
        self.fuzz = fuzz

    def __eq__(self, other):
        # may only be needed for unit tests.  Ignores pattern because it's not needed for these tests.
        return self.color == other.color and math.isclose(self.ambient, other.ambient) and \
            math.isclose(self.diffuse, other.diffuse) and math.isclose(self.specular, other.specular) and \
            math.isclose(self.shininess, other.shininess) and math.isclose(self.reflective, other.reflective) and \
            math.isclose(self.transparency, other.transparency) and \
            math.isclose(self.refractive_index, other.refractive_index)
