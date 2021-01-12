import multiprocessing
import random
import time
from .rttuple import Color
from .camera import Camera
from .world import World


class Canvas():
    __slots__ = ['arr', 'width', 'height', 'maxcolors']

    def __init__(self, width, height, maxcolors):
        self.width = width
        self.height = height
        self.maxcolors = maxcolors
        # multiprocessing arrays are initially zeroed.  We do not specify a lock here because when we do write,
        # each process will write to different cells, so there is no collision risk.
        self.arr = multiprocessing.Array('d', 3 * width * height)

    def __getitem__(self, key):
        return self.arr[key]

    def __setitem__(self, key, value):
        self.arr[key] = value

    def write_pixel(self, x, y, color):
        assert 0 <= x < self.width
        assert 0 <= y < self.height
        startcell = (y * self.width * 3) + (x * 3)
        # TODO - cannot use r, g, b any more because I'm dealing with tuples not colors
        self.arr[startcell] = color.arr[0]
        self.arr[startcell + 1] = color.arr[1]
        self.arr[startcell + 2] = color.arr[2]


    def pixel_at(self, x, y):
        startcell = (y * self.width * 3) + (x * 3)
        res = Color(self.arr[startcell], self.arr[startcell + 1], self.arr[startcell + 2])
        return res

    def canvas_to_ppm(self, filename):
        f = open(filename, 'w')
        f.write("P3\n")
        f.write("{} {}\n".format(self.width, self.height))
        f.write("255\n")

        for h in range(self.height):
            for w in range(self.width):
                startcell = (h * self.width * 3) + (w * 3)

                r = self.arr[startcell]
                g = self.arr[startcell + 1]
                b = self.arr[startcell + 2]

                r = int((self.maxcolors + 1) * clamp(r, 0.0, 0.999))
                g = int((self.maxcolors + 1) * clamp(g, 0.0, 0.999))
                b = int((self.maxcolors + 1) * clamp(b, 0.0, 0.999))
                f.write('{} {} {}\n'.format(r, g, b))
        f.close()

    def canvas_from_ppm(self, filename):
        print('Loading {}'.format(filename))
        timestart = time.time()
        f = open(filename, 'r')
        lines = f.readlines()
        comments_removed = [i for i in lines if i[0] != '#']
        filestr = ' '.join(comments_removed)
        data = filestr.split()
        assert data[0] == 'P3'
        assert data[1].isnumeric()
        assert data[2].isnumeric()
        assert data[3].isnumeric()
        self.width = int(data[1])
        self.height = int(data[2])
        self.maxcolors = int(data[3])
        self.arr = multiprocessing.Array('d', 3 * self.width * self.height)
        for i in range(4, len(data)):
            self.arr[i-4] = int(data[i]) / self.maxcolors
        timeend = time.time()
        print('{} loaded.'.format(filename))
        print('Elapsed time: {} seconds'.format(timeend - timestart))


def clamp(x, minimum, maximum):
    if x < minimum:
        return minimum
    if x > maximum:
        return maximum
    return x


# Using these wrapper functions is a bit messy.  However, with python multiprocessing, global objects declared
# before the Process.start() can be shared.  The Canvas objects have multiprocessing.arrays as members and that seems
# to work.  What I discovered, however, is that the global objects only seem to retain state if they are accessed by
# functions in this file.  So the wrapper functions below allow me to do that.  There may be other ways, but since
# this works, I'll keep it.


GLOBALCANVAS = Canvas(10, 10, 255)
GLOBALTEXTUREPATTERNDICT = {}


def init_canvas(width=10, height=10):
    global GLOBALCANVAS
    GLOBALCANVAS = Canvas(width, height, 255)


def get_canvasdims(texturepattern=False, texturename='default'):
    if texturepattern:
        canvas = GLOBALTEXTUREPATTERNDICT[texturename]
        return canvas.width, canvas.height
    else:
        return GLOBALCANVAS.width, GLOBALCANVAS.height


def write_pixel(x, y, color):
    global GLOBALCANVAS
    GLOBALCANVAS.write_pixel(x, y, color)


def pixel_at(x, y, texturepattern=False, texturename='default'):
    if texturepattern:
        canvas = GLOBALTEXTUREPATTERNDICT[texturename]
        return canvas.pixel_at(x, y)
    else:
        return GLOBALCANVAS.pixel_at(x, y)


def canvas_to_ppm(filename):
    GLOBALCANVAS.canvas_to_ppm(filename)


def canvas_from_ppm(filename, texturename='default'):
    global GLOBALTEXTUREPATTERNDICT
    canvas = Canvas(1, 1, 255)
    canvas.canvas_from_ppm(filename)
    GLOBALTEXTUREPATTERNDICT[texturename] = canvas


MPGLOBALWORLD = World()
MPGLOBALCAMERA = Camera()
LHS_SAMPLE_LIST = []
LHS_DELTA = 0


def init_LHS_sample_list(numsamples):
    # this range is constant for every sample we do
    global LHS_SAMPLE_LIST, LHS_DELTA
    for i in range(1, numsamples + 1):
        LHS_SAMPLE_LIST.append((-0.5 + (i / (numsamples + 1))))
    LHS_DELTA = 1 / (2 + (numsamples + 1))


def LHS_samples(x, y):
    # Latin Hypercube samples

    # degenerate case:
    if len(LHS_SAMPLE_LIST) == 1:
        return [(x, y)]
    else:
        xlist = []
        ylist = []
        for i in LHS_SAMPLE_LIST:
            xlist.append(random.uniform(x + i - LHS_DELTA, x + i + LHS_DELTA))
            ylist.append(random.uniform(y + i - LHS_DELTA, y + i + LHS_DELTA))

        random.shuffle(xlist)
        random.shuffle(ylist)
        retlist = []
        for i in range(len(xlist)):
            retlist.append((xlist[i], ylist[i]))

        return retlist


def mp_render_rows(rowlist, maxdepth, perfcount=False):

    for y in rowlist:
        for x in range(MPGLOBALCAMERA.hsize):
            c = Color(0, 0, 0)
            samples = LHS_samples(x, y)
            for q in samples:
                r = MPGLOBALCAMERA.ray_for_pixel(q[0], q[1], perfcount)
                c += MPGLOBALWORLD.color_at(r, maxdepth, perfcount)
            c = c / len(samples)
            write_pixel(x, y, c)
        print('line {} complete'.format(y))


def mp_render(camera, world, numsamples=10, numprocesses=1, maxdepth=5, perfcount=False):
    global MPGLOBALWORLD
    global MPGLOBALCAMERA
    init_canvas(camera.hsize, camera.vsize)
    init_LHS_sample_list(numsamples)
    MPGLOBALWORLD = world
    MPGLOBALCAMERA = camera

    rowlists = []
    for i in range(numprocesses):
        rowlists.append([])

    for i in range(camera.vsize):
        rowlists[i % numprocesses].append(i)

    procArr = []
    for s in rowlists:
        p = multiprocessing.Process(target=mp_render_rows, args=(s, maxdepth, perfcount))
        procArr.append(p)

    for p in procArr:
        p.start()

    for p in procArr:
        p.join()
