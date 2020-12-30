import math
import raytracer as rt

# These demo scenes return a camera and a World object that can then be rendered.

def chap11_demo(width, height):
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
    w = rt.World()
    cameratransform = rt.view_transform(rt.Point(-4.5, 0.85, -4), rt.Point(0, 0.85, 0), rt.Point(0, 1, 0))
    camera = rt.Camera(width, height, 0.5, cameratransform)

    light = rt.PointLight(rt.Point(-4.9, 4.9, 1.5), rt.Color(1, 1, 1))
    w.lights.append(light)

    floor = rt.Plane()
    floor.transform = rt.rotation_y(0.31415)
    floor.material.pattern = rt.CheckersPattern(None, rt.Color(0, 0, 0), rt.Color(0.75, 0.75, 0.75))
    floor.material.ambient = 0.5
    floor.material.diffuse = 0.4
    floor.material.specular = 0.8
    floor.material.reflective = 0.1
    w.objects.append(floor)

    ceiling = rt.Plane()
    ceiling.transform = rt.translation(0, 5, 0)
    ceiling.material.pattern = rt.CheckersPattern(rt.scaling(.2, .2, .2), rt.Color(0.85, 0.85, 0.85), rt.Color(1.0, 1.0, 1.0))
    ceiling.material.ambient = 0.5
    ceiling.material.specular = 0
    w.objects.append(ceiling)

    # ======================================================
    # define some constants to avoid duplication
    # ======================================================
    wallpattern = rt.CheckersPattern()
    wallpattern.color1 = rt.Color(0, 0, 0)
    wallpattern.color2 = rt.Color(0.75, 0.75, 0.75)
    wallpattern.transform = rt.scaling(0.5, 0.5, 0.5)
    wallmaterial = rt.Material()
    wallmaterial.pattern = wallpattern
    wallmaterial.specular = 0

    westwall = rt.Plane()
    A = rt.rotation_y(math.pi/2)  # orient texture
    B = rt.rotation_z(math.pi/2)  # rotate to vertical
    C = rt.translation(-5, 0, 0)
    westwall.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
    westwall.material = wallmaterial
    w.objects.append(westwall)

    eastwall = rt.Plane()
    A = rt.rotation_y(math.pi/2)  # orient texture
    B = rt.rotation_z(math.pi/2)  # rotate to vertical
    C = rt.translation(5, 0, 0)
    eastwall.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
    eastwall.material = wallmaterial
    w.objects.append(eastwall)

    northwall = rt.Plane()
    A = rt.rotation_x(math.pi/2)  # rotate to vertical
    B = rt.translation(0, 0, 5)
    northwall.transform = rt.matmul4x4(B, A)
    northwall.material = wallmaterial
    w.objects.append(northwall)

    southwall = rt.Plane()
    A = rt.rotation_x(math.pi/2)  # rotate to vertical
    B = rt.translation(0, 0, -5)
    southwall.transform = rt.matmul4x4(B, A)
    southwall.material = wallmaterial
    w.objects.append(southwall)

    red_backgroundball = rt.Sphere()
    red_backgroundball.transform = rt.translation(4, 1, 4)
    red_backgroundball.material.color = rt.Color(0.8, 0.1, 0.3)
    red_backgroundball.material.specular = 0
    w.objects.append(red_backgroundball)
    
    green_backgroundball = rt.Sphere()
    A = rt.scaling(0.4, 0.4, 0.4)
    B = rt.translation(4.6, 0.4, 2.9)
    green_backgroundball.transform = rt.matmul4x4(B, A)
    green_backgroundball.material.color = rt.Color(0.1, 0.8, 0.2)
    green_backgroundball.material.shininess = 200
    w.objects.append(green_backgroundball)

    blue_backgroundball = rt.Sphere()
    A = rt.scaling(0.6, 0.6, 0.6)
    B = rt.translation(2.6, 0.6, 4.4)
    blue_backgroundball.transform = rt.matmul4x4(B, A)
    blue_backgroundball.material.color = rt.Color(0.2, 0.1, 0.8)
    blue_backgroundball.material.shininess = 10
    blue_backgroundball.material.specular = 0.4
    w.objects.append(blue_backgroundball)

    glassball = rt.Sphere()
    A = rt.scaling(1, 1, 1)
    B = rt.translation(0.25, 1, 0)
    glassball.transform = rt.matmul4x4(B, A)
    glassball.material.color = rt.Color(0.8, 0.8, 0.9)
    glassball.material.ambient = 0
    glassball.material.diffuse = 0.2
    glassball.material.specular = 0.9
    glassball.material.shininess = 300
    glassball.material.transparency = 0.8
    glassball.material.refractive_index = 1.57
    w.objects.append(glassball)

    return camera, w
