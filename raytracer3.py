import time
import demoscenes
import raytracer as rt

def render():

    camera, w = demoscenes.chap12_demo()

    timestart = time.time()
    rt.mp_render(camera, w, 10, 6, 5)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    rt.canvas_to_ppm('chap12_demo.ppm')

if __name__ == '__main__':
    render()
