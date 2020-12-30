import math
import raytracer as rt
from .lights import lighting
from .objects import EPSILON


class World:
    __slots__ = ['objects', 'lights']

    def __init__(self, objects=None, lights=None):
        if objects is None:
            self.objects = []
        else:
            self.objects = objects

        if lights is None:
            self.lights = []
        else:
            self.lights = lights

    def intersect(self, r):
        res = []
        for i in self.objects:
            res.extend(i.intersect(r))
        res.sort(key=lambda x: x.t)
        return res

    def is_shadowed(self, point):
        # TODO if we add multiple lights we need to do something here too.
        v = self.lights[0].position - point
        distance = v.magnitude()
        direction = rt.normalize(v)

        r = rt.Ray(point, direction)
        xs = self.intersect(r)
        for i in xs:
            if i.t > 0:
                # if the smallest positive hit is nearer to the light than the point, then
                # the point is in shadow.
                if i.t < distance:
                    return True
                else:
                    return False
        return False

    def shade_hit(self, hitrecord, depth):
        # TODO p.96 to support multiple lights, just iterate over the lights in the scene.
        shadowed = self.is_shadowed(hitrecord.over_point)
        surface = lighting(hitrecord.objhit.material, hitrecord.objhit, self.lights[0], hitrecord.point,
                           hitrecord.eyev, hitrecord.normalv, shadowed)
        reflected = self.reflected_color(hitrecord, depth)
        refracted = self.refracted_color(hitrecord, depth)
        material = hitrecord.objhit.material
        if material.reflective > 0 and material.transparency > 0:
            reflectance = schlick_reflectance(hitrecord)
            return surface + (reflected * reflectance) + (refracted * (1 - reflectance))
        else:
            return surface + reflected + refracted  # I don't understand how this doesn't get > 1.

    def reflected_color(self, hitrecord, depth):
        if math.isclose(hitrecord.objhit.material.reflective, 0):
            return rt.Color(0, 0, 0)
        elif depth <= 0:
            return rt.Color(0, 0, 0)
        else:
            reflect_ray = rt.Ray(hitrecord.over_point, hitrecord.reflectv)
            color = self.color_at(reflect_ray, depth-1)
            return color * hitrecord.objhit.material.reflective

    def refracted_color(self, hitrecord, depth):
        if math.isclose(hitrecord.objhit.material.transparency, 0):
            return rt.Color(0, 0, 0)
        elif depth <= 0:
            return rt.Color(0, 0, 0)

        # Snell's law
        # Find the ratio of the first index of refraction to the second.  This is
        # inverted from the definition of Snell's law.
        n_ratio = hitrecord.n1 / hitrecord.n2
        # cos(theta_i) is the same as the dot product of the two vectors, as long as they
        # are unit vectors.
        cos_thetai = rt.dot(hitrecord.eyev, hitrecord.normalv)
        # find sin(theta_t)^2 via trigonometric identity
        sin_thetat_squared = (n_ratio * n_ratio) * (1 - (cos_thetai * cos_thetai))

        # In wikipedia for Snell's law, look under "Total internal reflection
        # and critical angle.  "Snell's law seems to require in some cases (whenever the
        # angle of incidence is large enough) that the sine of the angle of refraction be
        # greater than one.  This of course is impossible, and the light in such cases is
        # completely reflected by the boundary, a phenomenon known as total internal reflection.
        if sin_thetat_squared > 1:
            return rt.Color(0, 0, 0)

        # Find cosine of thetat via trigonometric identity
        cos_thetat = math.sqrt(1.0 - sin_thetat_squared)

        # Compute the direction of the refracted ray
        direction = hitrecord.normalv * (n_ratio * cos_thetai - cos_thetat) - hitrecord.eyev * n_ratio

        # Create the refracted ray
        refract_ray = rt.Ray(hitrecord.under_point, direction)

        return self.color_at(refract_ray, depth-1) * hitrecord.objhit.material.transparency

    def color_at(self, ray, depth):
        xs = self.intersect(ray)
        for i in xs:
            if i.t > 0:
                hitrecord = prepare_computations(i, ray, xs)
                return self.shade_hit(hitrecord, depth)
        return rt.Color(0, 0, 0)  # either no intersections or no positive t intersections


class HitRecord:
    __slots__ = ['t', 'objhit', 'point', 'inside', 'eyev', 'normalv', 'reflectv', 'over_point',
                 'under_point', 'n1', 'n2']

    def __init__(self, t, objhit, point, inside, eyev, normalv, reflectv, over_point, under_point, n1, n2):
        self.t = t
        self.objhit = objhit
        self.point = point
        self.inside = inside
        self.eyev = eyev
        self.normalv = normalv
        self.reflectv = reflectv
        self.over_point = over_point
        self.under_point = under_point
        self.n1 = n1
        self.n2 = n2


def prepare_computations(i, r, xs):
    # i is an intersection
    # r is a ray
    # xs is sorted list of intersections

    containers = []  # list of objects encountered, used for refraction
    for x in xs:
        if x is i:
            if len(containers) == 0:
                # first item encountered is the hit, so we're coming in from air.
                n1 = 1.0
            else:
                n1 = containers[-1].material.refractive_index

        if containers.count(x.objhit) > 0:
            containers.remove(x.objhit)
        else:
            containers.append(x.objhit)

        if x is i:
            if len(containers) == 0:
                n2 = 1.0
            else:
                n2 = containers[-1].material.refractive_index
            break

    point = r.at(i.t)
    eyev = -r.direction
    normalv = i.objhit.normal_at(point)
    if rt.dot(normalv, eyev) < 0:
        inside = True
        normalv = -normalv
    else:
        inside = False
    over_point = point + (normalv * EPSILON)
    under_point = point - (normalv * EPSILON)
    reflectv = rt.reflect(r.direction, normalv)

    return HitRecord(i.t, i.objhit, point, inside, eyev, normalv, reflectv, over_point, under_point, n1, n2)


def schlick_reflectance(hitrecord):
    # find the cosine of the angle between the eye and normal vectors
    cos_to_use = rt.dot(hitrecord.eyev, hitrecord.normalv)

    # total internal reflection can only occur if n1 > n2
    if hitrecord.n1 > hitrecord.n2:
        n = hitrecord.n1 / hitrecord.n2
        sin_t_squared = (n * n) * (1.0 - (cos_to_use * cos_to_use))
        if sin_t_squared > 1.0:
            return 1.0  # total internal reflection

        # compute cosine of theta_t using trig identity
        # and use that when n1 > n2
        cos_to_use = math.sqrt(1.0 - sin_t_squared)

    r0 = math.pow(((hitrecord.n1 - hitrecord.n2) / (hitrecord.n1 + hitrecord.n2)), 2)
    return r0 + (1 - r0) * math.pow(1 - cos_to_use, 5)