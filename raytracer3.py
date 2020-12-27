import time
import math
import rttuple
import canvas
import objects
import lights
import transformations
import world
import matrices
import materials
import demoscenes

def render():



    # camera = canvas.Camera(400, 200, math.pi/3)
    # camera.transform = transformations.view_transform(rttuple.Point(0, 1.5, -5), rttuple.Point(0, 1, 0),
    #                                                  rttuple.Vector(0, 1, 0))

    # w = world.World()

    camera, w = demoscenes.chap11_demo()

    timestart = time.time()
    canvas.mp_render(camera, w, 1, 6, 5)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    canvas.canvas_to_ppm('chap11d.ppm')


if __name__ == '__main__':
    render()
