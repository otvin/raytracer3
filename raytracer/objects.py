import math
from copy import deepcopy
import raytracer as rt
from .matrices import identity4
from .quarticsolver import quartic_solver


class Intersection:
    __slots__ = ['objhit', 't']

    def __init__(self, objhit, t):
        self.objhit = objhit
        self.t = t


class IntersectionWithUV(Intersection):
    __slots__ = ['u', 'v']

    def __init__(self, objhit, t, u, v):
        super().__init__(objhit, t)
        self.u = u
        self.v = v


EPSILON = 0.0001
ONEMINUSEPSILON = 1 - EPSILON


class HittableObject:
    __slots__ = ['material', '__transform', 'inversetransform', '__inversetransformtranspose', 'casts_shadow',
                 'parent', 'boundingbox']

    def __init__(self, transform=None, material=None, casts_shadow=True, parent=None):
        self.transform = transform or rt.identity4()
        self.material = material or rt.Material()
        self.casts_shadow = casts_shadow
        self.parent = parent
        self.boundingbox = None

    @property
    def transform(self):
        return self.__transform

    @transform.setter
    def transform(self, trans):
        self.__transform = trans
        self.inversetransform = rt.inverse4x4(self.__transform)
        self.__inversetransformtranspose = rt.transpose4x4(self.inversetransform)

    def includes(self, obj):
        # used for CSGs.  An object always includes itself.  Overridden for ObjectGroups and CSGs
        return self is obj

    def intersect(self, r):
        # returns a list of intersections
        object_ray = rt.do_transformray(self.inversetransform, r)
        return self.local_intersect(object_ray)

    def local_intersect(self, object_ray):
        # this method should be overridden by every base class
        # ray should be converted to object space by intersect() before calling this
        return []

    def normal_at(self, point, uv_intersection=None):
        object_point = self.world_to_object(point)
        object_normal = self.local_normal_at(object_point, uv_intersection)
        world_normal = self.normal_to_world(object_normal)
        return world_normal

    def local_normal_at(self, object_point, uv_intersection=None):
        # this method should be overridden by every base class
        # point should be converted to object space by normal_at() before calling this

        # uv_intersection is ignored by every class other than SmoothTriangle
        return NotImplementedError

    def world_to_object(self, world_point):
        if self.parent is not None:
            return rt.matmul4xTuple(self.inversetransform, self.parent.world_to_object(world_point))
        else:
            return rt.matmul4xTuple(self.inversetransform, world_point)

    def normal_to_world(self, normal):
        n = rt.matmul4xTuple(self.__inversetransformtranspose, normal)
        n.w = 0
        n = rt.normalize(n)

        if self.parent is not None:
            return self.parent.normal_to_world(n)
        else:
            return n

    def bounds_of(self):
        if self.boundingbox is None:
            self.boundingbox = rt.BoundingBox(rt.Point(-1, -1, -1), rt.Point(1, 1, 1))
        return self.boundingbox

    def parent_space_bounds_of(self):
        # TODO: Cache this.  It seems constant.
        return self.bounds_of().transform(self.transform)

    def divide(self, threshold):
        pass

    # TODO - this could be done more cleanly but it works
    def push_material_to_children(self):
        # takes the material of the group and sets all children to have this material
        if isinstance(self, ObjectGroup):
            childlist = self.children
        elif isinstance(self, CSG):
            childlist = [self.left, self.right]
        else:
            childlist = []
        for child in childlist:
            child.material = deepcopy(self.material)
            if isinstance(child, ObjectGroup) or isinstance(child, CSG):
                child.push_material_to_children()


