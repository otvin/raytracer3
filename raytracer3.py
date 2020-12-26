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
    floor.material.color = rttuple.Color(192/255, 192/255, 192/255)
    floor.material.specular = 0
    floor.material.reflective = 0.5

    middle = objects.Sphere()
    middle.transform = transformations.translation(-0.5, 1, 0.5)
    middle.material.color = rttuple.Color(1, 1, 1)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3
    middle.material.pattern = materials.CheckersPattern()
    middle.material.pattern.color1 = rttuple.Color(229/255, 114/255, 0)
    middle.material.pattern.color2 = rttuple.Color(35/255, 45/255, 75/255)
    middle.material.pattern.transform = matrices.matmul4x4(transformations.rotation_z(math.pi/2),
                                                           transformations.scaling(0.25, 0.25, 0.25))

    right = objects.Sphere()
    right.transform = matrices.matmul4x4(transformations.translation(1.5, 0.5, -0.5),
                                         transformations.scaling(0.5, 0.5, 0.5))
    right.material.color = rttuple.Color(1, 1, 1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3
    right.material.reflective = 0.2

    camera = canvas.Camera(400, 200, math.pi/3)
    camera.transform = transformations.view_transform(rttuple.Point(0, 1.5, -5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    w = world.World()
    w.lights.append(lights.PointLight(rttuple.Point(-10, 10, -10), rttuple.Color(1, 1, 1)))
    w.objects.append(floor)

    w.objects.append(middle)
    w.objects.append(right)

    timestart = time.time()
    canvas.mp_render(camera, w, 10, 6, 5)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    canvas.canvas_to_ppm('chap11.ppm')


if __name__ == '__main__':
    render()
