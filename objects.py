import math
import rttuple
import transformations
import materials
import matrices


class Intersection:
    def __init__(self, objhit, t):
        self.objhit = objhit
        self.t = t


EPSILON = 0.0001
ONEMINUSEPSILON = 1 - EPSILON


class HittableObject:
    def __init__(self, transform=matrices.identity4(), material=None):
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
        self.__inversetransform = matrices.inverse4x4(self.__transform)

    @property
    def inversetransform(self):
        return self.__inversetransform

    def intersect(self, r):
        # returns a list of intersections
        object_ray = transformations.transformray(self.inversetransform, r)
        return self.local_intersect(object_ray)

    def local_intersect(self, object_ray):
        # this method should be overridden by every base class
        # ray should be converted to object space by intersect() before calling this
        return []

    def normal_at(self, point):
        object_point = transformations.transform(self.inversetransform, point)
        object_normal = self.local_normal_at(object_point)
        world_normal = transformations.transform(matrices.transpose4x4(self.inversetransform), object_normal)
        # hack - should really get the submatrix of the transform, and multiply by the inverse and
        # transform that, but this is much faster and equivalent.
        world_normal.w = 0.0
        return rttuple.normalize(world_normal)

    def local_normal_at(self, object_point):
        # this method should be overridden by every base class
        # point should be converted to object space by normal_at() before calling this
        return rttuple.Vector()


class Sphere(HittableObject):
    def __init__(self, transform=matrices.identity4(), material=None):
        super().__init__(transform, material)
        self.origin = rttuple.Point(0, 0, 0)

    def local_intersect(self, object_ray):
        # original logic:
        # sphere_to_ray = r.origin - self.center
        # a = rttuple.dot(r.direction, r.direction)
        # b = 2 * rttuple.dot(r.direction, sphere_to_ray)
        # c = rttuple.dot(sphere_to_ray, sphere_to_ray) - (self.radius * self.radius)
        # discriminant = (b * b) - (4 * a * c)

        # speedup from mpraytracer, factoring in that center is always 0,0,0 and
        # radius is always 1, and we use transform to move the ray:

        # TODO - if we don't ever change the coordinates of the origin, we can take this rttuple.Point(0,0,0) out.
        sphere_to_ray = object_ray.origin - self.origin
        a = rttuple.dot(object_ray.direction, object_ray.direction)
        half_b = rttuple.dot(object_ray.direction, sphere_to_ray)
        c = rttuple.dot(sphere_to_ray, sphere_to_ray) - 1
        discriminant = (half_b * half_b) - (a * c)

        if discriminant < 0:
            return []
        else:
            sqrtd = math.sqrt(discriminant)
            t1 = (-half_b - sqrtd) / a
            t2 = (-half_b + sqrtd) / a
            return [Intersection(self, t1), Intersection(self, t2)]

    def local_normal_at(self, object_point):
        return object_point - self.origin


class Plane(HittableObject):
    def __init__(self, transform=matrices.identity4(), material=None):
        super().__init__(transform, material)

    def local_intersect(self, object_ray):
        # if ray is parallel to plane we say it misses (even if it's a
        # coplanar ray, cannot see an infinitely thin plane looking head on)
        if math.fabs(object_ray.direction.y) <= EPSILON:
            return []
        else:
            t = -object_ray.origin.y / object_ray.direction.y
            return [Intersection(self, t)]

    def local_normal_at(self, object_point):
        return rttuple.Vector(0, 1, 0)
