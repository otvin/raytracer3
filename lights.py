import math
import rttuple
import matrices


class Light:
    def __init__(self):
        pass


class PointLight(Light):
    __slots__ = ['position', 'intensity']

    def __init__(self, position=rttuple.Point(0, 0, 0), intensity=None):
        super().__init__()
        if intensity is None:
            self.intensity = rttuple.Color(1, 1, 1)
        else:
            self.intensity = intensity
        self.position = position


def lighting(material, object, light, point, eyev, normalv, in_shadow=False):
    # combine the surface color with the light's color/intensity

    if material.pattern is not None:
        object_point = matrices.matmul4xTuple(object.inversetransform, point)
        pattern_point = matrices.matmul4xTuple(material.pattern.inversetransform, object_point)
        effective_color = material.pattern.color_at(pattern_point) * light.intensity
    else:
        effective_color = material.color * light.intensity

    # find the direction to the light source
    lightv = rttuple.normalize(light.position - point)

    # compute the ambient contribution
    ambient = effective_color * material.ambient

    if in_shadow:
        diffuse = rttuple.BLACK
        specular = rttuple.BLACK
    else:
        # light_dot_normal represents the cosine of the angle between the
        # light vector and the normal vector.  A negative number means the
        # light is on the other side of the surface.
        light_dot_normal = rttuple.dot(lightv, normalv)
        if light_dot_normal < 0:
            diffuse = rttuple.BLACK
            specular = rttuple.BLACK
        else:
            # compute the diffuse contribution
            diffuse = effective_color * material.diffuse * light_dot_normal

            # reflect_dot_eye represents the cosine of the angel between the
            # reflection vector and the eye vector.  A negative number means the
            # light reflects away from the eye
            reflectv = rttuple.reflect(-lightv, normalv)
            reflect_dot_eye = rttuple.dot(reflectv, eyev)
            if reflect_dot_eye <= 0:
                specular = rttuple.BLACK
            else:
                # compute the specular contribution
                factor = math.pow(reflect_dot_eye, material.shininess)
                specular = light.intensity * material.specular * factor

    return ambient + diffuse + specular
