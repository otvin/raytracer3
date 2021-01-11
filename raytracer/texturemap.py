import math
from .materials import Pattern
from .canvas import get_canvasdims, pixel_at
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


def planar_map(point):
    return point.x % 1, point.z % 1


def cylindrical_map(point):
    # u is computed based on the azimuthal angle, same as with spherical_map()
    theta = math.atan2(point.x, point.z)
    raw_u = theta / (2 * math.pi)
    u = 1 - (raw_u + 0.5)

    # v goes from 0 to 1 between whole units of y
    v = point.y % 1
    return u, v


FACELEFT = 0
FACERIGHT = 1
FACEFRONT = 2
FACEBACK = 3
FACEUP = 4
FACEDOWN = 5


def face_from_point(point):
    absx = math.fabs(point.x)
    absy = math.fabs(point.y)
    absz = math.fabs(point.z)

    if absx > absy and absx > absz:
        if point.x < 0:
            return FACELEFT
        else:
            return FACERIGHT
    elif absy > absz:
        if point.y < 0:
            return FACEDOWN
        else:
            return FACEUP
    elif point.z < 0:
        return FACEBACK
    else:
        return FACEFRONT


def cube_uv_front(point):
    # u goes -1 .. 1 on the x axis
    # v goes -1 .. 1 on the y axis
    # add 1 to x so range goes from 0 .. 2
    # mod 2 so points outside the range repeat
    # divide by 2 so final range is between 0..1
    # v is same.
    u = ((point.x + 1) % 2) / 2
    v = ((point.y + 1) % 2) / 2
    return u, v


def cube_uv_back(point):
    # u goes 1 .. -1 on the x axis
    # v goes -1 .. 1 on the y axis
    # take 1 - x so range goes from 0 .. 2
    # then repeat steps from above
    u = ((1 - point.x) % 2) / 2
    v = ((point.y + 1) % 2) / 2
    return u, v


def cube_uv_up(point):
    # u goes -1 .. 1 on the x axis (diagram in book is incorrect, see errata)
    # v goes 1 .. -1 on the z axis
    u = ((point.x + 1) % 2) / 2
    v = ((1 - point.z) % 2) / 2
    return u, v


def cube_uv_down(point):
    # u goes -1 .. 1 on the x axis (diagram in book is incorrect, see errata)
    # v goes -1 .. 1 on the z axis
    u = ((point.x + 1) % 2) / 2
    v = ((point.z + 1) % 2) / 2
    return u, v


def cube_uv_left(point):
    # u goes -1 .. 1 on the z axis
    # v goes -1 .. 1 on the y axis
    u = ((point.z + 1) % 2) / 2
    v = ((point.y + 1) % 2) / 2
    return u, v


def cube_uv_right(point):
    # u goes from 1 .. -1 on the z axis
    # v goes from -1 .. 1 on the y axis
    u = ((1 - point.z) % 2) / 2
    v = ((point.y + 1) % 2) / 2
    return u, v


class UVPattern(Pattern):
    __slots__ = ['width', 'height', 'mapfn']

    def __init__(self, mapfn=None):
        super().__init__(None)
        if mapfn is None:
            self.mapfn = spherical_map
        else:
            self.mapfn = mapfn

    def uv_color_at(self, u, v):
        raise NotImplementedError

    def color_at(self, pattern_point):
        u, v = self.mapfn(pattern_point)
        return self.uv_color_at(u, v)


class UVAlignCheckPattern(UVPattern):
    __slots__ = ['main', 'ul', 'ur', 'bl', 'br']

    def __init__(self, main=None, ul=None, ur=None, bl=None, br=None, mapfn=None):
        super().__init__(mapfn or planar_map)
        self.main = main or rt.Color(1, 1, 1)
        self.ul = ul or rt.Color(1, 0, 0)
        self.ur = ur or rt.Color(1, 1, 0)
        self.bl = bl or rt.Color(0, 1, 0)
        self.br = br or rt.Color(0, 1, 1)

    def uv_color_at(self, u, v):
        if u > 0.8:
            if v < 0.2:
                return self.br
            elif v > 0.8:
                return self.ur
        elif u < 0.2:
            if v < 0.2:
                return self.bl
            elif v > 0.8:
                return self.ul
        return self.main


class UVCheckersPattern(UVPattern):
    __slots__ = ['width', 'height', 'color1', 'color2']

    def __init__(self, width=2, height=2, color1=None, color2=None, mapfn=None):
        super().__init__(mapfn)
        self.width = width
        self.height = height
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


# TODO - support more than one image pattern at a time
class UVImagePattern(UVPattern):
    __slots__ = ['width', 'height']

    def __init__(self, filename, mapfn=None):
        super().__init__(mapfn or planar_map)
        rt.canvas_from_ppm(filename)
        self.width, self.height = get_canvasdims(True)

    def uv_color_at(self, u, v):
        # flip v over so it matches the image layout, with y at the top
        realv = 1 - v

        x = round(u * (self.width - 1))
        y = round(realv * (self.height - 1))
        return pixel_at(x, y, True)


class CubeMap(Pattern):
    __slots__ = ["leftpattern", "rightpattern", "frontpattern", "backpattern", "uppattern", "downpattern"]

    def __init__(self):
        super().__init__(None)
        self.leftpattern = None
        self.rightpattern = None
        self.frontpattern = None
        self.backpattern = None
        self.uppattern = None
        self.downpattern = None

    def setupdemo(self):
        red = rt.Color(1, 0, 0)
        yellow = rt.Color(1, 1, 0)
        brown = rt.Color(1, 0.5, 0)
        green = rt.Color(0, 1, 0)
        cyan = rt.Color(0, 1, 1)
        blue = rt.Color(0, 0, 1)
        purple = rt.Color(1, 0, 1)
        white = rt.Color(1, 1, 1)

        self.leftpattern = UVAlignCheckPattern(yellow, cyan, red, blue, brown, rt.cube_uv_left)
        self.rightpattern = UVAlignCheckPattern(red, yellow, purple, green, white, rt.cube_uv_right)
        self.frontpattern = UVAlignCheckPattern(cyan, red, yellow, brown, green, rt.cube_uv_front)
        self.backpattern = UVAlignCheckPattern(green, purple, cyan, white, blue, rt.cube_uv_back)
        self.uppattern = UVAlignCheckPattern(brown, cyan, purple, red, yellow, rt.cube_uv_up)
        self.downpattern = UVAlignCheckPattern(purple, brown, green, blue, white, rt.cube_uv_down)

    def color_at(self, pattern_point):
        face = face_from_point(pattern_point)
        if face == FACELEFT:
            pat = self.leftpattern
        elif face == FACERIGHT:
            pat = self.rightpattern
        elif face == FACEFRONT:
            pat = self.frontpattern
        elif face == FACEBACK:
            pat = self.backpattern
        elif face == FACEUP:
            pat = self.uppattern
        else:
            pat = self.downpattern

        u, v = pat.mapfn(pattern_point)
        return pat.uv_color_at(u, v)
