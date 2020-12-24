import numpy as np
import time
import math
import tuple
import canvas
import objects
import lights
import random
import transformations
import world


def render():

    floor = objects.Sphere()
    floor.transform = transformations.scaling(10, 0.01, 10)
    floor.material.color = tuple.Color(1, 0.9, 0.9)
    floor.material.specular = 0

    left_wall = objects.Sphere()
    left_wall.transform = transformations.translation(0, 0, 5)
    left_wall.transform = np.matmul(left_wall.transform, transformations.rotation_y(-math.pi/4))
    left_wall.transform = np.matmul(left_wall.transform, transformations.rotation_x(math.pi/2))
    left_wall.transform = np.matmul(left_wall.transform, transformations.scaling(10, 0.01, 10))

    right_wall = objects.Sphere()
    right_wall.transform = transformations.translation(0, 0, 5)
    right_wall.transform = np.matmul(right_wall.transform, transformations.rotation_y(math.pi/4))
    right_wall.transform = np.matmul(right_wall.transform, transformations.rotation_x(math.pi/2))
    right_wall.transform = np.matmul(right_wall.transform, transformations.scaling(10, 0.01, 10))


    middle = objects.Sphere()
    middle.transform = transformations.translation(-0.5, 1, 0.5)
    middle.material.color = tuple.Color(1, .1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3

    right = objects.Sphere()
    right.transform = np.matmul(transformations.translation(1.5, 0.5, -0.5), transformations.scaling(0.5, 0.5, 0.5))
    right.material.color = tuple.Color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3

    camera = canvas.Camera(400, 200, math.pi/3)
    camera.transform = transformations.view_transform(tuple.Point(0, 1.5, -5), tuple.Point(0, 1, 0),
                                                      tuple.Vector(0, 1, 0))

    w = world.World()
    w.lights.append(lights.PointLight(tuple.Point(-10, 10, -10), tuple.Color(1, 1, 1)))
    w.objects.append(floor)
    w.objects.append(left_wall)
    w.objects.append(right_wall)
    w.objects.append(middle)
    w.objects.append(right)

    timestart = time.time()
    canvas.render(camera, w, 1)
    # canvas.mp_render(camera, w, 10, 6)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    canvas.canvas_to_ppm('chap7.ppm')


if __name__ == '__main__':
    render()
