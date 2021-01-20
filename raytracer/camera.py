import math
from .transformations import do_transform
from .matrices import identity4, inverse4x4
from .rttuple import Point, normalize, Ray, random_in_unit_disk
from .perfcounters import increment_rayforpixel


class Camera:
    __slots__ = ['hsize', 'vsize', 'field_of_view', 'aspect_ratio', 'half_width',
                 'half_height', 'pixel_size', '__transform', '__inversetransform', '__origin',
                 '__aperture', '__lensradius', 'focal_length']

    def __init__(self, hsize=160, vsize=120, field_of_view=math.pi/2, viewtransform=identity4(), aperture=0,
                 focal_length=1):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transform = viewtransform
        self.aperture = aperture
        self.focal_length = focal_length

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

    @property
    def aperture(self):
        return self.__aperture

    @aperture.setter
    def aperture(self, ap):
        if ap < 0:
            raise ValueError('Aperture must be a positive value')
        self.__aperture = ap
        self.__lensradius = ap / 2

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

        originalray = Ray(self.__origin, direction)
        focalpoint = originalray.at(self.focal_length)

        # defocus blur a.k.a. depth of field.
        # find a random point on the aperture
        # performance - even bif self.__lensradius = 0 (no depth of field), the random_in_unit_disk() will execute.
        # since, for now, most renderings do not use depth of field, we will avoid that call unless we are using the
        # feature.
        if self.__lensradius > 0:
            aperture_point = self.__origin + (random_in_unit_disk() * self.__lensradius)
        else:
            aperture_point = self.__origin
        newdirection = normalize(focalpoint - aperture_point)

        return Ray(aperture_point, newdirection)
