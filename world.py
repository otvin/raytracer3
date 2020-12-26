import math
import objects
import materials
import rttuple
import transformations
import lights
import matrices


class World:
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
        direction = rttuple.normalize(v)

        r = rttuple.Ray(point, direction)
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
        surface = lights.lighting(hitrecord.objhit.material, hitrecord.objhit, self.lights[0], hitrecord.point,
                                  hitrecord.eyev, hitrecord.normalv, shadowed)
        reflected = self.reflected_color(hitrecord, depth)
        return surface + reflected  # I don't understand how this doesn't get > 1.


    def reflected_color(self, hitrecord, depth):
        if math.isclose(hitrecord.objhit.material.reflective, 0):
            return rttuple.Color(0, 0, 0)
        elif depth <= 0:
            return rttuple.Color(0, 0, 0)
        else:
            reflect_ray = rttuple.Ray(hitrecord.over_point, hitrecord.reflectv)
            color = self.color_at(reflect_ray, depth-1)
            return color * hitrecord.objhit.material.reflective


    def color_at(self, ray, depth):

        xs = self.intersect(ray)
        for i in xs:
            if i.t > 0:
                hitrecord = prepare_computations(i, ray)
                return self.shade_hit(hitrecord, depth)
        return rttuple.Color(0, 0, 0)  # either no intersections or no positive t intersections


class HitRecord:
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


def prepare_computations(i, r):
    # i is an intersection
    # r is a ray

    point = r.at(i.t)
    eyev = -r.direction
    normalv = i.objhit.normal_at(point)
    if rttuple.dot(normalv, eyev) < 0:
        inside = True
        normalv = -normalv
    else:
        inside = False
    over_point = point + (normalv * objects.EPSILON)
    under_point = point - (normalv * objects.EPSILON)
    reflectv = rttuple.reflect(r.direction, normalv)
    n1 = 1.0
    n2 = 1.0

    return HitRecord(i.t, i.objhit, point, inside, eyev, normalv, reflectv, over_point, under_point, n1, n2)


def default_world():
    s1 = objects.Sphere(matrices.identity4(), materials.Material(rttuple.Color(0.8, 1.0, 0.6), 0.1, 0.7, 0.2, 200))
    s2 = objects.Sphere()
    s2.transform = transformations.scaling(0.5, 0.5, 0.5)
    light = lights.PointLight(rttuple.Point(-10, 10, -10), rttuple.Color(1, 1, 1))
    w = World([s1, s2], [light])
    return w
