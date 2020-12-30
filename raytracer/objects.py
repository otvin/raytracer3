import math
import raytracer as rt
from .matrices import identity4


class Intersection:
    __slots__ = ['objhit', 't']

    def __init__(self, objhit, t):
        self.objhit = objhit
        self.t = t


EPSILON = 0.0001
ONEMINUSEPSILON = 1 - EPSILON


class HittableObject:
    __slots__ = ['material', '__transform', 'inversetransform', '__inversetransformtranspose', 'casts_shadow']

    def __init__(self, transform=identity4(), material=None, casts_shadow=True):
        if material is None:
            self.material = rt.Material()
        else:
            self.material = material
        self.transform = transform
        self.casts_shadow = casts_shadow

    @property
    def transform(self):
        return self.__transform

    @transform.setter
    def transform(self, trans):
        self.__transform = trans
        self.inversetransform = rt.inverse4x4(self.__transform)
        self.__inversetransformtranspose = rt.transpose4x4(self.inversetransform)

    def intersect(self, r):
        # returns a list of intersections
        object_ray = rt.do_transformray(self.inversetransform, r)
        return self.local_intersect(object_ray)

    def local_intersect(self, object_ray):
        # this method should be overridden by every base class
        # ray should be converted to object space by intersect() before calling this
        return []

    def normal_at(self, point):
        object_point = rt.do_transform(self.inversetransform, point)
        object_normal = self.local_normal_at(object_point)
        world_normal = rt.transformations.do_transform(self.__inversetransformtranspose, object_normal)
        # hack - should really get the submatrix of the transform, and multiply by the inverse and
        # transform that, but this is much faster and equivalent.
        world_normal.w = 0.0
        return rt.normalize(world_normal)

    def local_normal_at(self, object_point):
        # this method should be overridden by every base class
        # point should be converted to object space by normal_at() before calling this
        return rt.Vector()


class Sphere(HittableObject):
    __slots__ = ['origin']

    def __init__(self, transform=identity4(), material=None):
        super().__init__(transform, material)
        self.origin = rt.Point(0, 0, 0)

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
        a = rt.dot(object_ray.direction, object_ray.direction)
        half_b = rt.dot(object_ray.direction, sphere_to_ray)
        c = rt.dot(sphere_to_ray, sphere_to_ray) - 1
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
    def __init__(self, transform=identity4(), material=None):
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
        return rt.Vector(0, 1, 0)


def check_axis(origin, direction):
    # helper function for cube intersection, but doesn't rely on cube itself
    tmin_numerator = -1 - origin
    tmax_numerator = 1 - origin
    if math.fabs(direction) >= EPSILON:
        tmin = tmin_numerator / direction
        tmax = tmax_numerator / direction
    else:
        # if the line is parallel to the axis, it won't intersect
        tmin = tmin_numerator * math.inf  # the multiplication gets the sign right
        tmax = tmax_numerator * math.inf

    if tmin > tmax:
        tmin, tmax = tmax, tmin  # swap them

    return tmin, tmax


class Cube(HittableObject):
    def __init__(self, transform=identity4(), material=None):
        super().__init__(transform, material)

    def local_intersect(self, object_ray):

        # TODO: p.176: When comparing a ray with the cube's sides, the algorithm
        # checks all three sides even if it's obvious by first or second comparison
        # that the ray misses.  How can this be optimized?

        xtmin, xtmax = check_axis(object_ray.origin.x, object_ray.direction.x)
        ytmin, ytmax = check_axis(object_ray.origin.y, object_ray.direction.y)
        ztmin, ztmax = check_axis(object_ray.origin.z, object_ray.direction.z)

        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)

        if tmin > tmax or tmax < 0:
            return []
        else:
            return [Intersection(self, tmin), Intersection(self, tmax)]

    def local_normal_at(self, object_point):
        abs_point = (math.fabs(object_point.x), math.fabs(object_point.y), math.fabs(object_point.z))
        maxc = max(abs_point)
        if math.isclose(maxc, abs_point[0]):
            return rt.Vector(object_point.x, 0, 0)
        elif math.isclose(maxc, abs_point[1]):
            return rt.Vector(0, object_point.y, 0)
        else:
            return rt.Vector(0, 0, object_point.z)
