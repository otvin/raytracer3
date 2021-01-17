import math
import random
import raytracer as rt


class Light:
    __slots__ = ['position', 'intensity']

    def __init__(self, position=rt.Point(0, 0, 0), intensity=None):
        self.intensity = intensity or rt.Color(1, 1, 1)
        self.position = position

    def lighting(self, material, obj, point, eyev, normalv, intensity_pct=1.0):
        # combine the surface color with the light's color/intensity

        if material.pattern is not None:
            object_point = obj.world_to_object(point)
            pattern_point = rt.matmul4xTuple(material.pattern.inversetransform, object_point)
            effective_color = material.pattern.color_at(pattern_point) * self.intensity
        else:
            effective_color = material.color * self.intensity

        # compute the ambient contribution
        ambient = effective_color * material.ambient

        diffuse_specular_sum = rt.Color(0, 0, 0)
        sample_list = self.position_samples()
        for pos in sample_list:
            # find the direction to the light source
            lightv = rt.normalize(pos - point)

            # light_dot_normal represents the cosine of the angle between the
            # light vector and the normal vector.  A negative number means the
            # light is on the other side of the surface.
            light_dot_normal = rt.dot(lightv, normalv)
            if light_dot_normal < 0:
                pass
            else:
                # compute the diffuse contribution
                diffuse_specular_sum += effective_color * material.diffuse * light_dot_normal * intensity_pct

                # reflect_dot_eye represents the cosine of the angel between the
                # reflection vector and the eye vector.  A negative number means the
                # light reflects away from the eye
                reflectv = rt.reflect(-lightv, normalv)
                reflect_dot_eye = rt.dot(reflectv, eyev)
                if reflect_dot_eye <= 0:
                    pass
                else:
                    # compute the specular contribution
                    factor = math.pow(reflect_dot_eye, material.shininess)
                    diffuse_specular_sum += self.intensity * material.specular * factor * intensity_pct

        return ambient + (diffuse_specular_sum / len(sample_list))

    def intensity_at(self, world, point):
        return 1.0

    def position_samples(self):
        return [self.position]


class PointLight(Light):

    def __init__(self, position=rt.Point(0, 0, 0), intensity=None):
        super().__init__(position, intensity)

    def intensity_at(self, world, point):
        if world.is_shadowed(point, self.position):
            return 0.0
        else:
            return 1.0


class AreaLight(Light):
    __slots__ = ['corner', 'uvec', 'usteps', 'vvec', 'vsteps', 'samples', 'jitter']

    def __init__(self, corner, full_uvec, usteps, full_vvec, vsteps, jitter, intensity):
        posx = (full_uvec.x + full_vvec.x) / 2 + corner.x
        posy = (full_uvec.y + full_vvec.y) / 2 + corner.y
        posz = (full_uvec.z + full_vvec.z) / 2 + corner.z
        super().__init__(rt.Point(posx, posy, posz), intensity)
        self.corner = corner
        self.uvec = full_uvec / usteps
        self.usteps = usteps
        self.vvec = full_vvec / vsteps
        self.vsteps = vsteps
        self.samples = usteps * vsteps
        self.jitter = jitter

    def point_on_light(self, u, v):
        # 0, 0 is the cell nearest the corner
        if self.jitter:
            return self.corner + (self.uvec * (u + random.random())) + (self.vvec * (v + random.random()))
        else:
            return self.corner + (self.uvec * (u + 0.5)) + (self.vvec * (v + 0.5))

    def intensity_at(self, world, point):
        count = 0
        for u in range(self.usteps):
            for v in range(self.vsteps):
                if not world.is_shadowed(point, self.point_on_light(u, v)):
                    count += 1
        return count / self.samples

    def position_samples(self):
        ret = []
        for u in range(self.usteps):
            for v in range(self.vsteps):
                ret.append(self.point_on_light(u, v))
        return ret