class TestShape(HittableObject):
    __slots__ = ['saved_ray']

    def __init__(self, transform=None, material=None, casts_shadow=True, parent=None):
        super().__init__(transform, material, casts_shadow, parent)
        self.saved_ray = None

    def local_intersect(self, object_ray):
        self.saved_ray = object_ray
        return []


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

    def local_normal_at(self, object_point, uv_intersection=None):
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

    def local_normal_at(self, object_point, uv_intersection=None):
        return rt.Vector(0, 1, 0)

    def bounds_of(self):
        if self.boundingbox is None:
            self.boundingbox = rt.BoundingBox(rt.Point(-math.inf, 0, -math.inf), rt.Point(math.inf, 0, math.inf))
        return self.boundingbox


def check_axis(origin, direction, axismin=-1, axismax=1):
    # helper function for cube and bounding box intersection, but doesn't rely on cube itself
    # For cubes, min and max are -1 and 1; for bounding boxes it's based on min/max of the box
    tmin_numerator = axismin - origin
    tmax_numerator = axismax - origin
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

    def local_normal_at(self, object_point, uv_intersection=None):
        abs_point = (math.fabs(object_point.x), math.fabs(object_point.y), math.fabs(object_point.z))
        maxc = max(abs_point)
        if math.isclose(maxc, abs_point[0]):
            return rt.Vector(object_point.x, 0, 0)
        elif math.isclose(maxc, abs_point[1]):
            return rt.Vector(0, object_point.y, 0)
        else:
            return rt.Vector(0, 0, object_point.z)


def check_cap(ray, t, radius_squared):
    # helper function for cylinder or cone intersection, but doesn't rely on those objects.
    # radius = 1 for cylinders, and equals abs(y) for cones, but squaring means the
    # sign of the radius doesn't matter.
    ro = ray.origin
    rd = ray.direction
    rox = ro.x
    roz = ro.z
    rdx = rd.x
    rdz = rd.z
    x = rox + (t * rdx)
    z = roz + (t * rdz)
    return (x * x + z * z) <= radius_squared


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
        if self.closed and math.fabs(rdy) > EPSILON:
            # check for intersection with lower end cap by intersecting the ray
            # with the plane at y = self.min_y
            t = (self.min_y - roy) / rdy
            if check_cap(object_ray, t, 1):
                res.append(Intersection(self, t))

            # check for intersection with upper end cap by intersecting the ray
            # with the plane at y = self.max_y
            t = (self.max_y - roy) / rdy
            if check_cap(object_ray, t, 1):
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

    def local_normal_at(self, object_point, uv_intersection=None):
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

    def bounds_of(self):
        if self.boundingbox is None:
            self.boundingbox = rt.BoundingBox(rt.Point(-1, self.min_y, -1), rt.Point(1, self.max_y, 1))
        return self.boundingbox


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

        if self.closed and math.fabs(rdy) > EPSILON:
            t = (self.min_y - roy) / rdy
            if check_cap(object_ray, t, self.min_y * self.min_y):
                res.append(Intersection(self, t))

            t = (self.max_y - roy) / rdy
            if check_cap(object_ray, t, self.max_y * self.max_y):
                res.append(Intersection(self, t))

        # Intersect with the body of the cone

        # original logic
        # a = (rdx * rdx) + (rdz * rdz) - (rdy * rdy)
        # b = 2 * (rox * rdx + roz * rdz - roy * rdy)
        # c = (rox * rox) + (roz * roz) - (roy * roy)

        # uses same "half b" trick from Sphere.local_intersect()
        a = (rdx * rdx) + (rdz * rdz) - (rdy * rdy)
        half_b = (rox * rdx + roz * rdz - roy * rdy)
        c = (rox * rox) + (roz * roz) - (roy * roy)

        if math.fabs(a) < EPSILON:
            # ray is parallel to one of the cone's halves
            if math.fabs(half_b) < EPSILON:
                # ray misses cone completely
                return res
            else:
                res.append(Intersection(self, -c/(4 * half_b)))
                return res

        discriminant = (half_b * half_b) - (a * c)
        if discriminant < 0:
            return res

        sqrtd = math.sqrt(discriminant)
        t1 = (-half_b - sqrtd) / a
        t2 = (-half_b + sqrtd) / a

        y1 = roy + (t1 * rdy)
        if self.min_y < y1 < self.max_y:
            res.append(Intersection(self, t1))
        y2 = roy + (t2 * rdy)
        if self.min_y < y2 < self.max_y:
            res.append(Intersection(self, t2))

        return res

    def local_normal_at(self, object_point, uv_intersection=None):
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

    def bounds_of(self):
        if self.boundingbox is None:
            limit = max(math.fabs(self.min_y), math.fabs(self.max_y))
            self.boundingbox = rt.BoundingBox(rt.Point(-limit, self.min_y, -limit), rt.Point(limit, self.max_y, limit))
        return self.boundingbox


