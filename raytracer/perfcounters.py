import multiprocessing as mp


COUNTER_RAYFORPIXEL = mp.Value('L', 0)
COUNTER_OBJINTERSECTTESTS = mp.Value('L', 0)
COUNTER_OBJINTERSECTIONS = mp.Value('L', 0)
COUNTER_COLORTESTS = mp.Value('L', 0)
COUNTER_REFLECTIONRAYS = mp.Value('L', 0)
COUNTER_REFRACTIONRAYS = mp.Value('L', 0)
COUNTER_RAYCOUNT = mp.Array('l',1)


def increment_reflectionrays():
    global COUNTER_REFLECTIONRAYS
    with COUNTER_REFLECTIONRAYS.get_lock():
        COUNTER_REFLECTIONRAYS.value += 1


def getcount_reflectionrays():
    global COUNTER_REFLECTIONRAYS
    return COUNTER_REFLECTIONRAYS.value


def increment_refractionrays():
    global COUNTER_REFRACTIONRAYS
    with COUNTER_REFRACTIONRAYS.get_lock():
        COUNTER_REFRACTIONRAYS.value += 1


def getcount_refractionrays():
    global COUNTER_REFRACTIONRAYS
    return COUNTER_REFRACTIONRAYS.value


def increment_rayforpixel():
    global COUNTER_RAYFORPIXEL
    with COUNTER_RAYFORPIXEL.get_lock():
        COUNTER_RAYFORPIXEL.value += 1


def getcount_rayforpixel():
    global COUNTER_RAYFORPIXEL
    return COUNTER_RAYFORPIXEL.value


def increment_objintersecttests():
    global COUNTER_OBJINTERSECTTESTS
    with COUNTER_OBJINTERSECTTESTS.get_lock():
        COUNTER_OBJINTERSECTTESTS.value += 1


def getcount_objintersecttests():
    global COUNTER_OBJINTERSECTTESTS
    return COUNTER_OBJINTERSECTTESTS.value


def increment_objintersections(n):
    global COUNTER_OBJINTERSECTIONS
    with COUNTER_OBJINTERSECTIONS.get_lock():
        COUNTER_OBJINTERSECTIONS.value += n


def getcount_objintersections():
    global COUNTER_OBJINTERSECTIONS
    return COUNTER_OBJINTERSECTIONS.value


def increment_colortests():
    global COUNTER_COLORTESTS
    with COUNTER_COLORTESTS.get_lock():
        COUNTER_COLORTESTS.value += 1


def getcount_colortests():
    global COUNTER_COLORTESTS
    return COUNTER_COLORTESTS.value


def init_raycount(w, h):
    global COUNTER_RAYCOUNT
    COUNTER_RAYCOUNT = mp.Array('l', h * w)


def add_raycount(w, x, y, numrays):
    global COUNTER_RAYCOUNT
    COUNTER_RAYCOUNT[(y * w) + x] += numrays


def save_raycount(width, height, filename):
    maxv = -1
    for i in range(width * height):
        if COUNTER_RAYCOUNT[i] > maxv:
            maxv = COUNTER_RAYCOUNT[i]

    f = open(filename, 'w')
    f.write("P3\n")
    f.write("{} {}\n".format(width, height))
    f.write("255\n")

    for h in range(height):
        for w in range(width):
            val = int((COUNTER_RAYCOUNT[(h * width) + w] / maxv) * 255)
            f.write('{} {} {}\n'.format(val, val, val))
    f.close()
    return maxv