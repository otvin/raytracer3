import math
import tuple


class Material:
    def __init__(self, color=tuple.Color(1, 1, 1), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def __eq__(self, other):
        # may only be needed for unit tests
        return self.color == other.color and math.isclose(self.ambient, other.ambient) and \
            math.isclose(self.diffuse, other.diffuse) and math.isclose(self.specular, other.specular) and \
            math.isclose(self.shininess, other.shininess)