class Torus(HittableObject):
    __slots__ = ['__r', '__R']

    # Torus is centered at 0, 0, 0, on the XZ plane, with major radius R and minor radius r
    def __init__(self, transform=identity4(), material=None, R=1.0, r=0.25):
        super().__init__(transform, material)
        self.R = R
        self.r = r

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, x):
        self.__r = x
        self.boundingbox = None  # force recalculation next time it is needed

    @property
    def R(self):
        return self.__R

    @R.setter
    def R(self, x):
        self.__R = x
        self.boundingbox = None  # force recalculation next time it is needed


    def bounds_of(self):
        if self.boundingbox is None:
            self.boundingbox = rt.BoundingBox(rt.Point(-self.R - self.r, -self.r, -self.R - self.r),
                                              rt.Point(self.R + self.r, self.r, self.R + self.r))
        return self.boundingbox

    def local_intersect(self, object_ray):
        # http://blog.marcinchwedczuk.pl/ray-tracing-torus
        rd = object_ray.direction
        ro = object_ray.origin
        rdx = rd.x
        rdz = rd.z
        rox = ro.x
        roz = ro.z
        roy = ro.y
        rdy = rd.y

        res = []


        # Some common subterms
        dx2 = rdx * rdx
        dy2 = rdy * rdy
        dz2 = rdz * rdz
        ox2 = rox * rox
        oy2 = roy * roy
        oz2 = roz * roz
        r2 = self.r * self.r
        R2 = self.R * self.R

        oxdx = rox * rdx
        oydy = roy * rdy
        ozdz = roz * rdz

        sum_d_squared = dx2 + dy2 + dz2
        e = ox2 + oy2 + oz2 - r2 - R2
        f = oxdx + oydy + ozdz
        four_a_squared = 4 * R2

        c4 = sum_d_squared * sum_d_squared
        c3 = 4 * sum_d_squared * f
        c2 = (2 * sum_d_squared * e) + (4 * f * f) + (four_a_squared * dy2)
        c1 = (4 * f * e) + (2 * four_a_squared * oydy)
        c0 = (e * e) - (four_a_squared * (r2 - oy2))

        roots = quartic_solver(c4, c3, c2, c1, c0)
        res = []
        for root in roots:
            res.append(Intersection(self, root))
        return res


    def local_normal_at(self, object_point, uv_intersection=None):
        # http://cosinekitty.com/raytrace/chapter13_torus.html
        # When reading through this, note that P is object_point and A (the distance from the center of the torus hole
        # to any point on the center of the solid tube is self.R.  Note later in the article, the author uses "R"
        # The final step of the math:

        # alpha = R / (sqrt (Px^2 + Py^2))
        # N = the vector from Q to P which is
        # (Px, Py, Pz) - (alpha * Px, alpha * Py, 0)
        # which then resolves to the vector
        # ((1 - alpha) * Px, ((1 - alpha) * Py, Pz)

        # Note the paper has the torus in the xy plane and my model has it in the xz plane, hence the tweak below.

        # px2 = object_point.x * object_point.x
        # pz2 = object_point.z * object_point.z
        # oneminusalpha = 1 - (self.R / math.sqrt(px2 + pz2))
        # return rt.normalize(rt.Vector(oneminusalpha * object_point.x, object_point.y, oneminusalpha * object_point.z))

        # This version of the code comes from https://github.com/marcin-chwedczuk/ray_tracing_torus_js
        # I have verified that the results are identical, and this version is ~10% faster.
        paramSquared = self.R * self.R + self.r * self.r
        x = object_point.x
        y = object_point.y
        z = object_point.z
        sumSquared = x * x + y * y + z * z
        return rt.normalize(
            rt.Vector(4 * x * (sumSquared - paramSquared), 4 * y * (sumSquared - paramSquared + 2 * self.R * self.R),
                      4 * z * (sumSquared - paramSquared))
        )


