import math
import raytracer as rt
from .objects import check_axis

# Bounding boxes are found in the bonus chapter at http://www.raytracerchallenge.com/bonus/bounding-boxes.html

class BoundingBox():
    __slots__ = ['min', 'max']

    def __init__(self, min=None, max=None):
        if min is None:
            self.min = rt.Point(math.inf, math.inf, math.inf)
        else:
            self.min = min
        if max is None:
            self.max = rt.Point(-math.inf, -math.inf, -math.inf)
        else:
            self.max = max

    def __str__(self):
        return ('min: {}, max: {}'.format(self.min, self.max))

    def __iadd__(self, other):
        self.addpoint(other.min)
        self.addpoint(other.max)
        return self

    def addpoint(self, point):
        if point.x < self.min.x:
            self.min.x = point.x
        if point.x > self.max.x:
            self.max.x = point.x

        if point.y < self.min.y:
            self.min.y = point.y
        if point.y > self.max.y:
            self.max.y = point.y

        if point.z < self.min.z:
            self.min.z = point.z
        if point.z > self.max.z:
            self.max.z = point.z

    def contains_point(self, point):
        return self.min.x <= point.x <= self.max.x and \
                self.min.y <= point.y <= self.max.y and \
                self.min.z <= point.z <= self.max.z

    def contains_box(self, other):
        return self.contains_point(other.min) and self.contains_point(other.max)

    def transform(self, matrix):
        # transform all 8 points on the cube by the matrix, add them all to a new box
        p1 = self.min
        p2 = rt.Point(self.min.x, self.min.y, self.max.z)
        p3 = rt.Point(self.min.x, self.max.y, self.min.z)
        p4 = rt.Point(self.min.x, self.max.y, self.max.z)
        p5 = rt.Point(self.max.x, self.min.y, self.min.z)
        p6 = rt.Point(self.max.x, self.min.y, self.max.z)
        p7 = rt.Point(self.max.x, self.max.y, self.min.z)
        p8 = self.max

        new_box = rt.BoundingBox()

        for p in (p1, p2, p3, p4, p5, p6, p7, p8):
            new_box.addpoint(rt.do_transform(matrix, p))

        return new_box

    def intersects(self, ray):
        # very similar logic from objects.Cube()
        xtmin, xtmax = check_axis(ray.origin.x, ray.direction.x, self.min.x, self.max.x)
        ytmin, ytmax = check_axis(ray.origin.y, ray.direction.y, self.min.y, self.max.y)

        if xtmin > ytmax or ytmin > xtmax:
            return False

        ztmin, ztmax = check_axis(ray.origin.z, ray.direction.z, self.min.z, self.max.z)

        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)

        if tmin > tmax or tmax < 0:
            return False
        else:
            return True
