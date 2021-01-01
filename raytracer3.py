import time
import demoscenes
import raytracer as rt


def render():

    GETPERFCOUNTERS = False

    camera, w = demoscenes.chap11_demo()

    timestart = time.time()
    rt.mp_render(camera, w, 10, 6, 5, GETPERFCOUNTERS)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))
    if GETPERFCOUNTERS:
        print('Objects in scene: {}'.format(len(w.objects)))
        print('Lights in scene: {}'.format(len(w.lights)))
        print('Rays cast into scene: {}'.format(rt.getcount_rayforpixel()))
        print('Reflection rays: {}'.format(rt.getcount_reflectionrays()))
        print('Refraction rays: {}'.format(rt.getcount_refractionrays()))
        print('Color tests: {}'.format(rt.getcount_colortests()))
        print('Intersection tests: {}'.format(rt.getcount_objintersecttests()))
        print('Intersections: {}'.format(rt.getcount_objintersections()))

    rt.canvas_to_ppm('chap11_demo.ppm')


if __name__ == '__main__':
    render()
