import math
import raytracer as rt
from .objects import check_axis

# Bounding boxes are found in the bonus chapter at http://www.raytracerchallenge.com/bonus/bounding-boxes.html

class BoundingBox():
    __slots__ = ['boxmin', 'boxmax']

    def __init__(self, boxmin=None, boxmax=None):
        if boxmin is None:
            self.boxmin = rt.Point(math.inf, math.inf, math.inf)
        else:
            self.boxmin = boxmin
        if boxmax is None:
            self.boxmax = rt.Point(-math.inf, -math.inf, -math.inf)
        else:
            self.boxmax = boxmax

    def __str__(self):
        return ('min: {}, max: {}'.format(self.boxmin, self.boxmax))

    def __iadd__(self, other):
        self.addpoint(other.boxmin)
        self.addpoint(other.boxmax)
        return self

    def addpoint(self, point):
        if point.x < self.boxmin.x:
            self.boxmin.x = point.x
        if point.x > self.boxmax.x:
            self.boxmax.x = point.x

        if point.y < self.boxmin.y:
            self.boxmin.y = point.y
        if point.y > self.boxmax.y:
            self.boxmax.y = point.y

        if point.z < self.boxmin.z:
            self.boxmin.z = point.z
        if point.z > self.boxmax.z:
            self.boxmax.z = point.z

    def contains_point(self, point):
        return self.boxmin.x <= point.x <= self.boxmax.x and \
                self.boxmin.y <= point.y <= self.boxmax.y and \
                self.boxmin.z <= point.z <= self.boxmax.z

    def contains_box(self, other):
        return self.contains_point(other.boxmin) and self.contains_point(other.boxmax)

    def transform(self, matrix):
        # transform all 8 points on the cube by the matrix, add them all to a new box
        p1 = self.boxmin
        p2 = rt.Point(self.boxmin.x, self.boxmin.y, self.boxmax.z)
        p3 = rt.Point(self.boxmin.x, self.boxmax.y, self.boxmin.z)
        p4 = rt.Point(self.boxmin.x, self.boxmax.y, self.boxmax.z)
        p5 = rt.Point(self.boxmax.x, self.boxmin.y, self.boxmin.z)
        p6 = rt.Point(self.boxmax.x, self.boxmin.y, self.boxmax.z)
        p7 = rt.Point(self.boxmax.x, self.boxmax.y, self.boxmin.z)
        p8 = self.boxmax

        new_box = rt.BoundingBox()

        for p in (p1, p2, p3, p4, p5, p6, p7, p8):
            new_box.addpoint(rt.do_transform(matrix, p))

        return new_box

    def intersects(self, ray):
        # very similar logic from objects.Cube()
        xtmin, xtmax = check_axis(ray.origin.x, ray.direction.x, self.boxmin.x, self.boxmax.x)
        ytmin, ytmax = check_axis(ray.origin.y, ray.direction.y, self.boxmin.y, self.boxmax.y)

        if xtmin > ytmax or ytmin > xtmax:
            return False

        ztmin, ztmax = check_axis(ray.origin.z, ray.direction.z, self.boxmin.z, self.boxmax.z)

        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)

        if tmin > tmax or tmax < 0:
            return False
        else:
            return True

    def split_bounds(self):
        xmin = self.boxmin.x
        ymin = self.boxmin.y
        zmin = self.boxmin.z

        xmax = self.boxmax.x
        ymax = self.boxmax.y
        zmax = self.boxmax.z

        dx = xmax - xmin
        dy = ymax - ymin
        dz = zmax - zmin

        greatest = max(dx, dy, dz)

        if math.isclose(dx, greatest):
            xmin = xmax = xmin + dx / 2.0
        elif math.isclose(dy, greatest):
            ymin = ymax = ymin + dy / 2.0
        else:
            zmin = zmax = zmin + dz / 2.0

        mid_min = rt.Point(xmin, ymin, zmin)
        mid_max = rt.Point(xmax, ymax, zmax)

        return BoundingBox(self.boxmin, mid_max), BoundingBox(mid_min, self.boxmax)
