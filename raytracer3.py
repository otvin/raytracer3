import time
import canvas
import demoscenes

def render():

    camera, w = demoscenes.chap11_demo()

    timestart = time.time()
    canvas.mp_render(camera, w, 10, 6, 5)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    canvas.canvas_to_ppm('chap11_demo.ppm')

if __name__ == '__main__':
    render()