class Triangle(HittableObject):
    __slots__ = ['__p1', '__p2', '__p3', 'e1', 'e2', 'normal']

    def __init__(self, p1, p2, p3):
        super().__init__(None, None)
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3
        self.e1 = rt.Vector()
        self.e2 = rt.Vector()
        self.normal = rt.Vector()
        self.compute_edge_vectors_and_normal()

    @property
    def p1(self):
        return self.__p1

    @p1.setter
    def p1(self, p):
        self.__p1 = p
        self.compute_edge_vectors_and_normal()

    @property
    def p2(self):
        return self.__p2

    @p2.setter
    def p2(self, p):
        self.__p2 = p
        self.compute_edge_vectors_and_normal()

    @property
    def p3(self):
        return self.__p3

    @p3.setter
    def p3(self, p):
        self.__p3 = p
        self.compute_edge_vectors_and_normal()

    def compute_edge_vectors_and_normal(self):
        self.e1 = self.p2 - self.p1
        self.e2 = self.p3 - self.p1
        self.normal = rt.normalize(rt.cross(self.e2, self.e1))
        res = rt.BoundingBox()
        res.addpoint(self.p1)
        res.addpoint(self.p2)
        res.addpoint(self.p3)
        self.boundingbox = res

    def local_intersect(self, object_ray):
        # https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
        dir_cross_e2 = rt.cross(object_ray.direction, self.e2)
        det = rt.dot(self.e1, dir_cross_e2)
        if math.fabs(det) < EPSILON:
            return []

        f = 1/det
        p1_to_origin = object_ray.origin - self.p1
        u = f * rt.dot(p1_to_origin, dir_cross_e2)
        if u < 0 or u > 1:
            return []

        origin_cross_e1 = rt.cross(p1_to_origin, self.e1)
        v = f * rt.dot(object_ray.direction, origin_cross_e1)
        if v < 0 or (u + v) > 1:
            return []

        t = f * rt.dot(self.e2, origin_cross_e1)
        return [IntersectionWithUV(self, t, u, v)]

    def local_normal_at(self, object_point, uv_intersection=None):
        return self.normal

    def bounds_of(self):
        return self.boundingbox


class SmoothTriangle(Triangle):
    __slots__ = ['n1', 'n2', 'n3']

    def __init__(self, p1, p2, p3, n1, n2, n3):
        super().__init__(p1, p2, p3)
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3

    def local_normal_at(self, object_point, uv_intersection):
        return (self.n2 * uv_intersection.u) + \
               (self.n3 * uv_intersection.v) + \
               (self.n1 * (1 - uv_intersection.u - uv_intersection.v))


