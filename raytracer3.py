import time
import demoscenes
import raytracer as rt


def render():

    GETPERFCOUNTERS = False

    camera, w = demoscenes.texture_mapped_chapel()

    timestart = time.time()
    rt.mp_render(camera, w, 10, 6, 5, GETPERFCOUNTERS)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))
    if GETPERFCOUNTERS:
        groups, objs, csgs = w.objectcount()
        print('Objects in scene (excluding groups/csgs): {}'.format(objs))
        print('Groups in scene: {}'.format(groups))
        print('CSGs in scene: {}'.format(csgs))
        print('Lights in scene: {}'.format(len(w.lights)))
        print('Rays cast into scene: {}'.format(rt.getcount_rayforpixel()))
        print('Reflection rays: {}'.format(rt.getcount_reflectionrays()))
        print('Refraction rays: {}'.format(rt.getcount_refractionrays()))
        print('Color tests: {}'.format(rt.getcount_colortests()))
        print('Intersection tests: {}'.format(rt.getcount_objintersecttests()))
        print('Intersections: {}'.format(rt.getcount_objintersections()))

    rt.canvas_to_ppm('texture_mapped_chapel.ppm')


if __name__ == '__main__':
    render()
