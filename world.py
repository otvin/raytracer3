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

    def shade_hit(self, hitrecord):
        # TODO p.96 to support multiple lights, just iterate over the lights in the scene.
        shadowed = self.is_shadowed(hitrecord.over_point)
        return lights.lighting(hitrecord.objhit.material, hitrecord.objhit, self.lights[0], hitrecord.point,
                               hitrecord.eyev, hitrecord.normalv, shadowed)

    def color_at(self, ray):
        xs = self.intersect(ray)
        for i in xs:
            if i.t > 0:
                hitrecord = prepare_computations(i, ray)
                return self.shade_hit(hitrecord)
        return rttuple.Color(0, 0, 0)  # either no intersections or no positive t intersections

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


def prepare_computations(i, r):
    # i is an intersection
    # r is a ray
    objhit = i.objhit
    point = r.at(i.t)
    return objects.HitRecord(i.t, objhit, point, -r.direction, objhit.normal_at(point))


def default_world():
    s1 = objects.Sphere(matrices.identity4(), materials.Material(rttuple.Color(0.8, 1.0, 0.6), 0.1, 0.7, 0.2, 200))
    s2 = objects.Sphere()
    s2.transform = transformations.scaling(0.5, 0.5, 0.5)
    light = lights.PointLight(rttuple.Point(-10, 10, -10), rttuple.Color(1, 1, 1))
    w = World([s1, s2], [light])
    return w
