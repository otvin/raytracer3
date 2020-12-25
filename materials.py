import math
import rttuple
import matrices


class Pattern:
    def __init__(self, transform=None):
        if transform is None:
            self.transform = matrices.identity4()
        else:
            self.transform = transform

    @property
    def transform(self):
        return self.__transform

    @transform.setter
    def transform(self, trans):
        self.__transform = trans
        self.__inversetransform = matrices.inverse4x4(self.__transform)

    @property
    def inversetransform(self):
        return self.__inversetransform

    def color_at(self, pattern_point):
        # point is in pattern space
        return rttuple.Color(1.0, 1.0, 1.0)


class StripePattern(Pattern):
    def __init__(self, transform=None, color1=None, color2=None):
        super().__init__(transform)
        if color1 is None:
            self.color1 = rttuple.Color(1.0, 1.0, 1.0)
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = rttuple.Color(0.0, 0.0, 0.0)
        else:
            self.color2 = color2

    def color_at(self, pattern_point):
        if pattern_point.x % 2 >= 1.0:
            return self.color2
        else:
            return self.color1


class Material:
    def __init__(self, color=None, ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0, pattern=None):
        if color is None:
            self.color = rttuple.Color(1, 1, 1)
        else:
            self.color = color
        if pattern is None:
            self.pattern = Pattern()
        else:
            self.pattern = pattern
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def __eq__(self, other):
        # may only be needed for unit tests
        return self.color == other.color and math.isclose(self.ambient, other.ambient) and \
            math.isclose(self.diffuse, other.diffuse) and math.isclose(self.specular, other.specular) and \
            math.isclose(self.shininess, other.shininess)
