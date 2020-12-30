import math
from .transformations import do_transform
from .matrices import identity4, inverse4x4
from .rttuple import Point, normalize, Ray
from .perfcounters import increment_rayforpixel

class Camera:
    __slots__ = ['hsize', 'vsize', 'field_of_view', 'aspect_ratio', 'half_width',
                 'half_height', 'pixel_size', '__transform', '__inversetransform', '__origin']

    def __init__(self, hsize=160, vsize=120, field_of_view=math.pi/2, viewtransform=identity4()):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transform = viewtransform

        half_view = math.tan(field_of_view / 2)
        self.aspect_ratio = (hsize * 1.0)/vsize
        if self.hsize > self.vsize:
            self.half_width = half_view
            self.half_height = half_view / self.aspect_ratio
        else:
            self.half_height = half_view
            self.half_width = half_view * self.aspect_ratio

        self.pixel_size = (self.half_width * 2) / self.hsize

    @property
    def transform(self):
        return self.__transform

    @transform.setter
    def transform(self, trans):
        self.__transform = trans
        self.__inversetransform = inverse4x4(self.__transform)
        self.__origin = do_transform(self.__inversetransform, Point(0, 0, 0))

    def ray_for_pixel(self, x, y, perfcount=False):
        if perfcount:
            increment_rayforpixel()

        px_center_x = (x + 0.5) * self.pixel_size
        px_center_y = (y + 0.5) * self.pixel_size

        # untransformed coords of the pixel in world space
        world_x = self.half_width - px_center_x
        world_y = self.half_height - px_center_y

        # canvas is at z = -1
        px_transform = do_transform(self.__inversetransform, Point(world_x, world_y, -1))
        direction = normalize(px_transform - self.__origin)
        return Ray(self.__origin, direction)
