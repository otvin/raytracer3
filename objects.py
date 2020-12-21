import math
import tuple


class Intersection():
    def __init__(self, objhit, t):
        self.objhit = objhit
        self.t = t


class HittableObject:
    def __init__(self):
        pass

    def intersect(self, r):
        # returns a list of intersections
        return []


class Sphere(HittableObject):
    def __init__(self, center=tuple.Point(0,0,0), radius=1.0):
        self.center = center
        self.radius = radius

    def intersect(self, r):
        assert isinstance(r, tuple.Ray)

        # original logic:
        # sphere_to_ray = r.origin - self.center
        # a = tuple.dot(r.direction, r.direction)
        # b = 2 * tuple.dot(r.direction, sphere_to_ray)
        # c = tuple.dot(sphere_to_ray, sphere_to_ray) - (self.radius * self.radius)
        # discriminant = (b * b) - (4 * a * c)

        # speedup from mpraytracer:
        sphere_to_ray = r.origin - self.center
        a = tuple.dot(r.direction, r.direction)
        half_b = tuple.dot(r.direction, sphere_to_ray)
        c = tuple.dot(sphere_to_ray, sphere_to_ray) - (self.radius * self.radius)
        discriminant = (half_b * half_b) - (a * c)

        if discriminant < 0:
            return []
        else:
            sqrtd = math.sqrt(discriminant)
            t1 = (-half_b - sqrtd) / a
            t2 = (-half_b + sqrtd) / a
            return [Intersection(self, t1), Intersection(self, t2)]


def hit(intersections):
    # for now, intersections is a list of Intersection objects.  Function returns the first object hit, which
    # is the intersection with the smallest non-negative t.
    assert isinstance(intersections, list)
    intersections.sort(key=lambda x: x.t)
    for i in intersections:
        if i.t > 0:
            return i
    return None
