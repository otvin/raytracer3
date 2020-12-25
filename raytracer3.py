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


def render():

    floor = objects.Plane()
    floor.material.color = rttuple.Color(1, 0.9, 0.9)
    floor.material.specular = 0
    floor.material.pattern = materials.StripePattern()

    middle = objects.Sphere()
    middle.transform = transformations.translation(-0.5, 1, 0.5)
    middle.material.color = rttuple.Color(1, .1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    middle.material.pattern = materials.StripePattern(color2=rttuple.Color(0.5, 0.5, 0.5))
    middle.material.pattern.transform = matrices.matmul4x4(transformations.rotation_z(math.pi/2), transformations.scaling(0.1, 0.1, 0.1))

    right = objects.Sphere()
    right.transform = matrices.matmul4x4(transformations.translation(1.5, 0.5, -0.5),
                                         transformations.scaling(0.5, 0.5, 0.5))
    right.material.color = rttuple.Color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3

    left = objects.Sphere()
    left.transform = matrices.matmul4x4(transformations.translation(-1.5, 0.33, -0.75),
                                        transformations.scaling(0.33, 0.33, 0.3))
    left.material.color = rttuple.Color(0.831, 0.686, 0.216)
    left.material.diffuse = 0.9
    left.material.specular = 0.9

    camera = canvas.Camera(400, 200, math.pi/3)
    camera.transform = transformations.view_transform(rttuple.Point(0, 1.5, -5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    w = world.World()
    w.lights.append(lights.PointLight(rttuple.Point(-10, 10, -10), rttuple.Color(1, 1, 1)))
    w.objects.append(floor)
    w.objects.append(middle)
    w.objects.append(right)
    w.objects.append(left)

    timestart = time.time()
    canvas.mp_render(camera, w, 10, 6)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    canvas.canvas_to_ppm('chap10.ppm')


if __name__ == '__main__':
    render()