class ObjectGroup(HittableObject):
    __slots__ = ['children']

    def __init__(self, transform=identity4()):
        super().__init__(transform, None)
        self.children = []
        self.boundingbox = rt.BoundingBox()

    def addchild(self, obj):
        obj.parent = self
        self.children.append(obj)
        self.boundingbox += obj.parent_space_bounds_of()

    def includes(self, obj):
        for child in self.children:
            if child.includes(obj):
                return True
        return False

    def local_normal_at(self, object_point, uv_intersection=None):
        raise NotImplementedError('Group objects do not have local normals')

    def local_intersect(self, object_ray):
        if len(self.children) == 0:
            return []
        elif not self.bounds_of().intersects(object_ray):
            return []
        else:
            xs = []
            for child in self.children:
                xs.extend(child.intersect(object_ray))
            return xs

    def bounds_of(self):
        return self.boundingbox

    def partition_children(self):
        # returns two lists - objects that should go in the left child, and objects that
        # should go in the right.  Removes those objects from self.children[]
        leftbox, rightbox = self.boundingbox.split_bounds()
        to_remove = []  # if we remove while we're iterating we break the iterator
        left = []
        right = []

        for child in self.children:
            if leftbox.contains_box(child.parent_space_bounds_of()):
                to_remove.append(child)
                left.append(child)
            elif rightbox.contains_box(child.parent_space_bounds_of()):
                to_remove.append(child)
                right.append(child)

        for rem in to_remove:
            self.children.remove(rem)

        return left, right

    def make_subgroup(self, objlist):
        # takes a list of objects, adds them to a group, and adds the new group to
        # self.children
        g = ObjectGroup()
        for i in objlist:
            g.addchild(i)
        self.addchild(g)

    def divide(self, threshold):
        if len(self.children) >= threshold:
            left, right = self.partition_children()
            if len(left) > 0:
                self.make_subgroup(left)
            if len(right) > 0:
                self.make_subgroup(right)

        for i in self.children:
            i.divide(threshold)


def intersection_allowed(oper, lhit, inl, inr):
    # oper = a CSGOperation
    # lhit = true if left object (s1) is hit, false if right object (s2) is hit
    # inl = true if the intersection is inside s1
    # inr = true if the intersection is inside s2

    # Union - true if its the left object and not inside the right, or hits the right object and not inside the left.
    if oper == "union":
        return (lhit and not inr) or (not lhit and not inl)
    elif oper == "intersection":
        return (lhit and inr) or (not lhit and inl)
    else:
        return (lhit and not inr) or (not lhit and inl)


class CSG(HittableObject):
    __slots__ = ['left', 'right', 'operation']

    def __init__(self, operation, left, right):
        super().__init__()
        if operation not in ['union', 'intersection', 'difference']:
            raise ValueError('Invalid operation: {}'.format(operation))
        self.operation = operation
        self.left = left
        left.parent = self
        self.right = right
        right.parent = self

    def includes(self, obj):
        if self.left.includes(obj):
            return True
        else:
            return self.right.includes(obj)

    def filter_intersections(self, xs):
        # begin outside both objects
        inl = False
        inr = False

        result = []

        for i in xs:
            # each intersection has to be included by either left or right.  So test left, and if it's not included
            # there, it must have been included in the right.
            lhit = self.left.includes(i.objhit)
            if intersection_allowed(self.operation, lhit, inl, inr):
                result.append(i)

            # depending on which object was hit, we toggle inl or inr.  Example: we were outside of l, we then
            # intersect with l, we are now in l.
            # QUESTION: what about rays that are tangent to spheres?  We intersect but did not go in.
            if lhit:
                inl = not inl
            else:
                inr = not inr

        return result

    def local_normal_at(self, object_point, uv_intersection=None):
        return NotImplementedError

    def local_intersect(self, object_ray):
        if not self.bounds_of().intersects(object_ray):
            return []

        xs = self.left.intersect(object_ray)
        xs.extend(self.right.intersect(object_ray))
        xs.sort(key=lambda x: x.t)  # this will lead to double-sorting but otherwise the filter algorithm doesn't work.
        return self.filter_intersections(xs)

    def bounds_of(self):
        if self.boundingbox is None:
            self.boundingbox = rt.BoundingBox()
            self.boundingbox += self.left.parent_space_bounds_of()
            self.boundingbox += self.right.parent_space_bounds_of()
        return self.boundingbox

    def divide(self, threshold):
        self.left.divide(threshold)
        self.right.divide(threshold)
