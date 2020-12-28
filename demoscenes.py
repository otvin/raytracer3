import rttuple
import canvas
import objects
import lights
import transformations
import world
import matrices
import materials
import math

# These demo scenes return a camera and a World object that can then be rendered.

def chap11_demo():
    # https://forum.raytracerchallenge.com/thread/114/refraction-results/unclear
    # ======================================================
    # refraction-bend.yml
    #
    # This file describes the scene illustrated at the start
    # of the "Transparency and Refraction" section, in
    # chapter 11 ("Reflection and Refraction") of
    # "The Ray Tracer Challenge"
    #
    # by Jamis Buck <jamis@jamisbuck.org>
    # ======================================================
    w = world.World()
    cameratransform = transformations.view_transform(rttuple.Point(-4.5, 0.85, -4), rttuple.Point(0, 0.85, 0), rttuple.Point(0, 1, 0))
    camera = canvas.Camera(600, 600, 0.5, cameratransform)

    light = lights.PointLight(rttuple.Point(-4.9, 4.9, 1.5), rttuple.Color(1, 1, 1))
    w.lights.append(light)

    floor = objects.Plane()
    floor.transform = transformations.rotation_y(0.31415)
    floor.material.pattern = materials.CheckersPattern(None, rttuple.Color(0, 0, 0), rttuple.Color(0.75, 0.75, 0.75))
    floor.material.ambient = 0.5
    floor.material.diffuse = 0.4
    floor.material.specular = 0.8
    floor.material.reflective = 0.1
    w.objects.append(floor)

    ceiling = objects.Plane()
    ceiling.transform = transformations.translation(0, 5, 0)
    ceiling.material.pattern = materials.CheckersPattern(transformations.scaling(.2, .2, .2), rttuple.Color(0.85, 0.85, 0.85), rttuple.Color(1.0, 1.0, 1.0))
    ceiling.material.ambient = 0.5
    ceiling.material.specular = 0
    w.objects.append(ceiling)

    # ======================================================
    # define some constants to avoid duplication
    # ======================================================
    wallpattern = materials.CheckersPattern()
    wallpattern.color1 = rttuple.Color(0, 0, 0)
    wallpattern.color2 = rttuple.Color(0.75, 0.75, 0.75)
    wallpattern.transform = transformations.scaling(0.5, 0.5, 0.5)
    wallmaterial = materials.Material()
    wallmaterial.pattern = wallpattern
    wallmaterial.specular = 0

    westwall = objects.Plane()
    A = transformations.rotation_y(math.pi/2)  # orient texture
    B = transformations.rotation_z(math.pi/2)  # rotate to vertical
    C = transformations.translation(-5, 0, 0)
    westwall.transform = matrices.matmul4x4(matrices.matmul4x4(C, B), A)
    westwall.material = wallmaterial
    w.objects.append(westwall)

    eastwall = objects.Plane()
    A = transformations.rotation_y(math.pi/2)  # orient texture
    B = transformations.rotation_z(math.pi/2)  # rotate to vertical
    C = transformations.translation(5, 0, 0)
    eastwall.transform = matrices.matmul4x4(matrices.matmul4x4(C, B), A)
    eastwall.material = wallmaterial
    w.objects.append(eastwall)

    northwall = objects.Plane()
    A = transformations.rotation_x(math.pi/2)  # rotate to vertical
    B = transformations.translation(0, 0, 5)
    northwall.transform = matrices.matmul4x4(B, A)
    northwall.material = wallmaterial
    w.objects.append(northwall)

    southwall = objects.Plane()
    A = transformations.rotation_x(math.pi/2)  # rotate to vertical
    B = transformations.translation(0, 0, -5)
    southwall.transform = matrices.matmul4x4(B, A)
    southwall.material = wallmaterial
    w.objects.append(southwall)

    red_backgroundball = objects.Sphere()
    red_backgroundball.transform = transformations.translation(4, 1, 4)
    red_backgroundball.material.color = rttuple.Color(0.8, 0.1, 0.3)
    red_backgroundball.material.specular = 0
    w.objects.append(red_backgroundball)
    
    green_backgroundball = objects.Sphere()
    A = transformations.scaling(0.4, 0.4, 0.4)
    B = transformations.translation(4.6, 0.4, 2.9)
    green_backgroundball.transform = matrices.matmul4x4(B, A)
    green_backgroundball.material.color = rttuple.Color(0.1, 0.8, 0.2)
    green_backgroundball.material.shininess = 200
    w.objects.append(green_backgroundball)

    blue_backgroundball = objects.Sphere()
    A = transformations.scaling(0.6, 0.6, 0.6)
    B = transformations.translation(2.6, 0.6, 4.4)
    blue_backgroundball.transform = matrices.matmul4x4(B, A)
    blue_backgroundball.material.color = rttuple.Color(0.2, 0.1, 0.8)
    blue_backgroundball.material.shininess = 10
    blue_backgroundball.material.specular = 0.4
    w.objects.append(blue_backgroundball)

    glassball = objects.Sphere()
    A = transformations.scaling(1, 1, 1)
    B = transformations.translation(0.25, 1, 0)
    glassball.transform = matrices.matmul4x4(B, A)
    glassball.material.color = rttuple.Color(0.8, 0.8, 0.9)
    glassball.material.ambient = 0
    glassball.material.diffuse = 0.2
    glassball.material.specular = 0.9
    glassball.material.shininess = 300
    glassball.material.transparency = 0.8
    glassball.material.refractive_index = 1.57
    w.objects.append(glassball)

    return camera, w
