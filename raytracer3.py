import time
import demoscenes
import raytracer as rt


def render():

    GETPERFCOUNTERS = False
    ADAPTIVE = False

    camera, w = demoscenes.dof_demo()

    timestart = time.time()
    rt.mp_render(camera, w, 100, 6, 5, ADAPTIVE, GETPERFCOUNTERS)
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
        if ADAPTIVE:
            maxv = rt.save_raycount(camera.hsize, camera.vsize, 'raycount.ppm')
            print('Max rays per pixel: {}'.format(maxv))

    rt.canvas_to_ppm('dof_demo.ppm')


if __name__ == '__main__':
    render()
