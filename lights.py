import math
import tuple


class Light:
    def __init__(self):
        pass


class PointLight(Light):
    def __init__(self, position=tuple.Point(0, 0, 0), intensity=tuple.Color(1, 1, 1)):
        super().__init__()
        self.intensity = intensity
        self.position = position


def lighting(material, light, point, eyev, normalv):
    # combine the surface color with teh light's color/intensity
    effective_color = material.color * light.intensity

    # find the direction to the light source
    lightv = tuple.normalize(light.position - point)

    # compute the ambient contribution
    ambient = effective_color * material.ambient

    # light_dot_normal represents the cosine of the angle between the
    # light vector and the normal vector.  A negative number means the
    # light is on the other side of the surface.
    light_dot_normal = tuple.dot(lightv, normalv)
    if light_dot_normal < 0:
        diffuse = tuple.BLACK
        specular = tuple.BLACK
    else:
        # compute the diffuse contribution
        diffuse = effective_color * material.diffuse * light_dot_normal

        # reflect_dot_eye represents the cosine of the angel between the
        # reflection vector and the eye vector.  A negative number means the
        # light reflects away from the eye
        reflectv = tuple.reflect(-lightv, normalv)
        reflect_dot_eye = tuple.dot(reflectv, eyev)
        if reflect_dot_eye <= 0:
            specular = tuple.BLACK
        else:
            # compute the specular contribution
            factor = math.pow(reflect_dot_eye, material.shininess)
            specular = light.intensity * material.specular * factor

    return ambient + diffuse + specular
