import math
import random
import raytracer as rt


class Light:
    __slots__ = ['position', 'intensity', 'decays', 'decayfactor']

    def __init__(self, position=rt.Point(0, 0, 0), intensity=None, decays=False, decayfactor=1.0 / (4 * math.pi)):
        self.intensity = intensity or rt.Color(1, 1, 1)
        self.position = position
        # real light, the brightness decays as 1/(4 pi r^2).
        self.decays = decays
        # if you want a unit of radius to be something other than the unit of the world coordinates,
        # add the number here.  Bigger number = decays faster.  The default will have the intensity of the light be
        # at 1.0 when the light is 1.0 units away from an object.
        self.decayfactor = decayfactor

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
        if self.decays:
            dist_squared = (self.position - point).magnitudesquared()
            if dist_squared > 0:
                return 1 / (4 * math.pi * dist_squared * self.decayfactor)
            else:
                return math.inf
        else:
            return 1.0

    def position_samples(self):
        return [self.position]


class PointLight(Light):

    def __init__(self, position=rt.Point(0, 0, 0), intensity=None, decays=False, decayfactor=1.0 / (4 * math.pi)):
        super().__init__(position, intensity, decays, decayfactor)

    def intensity_at(self, world, point):
        if world.is_shadowed(point, self.position):
            return 0.0
        else:
            if self.decays:
                dist_squared = (self.position - point).magnitudesquared()
                if dist_squared > 0:
                    return 1 / (4 * math.pi * dist_squared * self.decayfactor)
                else:
                    return math.inf
            else:
                return 1.0


class AreaLight(Light):
    __slots__ = ['corner', 'uvec', 'usteps', 'vvec', 'vsteps', 'samples', 'jitter']

    def __init__(self, corner, full_uvec, usteps, full_vvec, vsteps, jitter, intensity,
                 decays=False, decayfactor=1.0 / (4 * math.pi)):
        posx = (full_uvec.x + full_vvec.x) / 2 + corner.x
        posy = (full_uvec.y + full_vvec.y) / 2 + corner.y
        posz = (full_uvec.z + full_vvec.z) / 2 + corner.z
        super().__init__(rt.Point(posx, posy, posz), intensity, decays, decayfactor)
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
        if self.decays:
            dist_squared = (self.position - point).magnitudesquared()
            if dist_squared > 0:
                return count / (self.samples * 4 * math.pi * dist_squared * self.decayfactor)
            else:
                return math.inf
        else:
            return count / self.samples

    def position_samples(self):
        ret = []
        for u in range(self.usteps):
            for v in range(self.vsteps):
                ret.append(self.point_on_light(u, v))
        return ret


class SpotLight(Light):
    __slots__ = ['__direction', '__totalwidth', '__falloffstart', '__cos_totalwidth', '__cos_falloffstart',
                 '__cos_diff']

    def __init__(self, position=rt.Point(0, 0, 0), direction=rt.Vector(0, 0, 1), totalwidth=math.pi/2,
                 falloffstart=math.pi/2, intensity=rt.Color(1, 1, 1), decays=False, decayfactor=1.0 / (4 * math.pi)):
        super().__init__(position, intensity, decays, decayfactor)
        self.direction = direction
        # init this member variable so that the computation of __cos_diff doesn't blow up
        self.__cos_falloffstart = None
        self.totalwidth = totalwidth
        self.falloffstart = falloffstart

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, d):
        self.__direction = rt.normalize(d)

    @property
    def totalwidth(self):
        return self.__totalwidth

    @totalwidth.setter
    def totalwidth(self, t):
        if t <= 0 or t > math.pi/2:
            raise ValueError('totalwidth must be greater than 0 and no greater than pi/2')
        self.__totalwidth = t
        self.__cos_totalwidth = math.cos(t/2)
        if self.__cos_falloffstart is not None:
            self.__cos_diff = self.__cos_falloffstart - self.__cos_totalwidth
        else:
            self.__cos_diff = 0

    @property
    def falloffstart(self):
        return self.__falloffstart

    @falloffstart.setter
    def falloffstart(self, t):
        if t <= 0 or t > math.pi/2:
            raise ValueError('falloffstart must be greater than 0 and no greater than pi/2')
        if t > self.__totalwidth:
            raise ValueError('falloffstart can be no greater than totalwidth')
        self.__falloffstart = t
        self.__cos_falloffstart = math.cos(t/2)
        self.__cos_diff = self.__cos_falloffstart - self.__cos_totalwidth

    def intensity_at(self, world, point):
        vec = rt.normalize(point - self.position)
        cosv = rt.dot(vec, self.direction)
        # if the cosine is greater than the falloffstart, it's full intensity.
        # if it is less than the totalwidth, it's zero
        # if it is between the two, it is proportional
        if world.is_shadowed(point, self.position):
            return 0.0
        if cosv > self.__cos_falloffstart:
            return 1.0
        if cosv < self.__cos_totalwidth:
            return 0.0
        if self.decays:
            dist_squared = (self.position - point).magnitudesquared()
            if dist_squared > 0:
                return (1.0 - ((self.__cos_falloffstart - cosv) / self.__cos_diff)) / (4 * math.pi * dist_squared * self.decayfactor)
            else:
                return math.inf
        return 1.0 - ((self.__cos_falloffstart - cosv) / self.__cos_diff)
