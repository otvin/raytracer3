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

        # TODO - since we never change the origin of the sphere, we could
        # just create a vector out of object_ray.origin.x/y/z and save the
        # 4 subtractions that are done here in the tuple subtract.
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

        xtmin, xtmax = check_axis(object_ray.origin.x, object_ray.direction.x)
        ytmin, ytmax = check_axis(object_ray.origin.y, object_ray.direction.y)

        if xtmin > ytmax or ytmin > xtmax:
            return []

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


def check_cap(ray, t):
    # helper function for cylinder intersection, but doesn't rely on cylinder itself
    ro = ray.origin
    rd = ray.direction
    rox = ro.x
    roz = ro.z
    rdx = rd.x
    rdz = rd.z
    x = rox + (t * rdx)
    z = roz + (t * rdz)
    return (x * x + z * z) <= 1


class Cylinder(HittableObject):
    __slots__ = ['closed', 'min_y', 'max_y']

    def __init__(self, transform=identity4(), material=None, closed=False, min_y=-math.inf, max_y=math.inf):
        super().__init__(transform, material)
        self.closed = closed
        self.min_y = min_y
        self.max_y = max_y

    def local_intersect(self, object_ray):
        rd = object_ray.direction
        ro = object_ray.origin
        rdx = rd.x
        rdz = rd.z
        rox = ro.x
        roz = ro.z
        roy = ro.y
        rdy = rd.y

        res = []

        # First check for intersection with the caps
        if self.closed:
            # check for intersection with lower end cap by intersecting the ray
            # with the plane at y = self.min_y
            t = (self.min_y - roy) / rdy
            if check_cap(object_ray, t):
                res.append(Intersection(self, t))

            # check for intersection with upper end cap by intersecting the ray
            # with the plane at y = self.max_y
            t = (self.max_y - roy) / rdy
            if check_cap(object_ray, t):
                res.append(Intersection(self, t))

        # now intersect with the body of the cylinder

        # original logic:
        # a = (rdx * rdx) + (rdz * rdz)
        # b = 2 * ((rox * rdx) + (roz * rdz))
        # c = (rox * rox) + (roz * roz) - 1


        # uses same "half b" trick from Sphere.local_intersect()
        a = (rdx * rdx) + (rdz * rdz)

        # ray is parallel to the y axis
        if a < EPSILON:
            return res

        half_b = ((rox * rdx) + (roz * rdz))

        c = (rox * rox) + (roz * roz) - 1

        discriminant = (half_b * half_b) - (a * c)
        if discriminant < 0:
            return res

        sqrtd = math.sqrt(discriminant)
        t1 = (-half_b - sqrtd) / a
        t2 = (-half_b + sqrtd) / a

        # If we were rendering many infinite cylinders, we would
        # do an "if infinite cylinder, return both intersections, else..."
        # However, since almost all cylinders will be bounded, we will
        # not do the needless comparison

        y1 = roy + (t1 * rdy)
        if self.min_y < y1 < self.max_y:  # note strict less than
            res.append(Intersection(self, t1))
        y2 = roy + (t2 * rdy)
        if self.min_y < y2 < self.max_y:
            res.append(Intersection(self, t2))

        return res


    def local_normal_at(self, object_point):
        # Remember: local_normal_at assumes object_point is on the object.
        # So for cylinder it either needs to be on an end cap (which means
        # the cylinder must be closed) or on the body.

        # compute square of distance from the y axis
        opx = object_point.x
        opz = object_point.z
        dist = (opx * opx) + (opz * opz)
        if dist < ONEMINUSEPSILON:
            # it must have intersected an end cap because the cylinder
            # has x^2 + z^2 = 1 in object space
            if object_point.y >= self.max_y - EPSILON:
                # top cap
                return rt.Vector(0, 1, 0)
            else:
                # must be bottom cap
                return rt.Vector(0, -1, 0)
        else:
            return rt.Vector(object_point.x, 0, object_point.z)


def check_cone_cap(ray, t, y):
    # helper function for cone intersection, but doesn't rely on cone itself
    ro = ray.origin
    rd = ray.direction
    rox = ro.x
    roz = ro.z
    rdx = rd.x
    rdz = rd.z
    x = rox + (t * rdx)
    z = roz + (t * rdz)
    return (x * x + z * z) <= (y * y)


class Cone(HittableObject):
    __slots__ = ['closed', 'min_y', 'max_y']

    def __init__(self, transform=identity4(), material=None, closed=False, min_y=-math.inf, max_y=math.inf):
        super().__init__(transform, material)
        self.closed = closed
        self.min_y = min_y
        self.max_y = max_y

    def local_intersect(self, object_ray):
        rd = object_ray.direction
        ro = object_ray.origin
        rdx = rd.x
        rdz = rd.z
        rox = ro.x
        roz = ro.z
        roy = ro.y
        rdy = rd.y

        res = []

        if self.closed:
            t = (self.min_y - roy) / rdy
            if check_cone_cap(object_ray, t, self.min_y):
                res.append(Intersection(self, t))

            t = (self.max_y - roy) / rdy
            if check_cone_cap(object_ray, t, self.max_y):
                res.append(Intersection(self, t))

        # Intersect with the body of the cone
        a = (rdx * rdx) + (rdz * rdz) - (rdy * rdy)
        b = 2 * (rox * rdx + roz * rdz - roy * rdy)
        c = (rox * rox) + (roz * roz) - (roy * roy)

        if math.fabs(a) < EPSILON:
            # ray is parallel to one of the cone's halves
            if math.fabs(b) < EPSILON:
                # ray misses cone completely
                return res
            else:
                res.append(Intersection(self, -c/(2 * b)))
                return res

        discriminant = (b * b) - (4 * a * c)
        if discriminant < 0:
            return res

        sqrtd = math.sqrt(discriminant)
        t1 = (-b - sqrtd) / (2 * a)
        t2 = (-b + sqrtd) / (2 * a)

        y1 = roy + (t1 * rdy)
        if self.min_y < y1 < self.max_y:
            res.append(Intersection(self, t1))
        y2 = roy + (t2 * rdy)
        if self.min_y < y2 < self.max_y:
            res.append(Intersection(self, t2))

        return res


    def local_normal_at(self, object_point):
        opx = object_point.x
        opy = object_point.y
        opz = object_point.z

        dist = (opx * opx) + (opz * opz)
        if dist < (opy * opy) - EPSILON:
            # it must have intersected an end cap
            if opy >= self.max_y - EPSILON:
                return rt.Vector(0, 1, 0)
            else:
                return rt.Vector(0, -1, 0)

        normaly = math.sqrt(opx * opx + opz * opz)
        if opy > 0:
            normaly = -normaly

        return rt.Vector(opx, normaly, opz)
