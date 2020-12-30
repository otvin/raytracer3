import multiprocessing
import random
from .rttuple import Color
from .camera import Camera
from .world import World

# This needs to be in global space so that the mp array can be shared when we do multiprocessing.
# It means that the raytracer can only have a single canvas at a time, which from a practical perspective
# is also fine.  Bottom line - this file is not object-oriented and I'm ok with it.

GLOBALCANVAS = multiprocessing.Array('d', 300)  # init to 10x10
CANVASWIDTH = 0
CANVASHEIGHT = 0
MAXCOLORS = 255


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


def get_canvasdims():
    return CANVASWIDTH, CANVASHEIGHT


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
    res = Color(GLOBALCANVAS[startcell], GLOBALCANVAS[startcell + 1], GLOBALCANVAS[startcell + 2])
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


MPGLOBALWORLD = World()
MPGLOBALCAMERA = Camera()


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
                c = Color(0, 0, 0)
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
