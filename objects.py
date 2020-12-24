import math
import numpy as np
import tuple
import transformations
import materials


class Intersection():
    def __init__(self, objhit, t):
        self.objhit = objhit
        self.t = t


class HitRecord():
    def __init__(self, t, objhit, point, eyev, normalv):
        self.t = t
        self.objhit = objhit
        self.point = point
        self.eyev = eyev
        if tuple.dot(normalv, eyev) < 0:
            self.inside = True
            self.normalv = -normalv
        else:
            self.inside = False
            self.normalv = normalv


class HittableObject:
    def __init__(self, transform=np.identity(4), material=None):
        if material is None:
            self.material = materials.Material()
        else:
            self.material = material
        self.transform = transform

    @property
    def transform(self):
        return self.__transform

    @transform.setter
    def transform(self, trans):
        self.__transform = trans
        self.__inversetransform = np.linalg.inv(self.__transform)

    @property
    def inversetransform(self):
        return self.__inversetransform

    def intersect(self, r):
        # returns a list of intersections
        return []

    def normal_at(self, point):
        return tuple.Vector()


class Sphere(HittableObject):
    def __init__(self, transform=np.identity(4), material=None):
        super().__init__(transform, material)
        self.origin = tuple.Point(0, 0, 0)


    def intersect(self, r):
        # original logic:
        # sphere_to_ray = r.origin - self.center
        # a = tuple.dot(r.direction, r.direction)
        # b = 2 * tuple.dot(r.direction, sphere_to_ray)
        # c = tuple.dot(sphere_to_ray, sphere_to_ray) - (self.radius * self.radius)
        # discriminant = (b * b) - (4 * a * c)

        # speedup from mpraytracer, factoring in that center is always 0,0,0 and
        # radius is always 1, and we use transform to move the ray:

        r2 = transformations.transformray(self.inversetransform, r)

        # TODO - if we don't ever change the coordinates of the origin, we can take this tuple.Point(0,0,0) out.
        sphere_to_ray = r2.origin - self.origin
        a = tuple.dot(r2.direction, r2.direction)
        half_b = tuple.dot(r2.direction, sphere_to_ray)
        c = tuple.dot(sphere_to_ray, sphere_to_ray) - 1
        discriminant = (half_b * half_b) - (a * c)

        if discriminant < 0:
            return []
        else:
            sqrtd = math.sqrt(discriminant)
            t1 = (-half_b - sqrtd) / a
            t2 = (-half_b + sqrtd) / a
            return [Intersection(self, t1), Intersection(self, t2)]

    def normal_at(self, point):
        # get the point moved into object space
        object_point = transformations.transform(self.inversetransform, point)
        object_normal = object_point - self.origin
        world_normal = transformations.transform(np.matrix.transpose(self.inversetransform), object_normal)
        # hack - should really get the submatrix of the transform, and multiply by the inverse and
        # transform that, but this is much faster and equivalent.
        world_normal.w = 0.0
        return tuple.normalize(world_normal)


def hit(intersections):
    # for now, intersections is a list of Intersection objects.  Function returns the first object hit, which
    # is the intersection with the smallest non-negative t.
    assert isinstance(intersections, list)
    intersections.sort(key=lambda x: x.t)
    for i in intersections:
        if i.t > 0:
            return i
    return None
