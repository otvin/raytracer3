import numpy as np
import objects
import materials
import tuple
import transformations
import lights

class World:
    def __init__(self, objects=[], lights=[]):
        self.objects = objects
        self.lights = lights

    def intersect(self, r):
        res = []
        for i in self.objects:
            res.extend(i.intersect(r))
        # TODO this is a double-sort since objects.hit(intersections) also sorts
        res.sort(key=lambda x: x.t)
        return res

    def shade_hit(self, hitrecord):
        # TODO p.96 to support multiple lights, just iterate over the lights in the scene.
        return lights.lighting(hitrecord.objhit.material, self.lights[0], hitrecord.point,
                               hitrecord.eyev, hitrecord.normalv)

    def color_at(self, ray):
        xs = self.intersect(ray)
        # skipping the double-sort by not calling objects.hit().  If we need objects.hit()
        # later we have to figure something else out.
        for i in xs:
            if i.t > 0:
                hitrecord = prepare_computations(i, ray)
                return self.shade_hit(hitrecord)
        return tuple.Color(0, 0, 0)  # either no intersections or no positive t intersections


def prepare_computations(i, r):
    # i is an intersection
    # r is a ray
    objhit = i.objhit
    point = r.at(i.t)
    return objects.HitRecord(i.t, objhit, point, -r.direction, objhit.normal_at(point))


def default_world():
    s1 = objects.Sphere(np.identity(4), materials.Material(tuple.Color(0.8, 1.0, 0.6), 0.1, 0.7, 0.2, 200))
    s2 = objects.Sphere()
    s2.transform = transformations.scaling(0.5, 0.5, 0.5)
    light = lights.PointLight(tuple.Point(-10, 10, -10), tuple.Color(1, 1, 1))
    w = World([s1, s2], [light])
    return w
