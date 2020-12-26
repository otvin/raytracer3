import multiprocessing
import math
import random
import rttuple
import transformations
import matrices

# This needs to be in global space so that the mp array can be shared when we do multiprocessing.
# It means that the raytracer can only have a single canvas at a time, which from a practical perspective
# is also fine.  Bottom line - this file is not object-oriented and I'm ok with it.

GLOBALCANVAS = multiprocessing.Array('d', 300)  # init to 10x10
CANVASWIDTH = 0
CANVASHEIGHT = 0
MAXCOLORS = 255


class Camera:
    def __init__(self, hsize=160, vsize=120, field_of_view=math.pi/2, transform=matrices.identity4()):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transform = transform

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
        self.__inversetransform = matrices.inverse4x4(self.__transform)
        self.__origin = transformations.transform(self.__inversetransform, rttuple.Point(0, 0, 0))

    def ray_for_pixel(self, x, y):
        px_center_x = (x + 0.5) * self.pixel_size
        px_center_y = (y + 0.5) * self.pixel_size

        # untransformed coords of the pixel in world space
        world_x = self.half_width - px_center_x
        world_y = self.half_height - px_center_y

        # canvas is at z = -1
        px_transform = transformations.transform(self.__inversetransform, rttuple.Point(world_x, world_y, -1))
        direction = rttuple.normalize(px_transform - self.__origin)
        return rttuple.Ray(self.__origin, direction)


def clamp(x, minimum, maximum):
    if x < minimum:
        return minimum
    if x > maximum:
        return maximum
    return x


def init_canvas(width=10, height=10):
    global GLOBALCANVAS
    global CANVASHEIGHT
    global CANVASWIDTH
    # multiprocessing arrays are initially zeroed.  We do not specify a lock here because when we do write,
    # each process will write to different cells, so there is no collision risk.
    GLOBALCANVAS = multiprocessing.Array('d', width * height * 3)
    CANVASHEIGHT = height
    CANVASWIDTH = width


def write_pixel(x, y, color):
    global GLOBALCANVAS

    assert 0 <= x < CANVASWIDTH
    assert 0 <= y < CANVASHEIGHT

    startcell = (y * CANVASWIDTH * 3) + (x * 3)
    # TODO - cannot use r, g, b any more because I'm dealing with tuples not colors
    GLOBALCANVAS[startcell] = color.arr[0]
    GLOBALCANVAS[startcell + 1] = color.arr[1]
    GLOBALCANVAS[startcell + 2] = color.arr[2]


def pixel_at(x, y):
    startcell = (y * CANVASWIDTH * 3) + (x * 3)
    res = rttuple.Color(GLOBALCANVAS[startcell], GLOBALCANVAS[startcell + 1], GLOBALCANVAS[startcell + 2])
    return res


def canvas_to_ppm(filename):
    f = open(filename, "w")
    f.write("P3\n")
    f.write("{} {}\n".format(CANVASWIDTH, CANVASHEIGHT))
    f.write("255\n")

    for h in range(CANVASHEIGHT):
        for w in range(CANVASWIDTH):
            startcell = (h * CANVASWIDTH * 3) + (w * 3)

            r = GLOBALCANVAS[startcell]
            g = GLOBALCANVAS[startcell + 1]
            b = GLOBALCANVAS[startcell + 2]

            r = int((MAXCOLORS + 1) * clamp(r, 0.0, 0.999))
            g = int((MAXCOLORS + 1) * clamp(g, 0.0, 0.999))
            b = int((MAXCOLORS + 1) * clamp(b, 0.0, 0.999))
            f.write('{} {} {}\n'.format(r, g, b))
    f.close()


global MPGLOBALWORLD
global MPGLOBALCAMERA


def mp_render_rows(rowlist, numsamples, maxdepth):

    if numsamples == 1:
        for y in rowlist:
            for x in range(MPGLOBALCAMERA.hsize):
                r = MPGLOBALCAMERA.ray_for_pixel(x, y)
                write_pixel(x, y, MPGLOBALWORLD.color_at(r, maxdepth))
            print('line {} complete'.format(y))
    else:
        for y in rowlist:
            for x in range(MPGLOBALCAMERA.hsize):
                c = rttuple.Color(0, 0, 0)
                for i in range(numsamples):
                    rndx = x + random.uniform(-0.5, 0.5)
                    rndy = y + random.uniform(-0.5, 0.5)
                    r = MPGLOBALCAMERA.ray_for_pixel(rndx, rndy)
                    c += MPGLOBALWORLD.color_at(r, maxdepth)
                c = c / numsamples
                write_pixel(x, y, c)
            print('line {} complete'.format(y))


def mp_render(camera, world, numsamples=10, numprocesses=1, maxdepth=5):
    global MPGLOBALWORLD
    global MPGLOBALCAMERA
    init_canvas(camera.hsize, camera.vsize)
    MPGLOBALWORLD = world
    MPGLOBALCAMERA = camera

    rowlists = []
    for i in range(numprocesses):
        rowlists.append([])

    for i in range(camera.vsize):
        rowlists[i % numprocesses].append(i)

    procArr = []
    for s in rowlists:
        p = multiprocessing.Process(target=mp_render_rows, args=(s, numsamples, maxdepth))
        procArr.append(p)

    for p in procArr:
        p.start()

    for p in procArr:
        p.join()

