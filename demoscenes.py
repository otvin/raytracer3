import rttuple
import canvas
import objects
import lights
import transformations
import world
import matrices
import materials
import math

# These demo scenes return a World object that can then be rendered.

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

    # ======================================================
    # the camera
    # ======================================================

    camera = canvas.Camera(800, 400, math.pi/3)
    c1= transformations.view_transform(rttuple.Point(-4, 2.5, -5.5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    c2 = transformations.view_transform(rttuple.Point(-4, 1.5, -5.5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    highup = transformations.view_transform(rttuple.Point(-4, 4.5, -5.5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    c3 = transformations.view_transform(rttuple.Point(-5, 1.5, -5.5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    closeup = transformations.view_transform(rttuple.Point(-3.75, 1.5, -4.5), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    closeup2 = transformations.view_transform(rttuple.Point(-4.25, 1.75, -4), rttuple.Point(0, 1, 0),
                                             rttuple.Vector(0, 1, 0))

    closeup3 = transformations.view_transform(rttuple.Point(-3.75, 1.5, -4), rttuple.Point(0, 1, 0),
                                                      rttuple.Vector(0, 1, 0))

    closeup4 = transformations.view_transform(rttuple.Point(-4, 1, -4.5), rttuple.Point(0, 1, 0),
                                              rttuple.Vector(0, 1, 0))

    camera.transform = closeup4

    # ======================================================
    # light sources
    # ======================================================

    light = lights.PointLight(rttuple.Point(-4.9, 4.9, 1.5), rttuple.Color(1, 1, 1))
    w.lights.append(light)

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

    # ======================================================
    # describe the scene
    # ======================================================


    floor = objects.Plane()
    # floor.transform = transformations.rotation_y(.31415)
    floor.material.pattern = materials.CheckersPattern(None, rttuple.Color(0, 0, 0), rttuple.Color(0.75, 0.75, 0.75))
    floor.material.ambient = 0.5
    floor.material.diffuse = 0.4
    floor.material.specular = 0.8
    floor.material.reflective = 0.1
    w.objects.append(floor)


    # ceiling
    ceiling = objects.Plane()
    ceiling.transform = transformations.translation(0, 5, 0)
    ceiling.material.pattern = materials.CheckersPattern()
    ceiling.material.pattern.color1 = rttuple.Color(0.85, 0.85, 0.85)
    ceiling.material.pattern.color2 = rttuple.Color(1.0, 1.0, 1.0)
    ceiling.material.pattern.transform = transformations.scaling(0.2, 0.2, 0.2)
    ceiling.material.ambient = 0.5
    ceiling.material.specular = 0
    w.objects.append(ceiling)


    # east wall
    eastwall = objects.Plane()
    A = transformations.rotation_y(1.5708)
    B = transformations.rotation_x(1.5708)
    C = transformations.translation(0, 3, 0)
    eastwall.material = wallmaterial
    eastwall.transform = matrices.matmul4x4(matrices.matmul4x4(A, B), C)
    w.objects.append(eastwall)


    # west wall
    westwall = objects.Plane()
    B = transformations.rotation_x(1.5708)
    C = transformations.translation(0, 3, 0)
    westwall.transform = matrices.matmul4x4(B, C)
    westwall.material = wallmaterial
    w.objects.append(westwall)

    red = objects.Sphere()
    red.transform = matrices.matmul4x4(transformations.translation(1, 1, 1), transformations.scaling(0.5, 0.5, 0.5))
    red.material.color = rttuple.Color(0.8, 0.1, 0.3)
    red.material.specular = 0
    w.objects.append(red)


    green = objects.Sphere()
    A = transformations.scaling(0.4, 0.4, 0.4)
    B = transformations.translation(1.6, 0.4, .5)
    green.transform = matrices.matmul4x4(B, A)
    green.material.color = rttuple.Color(0.1, 0.8, 0.2)
    green.material.shininess = 200
    w.objects.append(green)


    blue = objects.Sphere()
    A = transformations.scaling(0.6, 0.6, 0.6)
    B = transformations.translation(-0.1, 0.7, 3.0)
    blue.transform = matrices.matmul4x4(A, B)
    blue.material.color = rttuple.Color(0.2, 0.1, 0.8)
    blue.material.shininess = 10
    blue.material.specular = 0.4
    w.objects.append(blue)


    glassball = objects.Sphere()
    A = transformations.scaling(1.1, 1.1, 1.1)
    B = transformations.translation(-0.8, 1.1, -1.2)
    glassball.transform = matrices.matmul4x4(A, B)
    glassball.material.color = rttuple.Color(0.8, 0.8, 0.9)
    glassball.material.ambient = 0
    glassball.material.diffuse = 0.2
    glassball.material.specular = 0.9
    glassball.material.shininess = 300
    glassball.material.transparency = 0.8
    glassball.material.refractive_index = 1.57
    w.objects.append(glassball)

    return camera, w