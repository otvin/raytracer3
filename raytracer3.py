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



    camera = canvas.Camera(400, 200, math.pi/3)
    camera.transform = transformations.view_transform(rttuple.Point(-4, 2.5, -5.5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    w = world.World()
    l = lights.PointLight(rttuple.Point(0, 10, 0), rttuple.Color(1,1,1))
    w.lights.append(l)

    f = objects.Plane()
    f.material.pattern = materials.CheckersPattern()
    f.material.pattern.transform = transformations.scaling(0.25, 0.25, 0.25)
    w.objects.append(f)

    backwall = objects.Plane()
    backwall.material.pattern = materials.CheckersPattern()
    backwall.material.pattern.transform = transformations.scaling(0.15, 0.15, 0.15)
    backwall.transform = matrices.matmul4x4(transformations.translation(0, 0, 4), transformations.rotation_x(math.pi/2))
    w.objects.append(backwall)


    s = objects.Sphere()
    s.material.color = rttuple.Color(0.8, 0.8, 0.9)
    s.material.ambient = 0
    s.material.diffuse = 0.2
    s.material.specular = 0.9
    s.material.shininess = 300
    s.material.transparency = 0.8
    s.material.refractive_index = 1.57
    s.transform = transformations.translation(0.25, 1, 0)
    w.objects.append(s)

    backgroundball = objects.Sphere()
    backgroundball.transform = matrices.matmul4x4(transformations.scaling(0.2, 0.2, 0.2), transformations.translation(1, .5, .75))
    backgroundball.material.color = rttuple.Color(0.8, 0.1, 0.3)
    backgroundball.material.specular = 0
    w.objects.append(backgroundball)

    backgroundball2 = objects.Sphere()
    A = transformations.scaling(0.4, 0.4, 0.4)
    B = transformations.translation(-1, 0.4, 1.75)
    backgroundball2.transform = matrices.matmul4x4(A, B)
    backgroundball2.material.color = rttuple.Color(0.1, 0.8, 0.2)
    backgroundball2.material.shininess = 200
    w.objects.append(backgroundball2)





    # camera, w = demoscenes.chap11_demo()

    timestart = time.time()
    canvas.mp_render(camera, w, 10, 6, 5)
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    canvas.canvas_to_ppm('chap11f.ppm')


if __name__ == '__main__':
    render()
