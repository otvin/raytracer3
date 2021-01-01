import math
import raytracer as rt


class Light:
    def __init__(self):
        pass

    def lighting(self, material, obj, point, eyev, normalv, in_shadow=False):
        return rt.Color(0, 0, 0)


class PointLight(Light):
    __slots__ = ['position', 'intensity']

    def __init__(self, position=rt.Point(0, 0, 0), intensity=None):
        super().__init__()
        if intensity is None:
            self.intensity = rt.Color(1, 1, 1)
        else:
            self.intensity = intensity
        self.position = position

    def lighting(self, material, obj, point, eyev, normalv, in_shadow=False):
        # combine the surface color with the light's color/intensity

        if material.pattern is not None:
            object_point = obj.world_to_object(point)
            pattern_point = rt.matmul4xTuple(material.pattern.inversetransform, object_point)
            effective_color = material.pattern.color_at(pattern_point) * self.intensity
        else:
            effective_color = material.color * self.intensity

        # find the direction to the light source
        lightv = rt.normalize(self.position - point)

        # compute the ambient contribution
        ambient = effective_color * material.ambient

        if in_shadow:
            diffuse = rt.BLACK
            specular = rt.BLACK
        else:
            # light_dot_normal represents the cosine of the angle between the
            # light vector and the normal vector.  A negative number means the
            # light is on the other side of the surface.
            light_dot_normal = rt.dot(lightv, normalv)
            if light_dot_normal < 0:
                diffuse = rt.BLACK
                specular = rt.BLACK
            else:
                # compute the diffuse contribution
                diffuse = effective_color * material.diffuse * light_dot_normal

                # reflect_dot_eye represents the cosine of the angel between the
                # reflection vector and the eye vector.  A negative number means the
                # light reflects away from the eye
                reflectv = rt.reflect(-lightv, normalv)
                reflect_dot_eye = rt.dot(reflectv, eyev)
                if reflect_dot_eye <= 0:
                    specular = rt.BLACK
                else:
                    # compute the specular contribution
                    factor = math.pow(reflect_dot_eye, material.shininess)
                    specular = self.intensity * material.specular * factor

        return ambient + diffuse + specular
