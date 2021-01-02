import time
import demoscenes
import raytracer as rt


def render():

    GETPERFCOUNTERS = False

    camera, w = demoscenes.chap15_demo(50, 50)

    timestart = time.time()
    rt.mp_render(camera, w, 1, 6, 5, GETPERFCOUNTERS)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))
    if GETPERFCOUNTERS:
        groups, objs = w.objectcount()
        print('Objects in scene: {}'.format(objs))
        print('Groups in scene: {}'.format(groups))
        print('Lights in scene: {}'.format(len(w.lights)))
        print('Rays cast into scene: {}'.format(rt.getcount_rayforpixel()))
        print('Reflection rays: {}'.format(rt.getcount_reflectionrays()))
        print('Refraction rays: {}'.format(rt.getcount_refractionrays()))
        print('Color tests: {}'.format(rt.getcount_colortests()))
        print('Intersection tests: {}'.format(rt.getcount_objintersecttests()))
        print('Intersections: {}'.format(rt.getcount_objintersections()))

    rt.canvas_to_ppm('chap15_demo2.ppm')


if __name__ == '__main__':
    render()
