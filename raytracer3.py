import time
import demoscenes
import raytracer as rt

def render():

    camera, w = demoscenes.chap11_demo(200, 200)

    timestart = time.time()
    rt.mp_render(camera, w, 10, 6, 5)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    rt.canvas_to_ppm('test.ppm')

if __name__ == '__main__':
    render()
