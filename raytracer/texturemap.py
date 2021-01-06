import math
from .materials import Pattern
import raytracer as rt


def spherical_map(point):
    # compute the azimuthal angle
    # -π < theta <= π
    # angle increases clockwise as viewed from above,
    # which is opposite of what we want, but we'll fix it later.
    theta = math.atan2(point.x, point.z)

    # vec is the vector pointing from the sphere's origin (the world origin)
    # to the point, which will also happen to be exactly equal to the sphere's
    # radius.
    vec = rt.Vector(point.x, point.y, point.z)
    radius = vec.magnitude()

    # compute the polar angle
    # 0 <= phi <= π
    phi = math.acos(point.y / radius)

    # -0.5 < raw_u <= 0.5
    raw_u = theta / (2 * math.pi)

    # 0 <= u < 1
    # here's also where we fix the direction of u. Subtract it from 1,
    # so that it increases counterclockwise as viewed from above.
    u = 1 - (raw_u + 0.5)

    # we want v to be 0 at the south pole of the sphere,
    # and 1 at the north pole, so we have to "flip it over"
    # by subtracting it from 1.
    v = 1 - (phi / math.pi)

    return u, v


class UVPattern(Pattern):
    __slots__ = ['width', 'height', 'mapfn']

    def __init__(self, width, height, mapfn=None):
        super().__init__(None)
        self.width = width
        self.height = height
        if mapfn is None:
            self.mapfn = spherical_map
        else:
            self.mapfn = mapfn


class UVCheckersPattern(UVPattern):
    __slots__ = ['color1', 'color2']

    def __init__(self, width=2, height=2, color1=None, color2=None, mapfn=None):
        super().__init__(width, height, mapfn)
        if color1 is None:
            self.color1 = rt.Color(0, 0, 0)
        else:
            self.color1 = color1
        if color2 is None:
            self.color2 = rt.Color(1, 1, 1)
        else:
            self.color2 = color2

    def uv_color_at(self, u, v):
        u2 = math.floor(u * self.width)
        v2 = math.floor(v * self.height)
        if (u2 + v2) % 2 == 0:
            return self.color1
        else:
            return self.color2

    def color_at(self, pattern_point):
        u, v = self.mapfn(pattern_point)
        return self.uv_color_at(u, v)
