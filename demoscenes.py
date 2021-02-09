from copy import deepcopy
import math
import random
import raytracer as rt


# These demo scenes return a camera and a World object that can then be rendered.


def chap11_demo(width=200, height=200):
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
    cameratransform = rt.view_transform(rt.Point(-4.5, 0.85, -4), rt.Point(0, 0.85, 0), rt.Vector(0, 1, 0))
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
    ceiling.material.pattern = rt.CheckersPattern(rt.scaling(.2, .2, .2), rt.Color(0.85, 0.85, 0.85),
                                                  rt.Color(1.0, 1.0, 1.0))
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
    westwall.transform = rt.chain_transforms(A, B, C)
    westwall.material = wallmaterial
    w.objects.append(westwall)

    eastwall = rt.Plane()
    A = rt.rotation_y(math.pi/2)  # orient texture
    B = rt.rotation_z(math.pi/2)  # rotate to vertical
    C = rt.translation(5, 0, 0)
    eastwall.transform = rt.chain_transforms(A, B, C)
    eastwall.material = wallmaterial
    w.objects.append(eastwall)

    northwall = rt.Plane()
    A = rt.rotation_x(math.pi/2)  # rotate to vertical
    B = rt.translation(0, 0, 5)
    northwall.transform = rt.chain_transforms(A, B)
    northwall.material = wallmaterial
    w.objects.append(northwall)

    southwall = rt.Plane()
    A = rt.rotation_x(math.pi/2)  # rotate to vertical
    B = rt.translation(0, 0, -5)
    southwall.transform = rt.chain_transforms(A, B)
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
    blue_backgroundball.transform = rt.chain_transforms(A, B)
    blue_backgroundball.material.color = rt.Color(0.2, 0.1, 0.8)
    blue_backgroundball.material.shininess = 10
    blue_backgroundball.material.specular = 0.4
    w.objects.append(blue_backgroundball)

    glassball = rt.Sphere()
    A = rt.scaling(1, 1, 1)
    B = rt.translation(0.25, 1, 0)
    glassball.transform = rt.chain_transforms(A, B)
    glassball.material.color = rt.Color(0.8, 0.8, 0.9)
    glassball.material.ambient = 0
    glassball.material.diffuse = 0.2
    glassball.material.specular = 0.9
    glassball.material.shininess = 300
    glassball.material.transparency = 0.8
    glassball.material.refractive_index = 1.57
    w.objects.append(glassball)

    return camera, w


def chap12_demo(width=400, height=200):
    # https://forum.raytracerchallenge.com/thread/6/tables-scene-description
    # ======================================================
    # table.yml
    #
    # This file describes the scene illustrated at the start
    # of chapter 12, "Cubes", in "The Ray Tracer Challenge"
    #
    # by Jamis Buck <jamis@jamisbuck.org>
    # ======================================================

    w = rt.World()
    cameratransform = rt.view_transform(rt.Point(8, 6, -8), rt.Point(0, 3, 0), rt.Point(0, 1, 0))
    camera = rt.Camera(width, height, 0.785, cameratransform)

    light = rt.PointLight(rt.Point(0, 6.9, -5), rt.Color(1, 1, 0.9))
    w.lights.append(light)

    floorceiling = rt.Cube()
    A = rt.translation(0, 1, 0)
    B = rt.scaling(20, 7, 20)
    floorceiling.transform = rt.chain_transforms(A, B)
    floorceiling.material.pattern = rt.CheckersPattern()
    floorceiling.material.pattern.color1 = rt.Color(0, 0, 0)
    floorceiling.material.pattern.color2 = rt.Color(0.25, 0.25, 0.25)
    floorceiling.material.pattern.transform = rt.scaling(0.07, 0.07, 0.07)
    floorceiling.ambient = 0.25
    floorceiling.diffuse = 0.7
    floorceiling.specular = 0.9
    floorceiling.shininess = 300
    floorceiling.reflective = 0.1
    w.objects.append(floorceiling)

    walls = rt.Cube()
    walls.transform = rt.scaling(10, 10, 10)
    walls.material.pattern = rt.CheckersPattern()
    walls.material.pattern.color1 = rt.Color(0.4863, 0.3765, 0.2941)
    walls.material.pattern.color2 = rt.Color(0.3725, 0.2902, 0.2275)
    walls.material.pattern.transform = rt.scaling(.05, 20, .05)
    walls.material.ambient = 0.1
    walls.material.diffuse = 0.7
    walls.material.specular = 0.9
    walls.material.shininess = 300
    walls.material.reflective = 0.1
    w.objects.append(walls)

    tabletop = rt.Cube()
    A = rt.scaling(3, 0.1, 2)
    B = rt.translation(0, 3.1, 0)
    tabletop.transform = rt.chain_transforms(A, B)
    C = rt.rotation_y(0.1)
    D = rt.scaling(0.05, 0.05, 0.05)
    patternxform = rt.chain_transforms(C, D)
    tabletoppattern = rt.StripePattern(patternxform, rt.Color(0.5529, 0.4235, 0.3255), rt.Color(0.6588, 0.5098, 0.4))
    tabletop.material.pattern = tabletoppattern
    tabletop.material.ambient = 0.1
    tabletop.material.diffuse = 0.7
    tabletop.material.specular = 0.9
    tabletop.material.shininess = 300
    tabletop.material.reflective = 0.2
    w.objects.append(tabletop)

    leg1 = rt.Cube()
    A = rt.scaling(0.1, 1.5, 0.1)
    B = rt.translation(2.7, 1.5, -1.7)
    leg1.transform = rt.chain_transforms(A, B)
    leg1.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg1.material.ambient = 0.2
    leg1.material.diffuse = 0.7
    w.objects.append(leg1)

    leg2 = rt.Cube()
    A = rt.scaling(0.1, 1.5, 0.1)
    B = rt.translation(2.7, 1.5, 1.7)
    leg2.transform = rt.chain_transforms(A, B)
    leg2.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg2.material.ambient = 0.2
    leg2.material.diffuse = 0.7
    w.objects.append(leg2)

    leg3 = rt.Cube()
    A = rt.scaling(0.1, 1.5, 0.1)
    B = rt.translation(-2.7, 1.5, -1.7)
    leg3.transform = rt.chain_transforms(A, B)
    leg3.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg3.material.ambient = 0.2
    leg3.material.diffuse = 0.7
    w.objects.append(leg3)

    leg4 = rt.Cube()
    A = rt.scaling(0.1, 1.5, 0.1)
    B = rt.translation(-2.7, 1.5, 1.7)
    leg4.transform = rt.chain_transforms(A, B)
    leg4.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg4.material.ambient = 0.2
    leg4.material.diffuse = 0.7
    w.objects.append(leg4)

    glasscube = rt.Cube()
    A = rt.scaling(0.25, 0.25, 0.25)
    B = rt.rotation_y(0.2)
    C = rt.translation(0, 3.45001, 0)
    glasscube.transform = rt.chain_transforms(A, B, C)
    glasscube.casts_shadow = False
    glasscube.material.color = rt.Color(1, 1, 0.8)
    glasscube.material.ambient = 0
    glasscube.material.diffuse = 0.3
    glasscube.material.specular = 0.9
    glasscube.material.shininess = 300
    glasscube.material.reflective = 0.7
    glasscube.material.transparency = 0.7
    glasscube.material.refractive_index = 1.5
    w.objects.append(glasscube)

    littlecube1 = rt.Cube()
    A = rt.scaling(0.15, 0.15, 0.15)
    B = rt.rotation_y(-0.4)
    C = rt.translation(1, 3.35, -0.9)
    littlecube1.transform = rt.chain_transforms(A, B, C)
    littlecube1.material.color = rt.Color(1, 0.5, 0.5)
    littlecube1.material.reflective = 0.6
    littlecube1.material.diffuse = 0.4
    w.objects.append(littlecube1)

    littlecube2 = rt.Cube()
    A = rt.scaling(0.15, 0.07, 0.15)
    B = rt.rotation_y(0.4)
    C = rt.translation(-1.5, 3.27, 0.3)
    littlecube2.transform = rt.chain_transforms(A, B, C)
    littlecube2.material.color = rt.Color(1, 1, 0.5)
    w.objects.append(littlecube2)

    littlecube3 = rt.Cube()
    A = rt.scaling(0.2, 0.05, 0.05)
    B = rt.rotation_y(0.4)
    C = rt.translation(0, 3.25, 1)
    littlecube3.transform = rt.chain_transforms(A, B, C)
    littlecube3.material.color = rt.Color(0.5, 1, 0.5)
    w.objects.append(littlecube3)

    littlecube4 = rt.Cube()
    A = rt.scaling(0.05, 0.2, 0.05)
    B = rt.rotation_y(0.8)
    C = rt.translation(-0.6, 3.4, -1)
    littlecube4.transform = rt.chain_transforms(A, B, C)
    littlecube4.material.color = rt.Color(0.5, 0.5, 1)
    w.objects.append(littlecube4)

    littlecube5 = rt.Cube()
    A = rt.scaling(0.05, 0.2, 0.05)
    B = rt.rotation_y(0.8)
    C = rt.translation(2, 3.4, 1)
    littlecube5.transform = rt.chain_transforms(A, B, C)
    littlecube5.material.color = rt.Color(0.5, 1, 1)
    w.objects.append(littlecube5)

    frame1 = rt.Cube()
    frame1.transform = rt.chain_transforms(rt.scaling(0.05, 1, 1), rt.translation(-10, 4, 1))
    frame1.material.color = rt.Color(0.7098, 0.2471, 0.2196)
    frame1.material.diffuse = 0.6
    w.objects.append(frame1)

    frame2 = rt.Cube()
    frame2.transform = rt.chain_transforms(rt.scaling(0.05, 0.4, 0.4), rt.translation(-10, 3.4, 2.7))
    frame2.material.color = rt.Color(0.2667, 0.2706, 0.6902)
    frame2.material.diffuse = 0.6
    w.objects.append(frame2)

    frame3 = rt.Cube()
    frame3.transform = rt.chain_transforms(rt.scaling(0.05, 0.4, 0.4), rt.translation(-10, 4.6, 2.7))
    frame3.material.color = rt.Color(0.3098, 0.5961, 0.3098)
    frame3.material.diffuse = 0.6
    w.objects.append(frame3)

    mirrorframe = rt.Cube()
    mirrorframe.transform = rt.chain_transforms(rt.scaling(5, 1.5, 0.05), rt.translation(-2, 3.5, 9.95))
    mirrorframe.material.color = rt.Color(0.3882, 0.2627, 0.1882)
    mirrorframe.material.diffuse = 0.7
    w.objects.append(mirrorframe)

    mirror = rt.Cube()
    mirror.transform = rt.chain_transforms(rt.scaling(4.8, 1.4, 0.06), rt.translation(-2, 3.5, 9.95))
    mirror.material.color = rt.Color(0, 0, 0)
    mirror.material.diffuse = 0
    mirror.material.ambient = 0
    mirror.material.specular = 1
    mirror.material.shininess = 300
    mirror.material.reflective = 1
    w.objects.append(mirror)

    return camera, w


def chap13_demo(width=400, height=200):
    # https://forum.raytracerchallenge.com/thread/7/cylinders-scene-description
    # ======================================================
    # cylinders.yml
    #
    # This file describes the scene illustrated at the start
    # of chapter 13, "Cylinders", in "The Ray Tracer
    # Challenge"
    #
    # by Jamis Buck <jamis@jamisbuck.org>
    # ======================================================
    w = rt.World()
    cameratransform = rt.view_transform(rt.Point(8, 3.5, -9), rt.Point(0, 0.3, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 0.314, cameratransform)

    # light = rt.PointLight(rt.Point(1, 6.9, -4.9), rt.Color(1, 1, 1))

    # point it at the concentric circles
    vec = rt.Point(1, 0, 0) - rt.Point(1, 6.9, -4.9)
    light = rt.SpotLight(rt.Point(1, 6.9, -4.9), vec, math.pi/6, math.pi/12, rt.Color(1, 1, 1))

    w.lights.append(light)

    floor = rt.Plane()
    A = rt.scaling(0.25, 0.25, 0.25)
    B = rt.rotation_y(0.3)
    floor.material.pattern = rt.CheckersPattern()
    floor.material.pattern.color1 = rt.Color(0.5, 0.5, 0.5)
    floor.material.pattern.color2 = rt.Color(0.75, 0.75, 0.75)
    floor.material.pattern.transform = rt.chain_transforms(A, B)
    floor.material.ambient = 0.2
    floor.material.diffuse = 0.9
    floor.material.specular = 0
    w.objects.append(floor)

    cyl1 = rt.Cylinder()
    cyl1.min_y = 0
    cyl1.max_y = 0.75
    cyl1.closed = True
    A = rt.scaling(0.5, 1, 0.5)
    B = rt.translation(-1, 0, 1)
    cyl1.transform = rt.chain_transforms(A, B)
    cyl1.material.color = rt.Color(0, 0, 0.6)
    cyl1.material.diffuse = 0.1
    cyl1.material.specular = 0.9
    cyl1.material.shininess = 300
    cyl1.material.reflective = 0.9
    w.objects.append(cyl1)

    # concentric cylinders

    con1 = rt.Cylinder()
    con1.min_y = 0
    con1.max_y = 0.2
    A = rt.scaling(0.8, 1, 0.8)
    B = rt.translation(1, 0, 0)
    con1.transform = rt.chain_transforms(A, B)
    con1.material.color = rt.Color(1, 1, 0.3)
    con1.material.ambient = 0.1
    con1.material.diffuse = 0.8
    con1.material.specular = 0.9
    con1.material.shininess = 300
    w.objects.append(con1)

    con2 = rt.Cylinder()
    con2.min_y = 0
    con2.max_y = 0.3
    A = rt.scaling(0.6, 1, 0.6)
    B = rt.translation(1, 0, 0)
    con2.transform = rt.chain_transforms(A, B)
    con2.material.color = rt.Color(1, 0.9, 0.4)
    con2.material.ambient = 0.1
    con2.material.diffuse = 0.8
    con2.material.specular = 0.9
    con2.material.shininess = 300
    w.objects.append(con2)

    con3 = rt.Cylinder()
    con3.min_y = 0
    con3.max_y = 0.4
    A = rt.scaling(0.4, 1, 0.4)
    B = rt.translation(1, 0, 0)
    con3.transform = rt.chain_transforms(A, B)
    con3.material.color = rt.Color(1, 0.8, 0.5)
    con3.material.ambient = 0.1
    con3.material.diffuse = 0.8
    con3.material.specular = 0.9
    con3.material.shininess = 300
    w.objects.append(con3)

    con4 = rt.Cylinder()
    con4.min_y = 0
    con4.max_y = 0.5
    A = rt.scaling(0.2, 1, 0.2)
    B = rt.translation(1, 0, 0)
    con4.transform = rt.chain_transforms(A, B)
    con4.material.color = rt.Color(1, 0.7, 0.6)
    con4.material.ambient = 0.1
    con4.material.diffuse = 0.8
    con4.material.specular = 0.9
    con4.material.shininess = 300
    w.objects.append(con4)

    # decorative cylinders
    dec1 = rt.Cylinder()
    dec1.min_y = 0
    dec1.max_y = 0.3
    dec1.closed = True
    A = rt.scaling(0.05, 1, 0.05)
    B = rt.translation(0, 0, -0.75)
    dec1.transform = rt.chain_transforms(A, B)
    dec1.material.color = rt.Color(1, 0, 0)
    dec1.material.ambient = 0.1
    dec1.material.diffuse = 0.9
    dec1.material.specular = 0.9
    dec1.material.shininess = 300
    w.objects.append(dec1)

    dec2 = rt.Cylinder()
    dec2.min_y = 0
    dec2.max_y = 0.3
    dec2.closed = True
    A = rt.scaling(0.05, 1, 0.05)
    B = rt.translation(0, 0, 1.5)
    C = rt.rotation_y(-0.15)
    D = rt.translation(0, 0, -2.25)
    dec2.transform = rt.chain_transforms(A, B, C, D)
    dec2.material.color = rt.Color(1, 1, 0)
    dec2.material.ambient = 0.1
    dec2.material.diffuse = 0.9
    dec2.material.specular = 0.9
    dec2.material.shininess = 300
    w.objects.append(dec2)

    dec3 = rt.Cylinder()
    dec3.min_y = 0
    dec3.max_y = 0.3
    dec3.closed = True
    A = rt.scaling(0.05, 1, 0.05)
    B = rt.translation(0, 0, 1.5)
    C = rt.rotation_y(-0.3)
    D = rt.translation(0, 0, -2.25)
    dec3.transform = rt.chain_transforms(A, B, C, D)
    dec3.material.color = rt.Color(0, 1, 0)
    dec3.material.ambient = 0.1
    dec3.material.diffuse = 0.9
    dec3.material.specular = 0.9
    dec3.material.shininess = 300
    w.objects.append(dec3)

    dec4 = rt.Cylinder()
    dec4.min_y = 0
    dec4.max_y = 0.3
    dec4.closed = True
    A = rt.scaling(0.05, 1, 0.05)
    B = rt.translation(0, 0, 1.5)
    C = rt.rotation_y(-0.45)
    D = rt.translation(0, 0, -2.25)
    dec4.transform = rt.chain_transforms(A, B, C, D)
    dec4.material.color = rt.Color(0, 1, 1)
    dec4.material.ambient = 0.1
    dec4.material.diffuse = 0.9
    dec4.material.specular = 0.9
    dec4.material.shininess = 300
    w.objects.append(dec4)

    # glass cylinder

    # glass = rt.Cylinder()
    # glass.min_y = 0.0001
    # glass.max_y = 0.5
    # glass.closed = True

    # I'm using a glass cube because the glass cylinder looks meh.
    glass = rt.Cube()
    A = rt.scaling(0.33, 1, 0.33)
    B = rt.translation(0, 0, -1.5)
    glass.transform = rt.chain_transforms(A, B)
    glass.material.color = rt.Color(0.25, 0, 0)
    glass.material.diffuse = 0.1
    glass.material.specular = 0.9
    glass.material.shininess = 300
    glass.material.reflective = 0.9
    glass.material.transparency = 0.9
    glass.material.refractive_index = 1.5
    w.objects.append(glass)

    return camera, w


def chap13_demo2(width=400, height=200):

    # add a cone and move the light
    camera, w = chap13_demo(width, height)
    light = rt.PointLight(rt.Point(0, 0.75, 0), rt.Color(0.5, 0.5, 0.5))
    w.lights = [light]
    w.lights.append(rt.PointLight(rt.Point(1, 6.9, -4.9), rt.Color(0.5, 0.5, 0.5)))

    cone1 = rt.Cone()
    A = rt.scaling(0.5, 0.5, 0.5)
    B = rt.translation(0.5, 0.25, 1.5)
    cone1.transform = rt.chain_transforms(A, B)
    cone1.min_y = -0.5
    cone1.max_y = 0.5
    cone1.material.color = rt.Color(0.5, 0.0, 0.5)
    cone1.material.reflective = 0.1
    cone1.material.diffuse = 0.8
    w.objects.append(cone1)

    return camera, w


# ======================================================
# These (leg, cap, and wacky) describe groups that will be reused within
# the scene. (You can think of these as functions that
# return a new instance of the given shape each time they
# are referenced.)
# ======================================================
def chap14_demo_leg(trans=rt.identity4()):
    leg = rt.ObjectGroup()

    sphere = rt.Sphere()
    A = rt.scaling(0.25, 0.25, 0.25)
    B = rt.translation(0, 0, -1)
    sphere.transform = rt.chain_transforms(A, B, trans)
    leg.addchild(sphere)

    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 1
    A = rt.scaling(0.25, 1, 0.25)
    B = rt.rotation_z(-1.5708)
    C = rt.rotation_y(-0.5236)
    D = rt.translation(0, 0, -1)
    cylinder.transform = rt.chain_transforms(A, B, C, D, trans)
    leg.addchild(cylinder)

    return leg


def chap14_demo_cap(trans=rt.identity4(), trans2=rt.identity4()):
    cap = rt.ObjectGroup()

    cone1 = rt.Cone()
    cone1.min_y = -1
    cone1.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    cone1.transform = rt.chain_transforms(A, B, trans, trans2)
    cap.addchild(cone1)

    cone2 = rt.Cone()
    cone2.min_y = -1
    cone2.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(1.0472)
    cone2.transform = rt.chain_transforms(A, B, C, trans, trans2)
    cap.addchild(cone2)

    cone3 = rt.Cone()
    cone3.min_y = -1
    cone3.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(2.0944)
    cone3.transform = rt.chain_transforms(A, B, C, trans, trans2)
    cap.addchild(cone3)

    cone4 = rt.Cone()
    cone4.min_y = -1
    cone4.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(3.1416)
    cone4.transform = rt.chain_transforms(A, B, C, trans, trans2)
    cap.addchild(cone4)

    cone5 = rt.Cone()
    cone5.min_y = -1
    cone5.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(4.1888)
    cone5.transform = rt.chain_transforms(A, B, C, trans, trans2)
    cap.addchild(cone5)

    cone6 = rt.Cone()
    cone6.min_y = -1
    cone6.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(5.236)
    cone6.transform = rt.chain_transforms(A, B, C, trans, trans2)
    cap.addchild(cone6)

    return cap


def chap14_demo_wacky():
    wacky = rt.ObjectGroup()

    wacky.addchild(chap14_demo_leg())
    leg2 = chap14_demo_leg(rt.rotation_y(1.0472))
    wacky.addchild(leg2)
    leg3 = chap14_demo_leg(rt.rotation_y(2.0944))
    wacky.addchild(leg3)
    leg4 = chap14_demo_leg(rt.rotation_y(3.1416))
    wacky.addchild(leg4)
    leg5 = chap14_demo_leg(rt.rotation_y(4.1888))
    wacky.addchild(leg5)
    leg6 = chap14_demo_leg(rt.rotation_y(5.236))
    wacky.addchild(leg6)

    cap1 = chap14_demo_cap(rt.translation(0, 1, 0))
    wacky.addchild(cap1)
    A = rt.translation(0, 1, 0)
    B = rt.rotation_x(3.1416)
    cap2 = chap14_demo_cap(A, B)
    wacky.addchild(cap2)

    return wacky


def chap14_demo(width=600, height=200):
    # Found at: https://iliathoughts.com/posts/raytracer/
    # ======================================================
    # group.yml
    #
    # This file describes the scene illustrated at the start
    # of chapter 14, "Groups", in "The Ray Tracer
    # Challenge"
    #
    # This scene description assumes:
    #
    # 1. Your ray tracer supports multiple light sources.
    #    If it does not, you can omit the extra light
    #    sources and bump up the existing light's intensity
    #    to [1, 1, 1].
    # 2. Child objects in a group inherit their default
    #    material from the parent group. If you haven't
    #    implemented this optional feature, you'll need
    #    arrange other means of texturing the child
    #    elements (or accept that all elements of the
    #    scene will be white).
    #
    # by Jamis Buck <jamis@jamisbuck.org>
    # ======================================================

    w = rt.World()
    cameratransform = rt.view_transform(rt.Point(0, 0, -9), rt.Point(0, 0, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 0.9, cameratransform)

    w.lights.append(rt.PointLight(rt.Point(10000, 10000, -10000), rt.Color(0.25, 0.25, 0.25)))
    w.lights.append(rt.PointLight(rt.Point(-10000, 10000, -10000), rt.Color(0.25, 0.25, 0.25)))
    w.lights.append(rt.PointLight(rt.Point(10000, -10000, -10000), rt.Color(0.25, 0.25, 0.25)))
    w.lights.append(rt.PointLight(rt.Point(-10000, -10000, -10000), rt.Color(0.25, 0.25, 0.25)))

    # a white backdrop
    backdrop = rt.Plane()
    A = rt.rotation_x(1.5708)
    B = rt.translation(0, 0, 100)
    backdrop.transform = rt.chain_transforms(A, B)
    backdrop.material.color = rt.Color(1, 1, 1)
    backdrop.material.ambient = 1
    backdrop.material.diffuse = 0
    backdrop.material.specular = 0
    w.objects.append(backdrop)

    wacky1 = chap14_demo_wacky()
    A = rt.rotation_y(0.1745)
    B = rt.rotation_x(0.4363)
    C = rt.translation(-2.8, 0, 0)
    wacky1.transform = rt.chain_transforms(A, B, C)
    wacky1.material.color = rt.Color(0.9, 0.2, 0.4)
    wacky1.material.ambient = 0.2
    wacky1.material.diffuse = 0.8
    wacky1.material.specular = 0.7
    wacky1.material.shininess = 20
    wacky1.push_material_to_children()
    w.objects.append(wacky1)

    wacky2 = chap14_demo_wacky()
    wacky2.transform = rt.rotation_y(0.1745)
    wacky2.material.color = rt.Color(0.2, 0.9, 0.6)
    wacky2.material.ambient = 0.2
    wacky2.material.diffuse = 0.8
    wacky2.material.specular = 0.7
    wacky2.material.shininess = 20
    wacky2.push_material_to_children()
    w.objects.append(wacky2)

    wacky3 = chap14_demo_wacky()
    A = rt.rotation_y(-0.1745)
    B = rt.rotation_x(-0.4363)
    C = rt.translation(2.8, 0, 0)
    wacky3.transform = rt.chain_transforms(A, B, C)
    wacky3.material.color = rt.Color(0.2, 0.3, 1.0)
    wacky3.material.ambient = 0.2
    wacky3.material.diffuse = 0.8
    wacky3.material.specular = 0.7
    wacky3.material.shininess = 20
    wacky3.push_material_to_children()
    w.objects.append(wacky3)

    return camera, w


def chap15_demo(width=200, height=200):

    w = rt.World()
    cameratransform = rt.view_transform(rt.Point(-3.0, 1.0, 0), rt.Point(0, 1.0, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 0.5, cameratransform)

    light = rt.PointLight(rt.Point(-4.9, 2, 3.5), rt.Color(0.5, 0.5, 0.5))
    w.lights.append(light)
    light2 = rt.PointLight(rt.Point(-4.9, 2, -3.5), rt.Color(0.5, 0.5, 0.5))
    w.lights.append(light2)

    floor = rt.Plane()
    floor.transform = rt.translation(0, -0.5, 0)
    floor.material.color = rt.Color(0.7, 0.7, 0.2)
    floor.material.reflective = 0.7
    floor.material.ambient = 0.3
    floor.material.diffuse = 0.4
    floor.material.specular = 0.8
    w.objects.append(floor)

    parser = rt.Parser()
    # parser.parse_obj_file('raytracer/test_obj_files/tetrahedron.obj')
    # parser.parse_obj_file('raytracer/test_obj_files/icosahedron.obj')
    parser.parse_obj_file('raytracer/test_obj_files/teapot-low.obj')
    g = parser.get_group_by_name('Teapot001')
    A = rt.rotation_x(-math.pi/2)
    B = rt.rotation_z(-math.pi / 2)
    C = rt.translation(2, 1, 0)
    D = rt.rotation_y(-math.pi / 10)
    g.transform = rt.chain_transforms(B, D, A, C)
    g.material.color = rt.Color(0.1, 0.5, 0.7)
    g.material.ambient = 0.3
    g.material.diffuse = 0.9
    g.material.shininess = 10
    g.material.specular = 0.4
    g.push_material_to_children()
    g.divide(10)
    w.objects.append(g)

    return camera, w


def chap16_demo(width=200, height=100):
    # Trying to translate from Jamis's OCaml at: https://github.com/jamis/rtc-ocaml/blob/master/progs/chap16.ml

    world = rt.World()

    red_material = rt.Material()
    red_material.color = rt.Color(1, 0, 0)
    red_material.ambient = 0.2

    green_material = rt.Material()
    green_material.color = rt.Color(0, 1, 0)
    green_material.ambient = 0.2

    blue_material = rt.Material()
    blue_material.color = rt.Color(0, 0, 1)
    blue_material.ambient = 0.2

    dark_mirror = rt.Material()
    dark_mirror.color = rt.Color(0, 0, 0)
    dark_mirror.ambient = 0
    dark_mirror.diffuse = 0.4
    dark_mirror.reflective = 0.5

    transparent = rt.Material()
    transparent.color = rt.Color(0, 0, 0)
    transparent.ambient = 0
    transparent.diffuse = 0
    transparent.reflective = 0
    transparent.transparency = 1
    transparent.refractive_index = 1

    room = rt.Cube()
    A = rt.translation(0, 1, 0)
    B = rt.scaling(5, 5, 5)
    room.transform = rt.chain_transforms(A, B)
    room.material.pattern = rt.CheckersPattern(rt.scaling(0.05, 0.05, 0.05), rt.Color(1, 1, 1), rt.Color(0.9, 0.9, 0.9))
    room.material.ambient = 0.1
    room.material.diffuse = 0.7
    room.material.reflective = 0.05

    left1 = rt.Cylinder()
    left1.min_y = -1
    left1.max_y = 1
    left1.closed = True
    left1.transform = rt.scaling(0.5, 1.1, 0.5)
    left1.material = deepcopy(red_material)
    left1.material.ambient = 0.1
    left1.material.diffuse = 0.5
    left1.material.reflective = 0.3

    left2 = rt.Cylinder()
    left2.min_y = -1
    left2.max_y = 1
    left2.closed = True
    A = rt.scaling(0.5, 1., 0.5)
    B = rt.rotation_x(math.pi/2)
    left2.transform = rt.matmul4x4(B, A)
    left2.material = deepcopy(green_material)
    left2.material.ambient = 0.1
    left2.material.diffuse = 0.5
    left2.material.reflective = 0.3

    right2 = rt.Cylinder()
    right2.min_y = -1
    right2.max_y = 1
    right2.closed = True
    A = rt.scaling(0.5, 1., 0.5)
    B = rt.rotation_z(math.pi / 2)
    right2.transform = rt.matmul4x4(B, A)
    right2.material = deepcopy(blue_material)
    right2.material.ambient = 0.1
    right2.material.diffuse = 0.5
    right2.material.reflective = 0.3

    right1 = rt.CSG('intersection', left2, right2)
    tricylinder = rt.CSG('intersection', left1, right1)
    A = rt.rotation_y(0.4)
    B = rt.rotation_x(-0.1)
    C = rt.rotation_z(-0.2)
    D = rt.translation(-1.5, 0.7, 0)
    tricylinder.transform = rt.chain_transforms(A, B, C, D)

    boxleft = rt.Sphere()
    boxleft.transform = rt.scaling(1.4, 1.4, 1.4)
    boxleft.material.color = rt.Color(0.1, 0.1, 0.1)
    boxleft.material.ambient = 0.2
    boxleft.material.diffuse = 0.9
    boxleft.material.specular = 1
    boxleft.material.shininess = 50

    diffleft = rt.Cube()
    diffleft.material = deepcopy(dark_mirror)

    diffright = rt.ObjectGroup()
    cylY = rt.Cylinder()
    cylY.min_y = -1
    cylY.max_y = 1
    cylY.closed = True
    cylY.transform = rt.scaling(0.5, 1.1, 0.5)
    cylY.material = deepcopy(red_material)

    cylZ = rt.Cylinder()
    cylZ.min_y = -1
    cylZ.max_y = 1
    cylZ.closed = True
    A = rt.scaling(0.5, 1.1, 0.5)
    B = rt.rotation_x(math.pi/2)
    cylZ.transform = rt.chain_transforms(A, B)
    cylZ.material = deepcopy(green_material)

    cylX = rt.Cylinder()
    cylX.min_y = -1
    cylX.max_y = 1
    cylX.closed = True
    A = rt.scaling(0.5, 1.1, 0.5)
    B = rt.rotation_z(math.pi/2)
    cylX.transform = rt.chain_transforms(A, B)
    cylX.material = deepcopy(blue_material)

    diffright.addchild(cylX)
    diffright.addchild(cylY)
    diffright.addchild(cylZ)
    diff = rt.CSG('difference', diffleft, diffright)

    box = rt.CSG('intersection', boxleft, diff)
    A = rt.translation(0, 1, 0)
    B = rt.scaling(0.5, 0.5, 0.5)
    C = rt.rotation_y(1.3)
    box.transform = rt.chain_transforms(A, B, C)

    wedge = rt.Cube()
    wedge.casts_shadow = False
    A = rt.scaling(1, 1, 0.15)
    B = rt.translation(math.sqrt(2), 0, 0)
    C = rt.rotation_y(math.pi/4)
    wedge.transform = rt.chain_transforms(A, B, C)

    ballleft = rt.Sphere()
    ballleft.material = deepcopy(red_material)

    ballright = rt.ObjectGroup()
    for i in range(12):
        w = deepcopy(wedge)
        w.transform = rt.chain_transforms(w.transform, rt.rotation_y(i * math.pi / 6))
        ballright.addchild(w)
    ball = rt.CSG('intersection', ballleft, ballright)
    A = rt.translation(0, 1, 0)
    B = rt.scaling(0.5, 0.5, 0.5)
    C = rt.rotation_y(-0.5)
    D = rt.rotation_x(-0.1)
    E = rt.rotation_z(0.1)
    F = rt.translation(1.5, 0.25, 0)
    ball.transform = rt.chain_transforms(A, B, C, D, E, F)

    light = rt.PointLight(rt.Point(-2, 5, -2), rt.Color(1, 1, 1))

    world.lights.append(light)
    world.objects.append(room)
    world.objects.append(tricylinder)
    world.objects.append(box)
    world.objects.append(ball)

    view = rt.view_transform(rt.Point(0, 2, -4.9), rt.Point(0, 0.5, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 0.9, view)

    return camera, world


def christmas_branch():
    # the length of the branch
    length = 2.0

    # the radius of the branch
    radius = 0.025

    # how many groups of needles to cover the branch
    segments = 20

    # how many needles per group (or segment)
    per_segment = 24

    # the branch itself, just a cylinder
    branch = rt.Cylinder()
    branch.min_y = 0
    branch.max_y = length
    branch.material.color = rt.Color(0.5, 0.35, 0.26)
    branch.material.ambient = 0.2
    branch.material.specular = 0
    branch.material.diffuse = 0.6

    # how much branch each segment gets
    seg_size = length / (segments - 1)

    # the radial distance, in radians, between adjacent needles in a group
    theta = 2.1 * math.pi / per_segment

    # the maximum length of each needle
    max_length = 20.0 * radius

    # the group that will contain the branch and all needles
    obj = rt.ObjectGroup()

    for y in range(segments):
        # create a subgroup for each segment of needles
        subgroup = rt.ObjectGroup()

        for i in range(per_segment):
            # each needle is a triangle
            # y_base y coordinate of the base of the triangle
            y_base = (seg_size * y) + (random.random() * seg_size)

            # y_tip is the y coordinate of the tip of the triangle
            y_tip = y_base - (random.random() * seg_size)

            # y_angle is angle (in radians) that the needle should be rotated around the branch
            y_angle = (i * theta) + (random.random() * theta)

            # how long is the needle?
            needle_length = (max_length / 2) * (1 + random.random())

            # how much is the needle offset from the center of the branch?
            ofs = radius / 2

            # the three points of the triangle that form the needle
            p1 = rt.Point(ofs, y_base, ofs)
            p2 = rt.Point(-ofs, y_base, ofs)
            p3 = rt.Point(0.0, y_tip, needle_length)

            # create, transform, and texture the needle
            tri = rt.Triangle(p1, p2, p3)
            tri.transform = rt.rotation_y(y_angle)
            tri.material.color = rt.Color(0.26, 0.36, 0.16)
            tri.material.specular = 0.1
            subgroup.addchild(tri)

        obj.addchild(subgroup)

    return obj


def christmas_demo(width=400, height=300):
    # Found at https://iliathoughts.com/posts/raytracer/
    # ======================================================
    # christmas.yml
    #
    # This file describes a scene depicting a red Christmas
    # ornament nestled among several fir branches.
    #
    # by Jamis Buck <jamis@jamisbuck.org>
    # ======================================================

    cameraview = rt.view_transform(rt.Point(0, 0, -4), rt.Point(0, 0, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 1.047, cameraview)

    world = rt.World()

    # ======================================================
    # the light sources are all coupled with physical
    # objects, so that they appear as reflections on the
    # ornament.
    # ======================================================
    light = rt.PointLight(rt.Point(-10, 10, -10), rt.Color(0.6, 0.6, 0.6))
    sphere = rt.Sphere()
    sphere.casts_shadow = False
    sphere.transform = rt.chain_transforms(rt.scaling(1.5, 1.5, 1.5), rt.translation(-10, 10, -10))
    sphere.material.color = rt.Color(1, 1, 1)
    sphere.material.ambient = 0.6
    sphere.material.diffuse = 0
    sphere.material.specular = 0
    world.lights.append(light)
    world.objects.append(sphere)

    light = rt.PointLight(rt.Point(10, 10, -10), rt.Color(0.6, 0.6, 0.6))
    sphere = rt.Sphere()
    sphere.casts_shadow = False
    sphere.transform = rt.chain_transforms(rt.scaling(1.5, 1.5, 1.5), rt.translation(10, 10, -10))
    sphere.material.color = rt.Color(1, 1, 1)
    sphere.material.ambient = 0.6
    sphere.material.diffuse = 0
    sphere.material.specular = 0
    world.lights.append(light)
    world.objects.append(sphere)

    light = rt.PointLight(rt.Point(-2, 1, -6), rt.Color(0.2, 0.1, 0.1))
    sphere = rt.Sphere()
    sphere.casts_shadow = False
    sphere.transform = rt.chain_transforms(rt.scaling(0.4, 0.4, 0.4), rt.translation(-2, 1, -6))
    sphere.material.color = rt.Color(1, 0.5, 0.5)
    sphere.material.ambient = 0.6
    sphere.material.diffuse = 0
    sphere.material.specular = 0
    world.lights.append(light)
    world.objects.append(sphere)

    light = rt.PointLight(rt.Point(-1, -2, -6), rt.Color(0.1, 0.2, 0.1))
    sphere = rt.Sphere()
    sphere.casts_shadow = False
    sphere.transform = rt.chain_transforms(rt.scaling(0.4, 0.4, 0.4), rt.translation(-1, -2, -6))
    sphere.material.color = rt.Color(0.5, 1, 0.5)
    sphere.material.ambient = 0.6
    sphere.material.diffuse = 0
    sphere.material.specular = 0
    world.lights.append(light)
    world.objects.append(sphere)

    light = rt.PointLight(rt.Point(3, -1, -6), rt.Color(0.2, 0.2, 0.2))
    sphere = rt.Sphere()
    sphere.casts_shadow = False
    sphere.transform = rt.chain_transforms(rt.scaling(0.5, 0.5, 0.5), rt.translation(3, -1, -6))
    sphere.material.color = rt.Color(1, 1, 1)
    sphere.material.ambient = 0.6
    sphere.material.diffuse = 0
    sphere.material.specular = 0
    world.lights.append(light)
    world.objects.append(sphere)

    # ======================================================
    # the scene
    # ======================================================

    # The ornament itself. Note that specular=0, because we're
    # making the ornament reflective and then putting each light
    # source inside another sphere, so that they show up as
    # reflections. The specular component of Phong shading
    # simulates this sort of reflection, so we don't need it here.

    sphere = rt.Sphere()
    sphere.material.color = rt.Color(1, 0.25, 0.25)
    sphere.material.ambient = 0
    sphere.material.specular = 0
    sphere.material.diffuse = 0.5
    sphere.material.reflective = 0.5
    world.objects.append(sphere)

    # The silver crown atop the ornament
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 1
    A = rt.scaling(0.2, 0.3, 0.2)
    B = rt.translation(0, 0.9, 0)
    C = rt.rotation_z(-0.1)
    cylinder.transform = rt.chain_transforms(A, B, C)
    cylinder.material.pattern = rt.CheckersPattern(rt.scaling(0.2, 0.2, 0.2), rt.Color(1, 1, 1),
                                                   rt.Color(0.94, 0.94, 0.94))
    cylinder.material.ambient = 0.02
    cylinder.material.diffuse = 0.7
    cylinder.material.specular = 0.8
    cylinder.material.shininess = 20
    cylinder.material.reflective = 0.05
    world.objects.append(cylinder)

    # the branches
    # WARNING: by default, each branch consists of 20 segments * 24 needles per
    #   segment, or 480 triangles. There are 11 branches, so there are
    #   5,280 triangles used by default. While bounding boxes are not necessary
    #   to render this, you will find your ray tracer works much, MUCH more quickly
    #   with them, than without them.

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_y(0.349)
    D = rt.translation(-1, -1, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_y(0.349)
    D = rt.translation(-1, 1, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_y(-0.1745)
    D = rt.translation(1, -1, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_y(-0.349)
    D = rt.translation(1, 1, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_y(-0.349)
    D = rt.translation(0.2, -1.25, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_y(0.349)
    D = rt.translation(-0.2, -1.25, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_x(0.087)
    D = rt.rotation_y(0.5236)
    E = rt.translation(-1.2, 0.1, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D, E)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_x(-0.1745)
    D = rt.rotation_y(0.5236)
    E = rt.translation(-1.2, -0.35, 0.5)
    fir_branch.transform = rt.chain_transforms(A, B, C, D, E)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_x(0.087)
    D = rt.rotation_y(-0.5236)
    E = rt.translation(-0.2, 1.5, 0.25)
    fir_branch.transform = rt.chain_transforms(A, B, C, D, E)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_x(-0.087)
    D = rt.rotation_y(-0.5236)
    E = rt.translation(1.3, 0.4, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D, E)
    world.objects.append(fir_branch)

    fir_branch = christmas_branch()
    A = rt.translation(0, -0.5, 0)
    B = rt.rotation_x(-1.5708)
    C = rt.rotation_x(0.087)
    D = rt.rotation_y(-0.1745)
    E = rt.translation(1.5, -0.4, 0)
    fir_branch.transform = rt.chain_transforms(A, B, C, D, E)
    world.objects.append(fir_branch)

    for i in world.objects:
        i.divide(7)

    return camera, world


def die_body(material):
    cube = rt.Cube()
    cube.material = material
    sphere = rt.Sphere()
    sphere.material = material
    sphere.transform = rt.scaling(1.5, 1.5, 1.5)
    return rt.CSG('intersection', cube, sphere)


def die_point(i, j, material):
    sphere = rt.Sphere()
    sphere.material = material
    sphere.transform = rt.chain_transforms(rt.scaling(0.2, 0.1, 0.2), rt.translation(0.5 * i, 1, 0.5 * j))
    return sphere


def die_side(side_num, material):
    ijlist = []
    if side_num == 1:
        ijlist.append((0, 0))
    elif side_num == 2:
        ijlist.extend([(-0.8, -0.8), (0.8, 0.8)])
    elif side_num == 3:
        ijlist.extend([(0, 0), (-1, -1), (1, 1)])
    elif side_num == 4:
        ijlist.extend([(-0.8, -0.8), (-0.8, 0.8), (0.8, -0.8), (0.8, 0.8)])
    elif side_num == 5:
        ijlist.extend([(0, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)])
    elif side_num == 6:
        ijlist.extend([(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)])
    else:
        raise ValueError('invalid die side: {}'.format(side_num))

    ret = rt.ObjectGroup()
    for ij in ijlist:
        ret.addchild(die_point(ij[0], ij[1], material))
    return ret


def die(material1, material2):
    body = die_body(material1)
    side1 = die_side(1, material2)
    side2 = die_side(2, material2)
    side3 = die_side(3, material2)
    side4 = die_side(4, material2)
    side5 = die_side(5, material2)
    side6 = die_side(6, material2)

    side2.transform = rt.rotation_x(math.pi/2)
    side3.transform = rt.rotation_z(math.pi/2)
    side4.transform = rt.rotation_z(-math.pi/2)
    side5.transform = rt.rotation_x(-math.pi/2)
    side6.transform = rt.scaling(1, -1, 1)

    body = rt.CSG('difference', body, side1)
    body = rt.CSG('difference', body, side6)
    body = rt.CSG('difference', body, side2)
    body = rt.CSG('difference', body, side5)
    body = rt.CSG('difference', body, side3)
    body = rt.CSG('difference', body, side4)

    return body


def from_hsv(hue, saturation, value):
    # this doesn't look like the demo is using true hsv, so I'm using their algorithm to convert
    hue = hue % 360
    h = math.floor((hue / 60.0))
    f = (hue / 60) - h
    p = value * (1.0 - saturation)
    q = value * (1.0 - (saturation * f))
    t = value * (1.0 - (saturation * (1.0 - f)))
    if h == 1:
        return rt.Color(q, value, p)
    elif h == 2:
        return rt.Color(p, value, t)
    elif h == 3:
        return rt.Color(p, q, value)
    elif h == 4:
        return rt.Color(t, p, value)
    elif h == 5:
        return rt.Color(value, p, q)
    else:
        return rt.Color(value, t, p)


def dice_demo(width=900, height=450):
    # Translated from Rust.
    # found at: https://github.com/mbillingr/raytracing/blob/master/rust/examples/chapter-16.rs

    viewtransform = rt.view_transform(rt.Point(0, 0, -3), rt.Point(0, 0, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi/3, viewtransform)

    world = rt.World()
    light = rt.AreaLight(rt.Point(-8, 8, -6), rt.Vector(2, 0, 0), 4, rt.Vector(0, 0, 2), 4, True, rt.Color(1, 1, 1))
    world.lights.append(light)

    floor_material = rt.Material()
    floor_material.pattern = rt.CheckersPattern(rt.scaling(0.1, 0.1, 0.1), rt.Color(0.75, 0.75, 0.75),
                                                rt.Color(0.9, 0.9, 0.9))
    floor_material.diffuse = 0.5
    floor_material.specular = 0

    floor = rt.Plane()
    floor.material = floor_material
    floor.transform = rt.chain_transforms(rt.rotation_x(math.pi/2), rt.translation(0, 0, 2))
    world.objects.append(floor)

    glass = rt.Material()
    glass.color = rt.Color(0, 0, 0)
    glass.diffuse = 0
    glass.specular = 0.9
    glass.shininess = 500
    glass.reflective = 1.0
    glass.transparency = 1.0
    glass.refractive_index = 1.5

    a = rt.Sphere()
    a.material = glass
    a.transform = rt.translation(0, 0, 0.8)
    b = rt.Sphere()
    b.material = glass
    b.transform = rt.translation(0, 0, -0.8)
    lens = rt.CSG('intersection', a, b)
    lens.casts_shadow = False
    world.objects.append(lens)

    dices = rt.ObjectGroup()
    for i in range(-8, 9):
        for j in range(-4, 5):
            hue = random.randint(0, 360)
            mat1 = rt.Material()
            mat1.color = from_hsv(hue, 0.8, 1.0)
            mat1.diffuse = 1.0
            mat2 = rt.Material()
            mat2.color = from_hsv(hue + 180, 0.8, 1.0)
            mat2.diffuse = 1.0
            size = random.uniform(0.05, 0.1)
            pos_x = 0.4 * i + random.uniform(-0.1, 0.1)
            pos_y = 0.4 * j + random.uniform(-0.1, 0.1)
            rotay = random.uniform(0, math.pi * 2)
            rotax = random.uniform(0, math.pi * 2)
            rotaz = random.uniform(0, math.pi * 2)

            mydie = die(mat1, mat2)
            mydie.transform = rt.chain_transforms(rt.scaling(size, size, size),
                                                  rt.rotation_z(rotaz),
                                                  rt.rotation_y(rotay),
                                                  rt.rotation_x(rotax),
                                                  rt.translation(pos_x, pos_y, 1.8))

            dices.addchild(mydie)

    dices.divide(7)
    world.objects.append(dices)

    return camera, world


def texture_mapping_cubetest(width=800, height=400):
    world = rt.World()
    cameratransform = rt.view_transform(rt.Point(0, 0, -20), rt.Point(0, 0, 0), rt.Point(0, 1, 0))
    camera = rt.Camera(width, height, 0.8, cameratransform)

    light = rt.PointLight(rt.Point(0, 100, -100), rt.Color(0.25, 0.25, 0.25))
    world.lights.append(light)
    light = rt.PointLight(rt.Point(0, -100, -100), rt.Color(0.25, 0.25, 0.25))
    world.lights.append(light)
    light = rt.PointLight(rt.Point(-100, 0, -100), rt.Color(0.25, 0.25, 0.25))
    world.lights.append(light)
    light = rt.PointLight(rt.Point(100, 0, -100), rt.Color(0.25, 0.25, 0.25))
    world.lights.append(light)

    cube = rt.Cube()
    cube.material.pattern = rt.CubeMap()
    cube.material.pattern.setupdemo()
    cube.material.ambient = 0.2
    cube.material.specular = 0
    cube.material.diffuse = 0.8

    c1 = deepcopy(cube)
    c1.transform = rt.chain_transforms(rt.rotation_y(0.7854), rt.rotation_x(0.7854), rt.translation(-6, 2, 0))
    world.objects.append(c1)

    c2 = deepcopy(cube)
    c2.transform = rt.chain_transforms(rt.rotation_y(2.3562), rt.rotation_x(0.7854), rt.translation(-2, 2, 0))
    world.objects.append(c2)

    c3 = deepcopy(cube)
    c3.transform = rt.chain_transforms(rt.rotation_y(3.927), rt.rotation_x(0.7854), rt.translation(2, 2, 0))
    world.objects.append(c3)

    c4 = deepcopy(cube)
    c4.transform = rt.chain_transforms(rt.rotation_y(5.4978), rt.rotation_x(0.7854), rt.translation(6, 2, 0))
    world.objects.append(c4)

    c5 = deepcopy(cube)
    c5.transform = rt.chain_transforms(rt.rotation_y(0.7854), rt.rotation_x(-0.7854), rt.translation(-6, -2, 0))
    world.objects.append(c5)

    c6 = deepcopy(cube)
    c6.transform = rt.chain_transforms(rt.rotation_y(2.3562), rt.rotation_x(-0.7854), rt.translation(-2, -2, 0))
    world.objects.append(c6)

    c7 = deepcopy(cube)
    c7.transform = rt.chain_transforms(rt.rotation_y(3.927), rt.rotation_x(-0.7854), rt.translation(2, -2, 0))
    world.objects.append(c7)

    c8 = deepcopy(cube)
    c8.transform = rt.chain_transforms(rt.rotation_y(5.4978), rt.rotation_x(-0.7854), rt.translation(6, -2, 0))
    world.objects.append(c8)

    return camera, world


def texture_mapped_earth(width=800, height=400):
    cameratransform = rt.view_transform(rt.Point(1, 2, -10), rt.Point(0, 1.1, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 0.8, cameratransform)

    world = rt.World()
    light = rt.PointLight(rt.Point(-100, 100, -100), rt.Color(1, 1, 1))
    world.lights.append(light)

    plane = rt.Plane()
    plane.material.color = rt.Color(1, 1, 1)
    plane.material.diffuse = 0.1
    plane.material.ambient = 0
    plane.material.specular = 0
    plane.material.reflective = 0.4
    world.objects.append(plane)

    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 0.1
    cylinder.closed = True
    cylinder.material.color = rt.Color(1, 1, 1)
    cylinder.material.diffuse = 0.2
    cylinder.material.specular = 0
    cylinder.material.ambient = 0
    cylinder.material.reflective = 0.1
    world.objects.append(cylinder)

    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.rotation_y(1.9), rt.translation(0, 1.1, 0))
    sphere.material.diffuse = 0.9
    sphere.material.specular = 0.1
    sphere.material.shininess = 10
    sphere.material.ambient = 0.1
    # the earth image map is from
    # http://planetpixelemporium.com/earth.html (see "color map")
    #
    # converted from JPG to PPM via ImageMagick with:
    # $ convert earthmap1k.jpg -compress none earthmap1k.ppm
    sphere.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/earthmap1k.ppm', rt.spherical_map)
    world.objects.append(sphere)

    return camera, world


def texture_mapped_chapel(width=800, height=400):

    cameratransform = rt.view_transform(rt.Point(0, 0, 0), rt.Point(0, 0, 5), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 1.2, cameratransform)

    world = rt.World()
    light = rt.PointLight(rt.Point(0, 100, 0), rt.Color(1, 1, 1))
    world.lights.append(light)

    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.75, 0.75, 0.75), rt.translation(0, 0, 5))
    sphere.material.diffuse = 0.4
    sphere.material.specular = 0.6
    sphere.material.shininess = 20
    sphere.material.reflective = 0.6
    sphere.material.ambient = 0
    world.objects.append(sphere)

    # the cube map image is from Lancellotti Chapel from
    # http://www.humus.name/index.php?page=Textures
    # It is the work of Emil Persson, a.k.a. Humus
    # It is licensed under a Creative Commons Attribution 3.0 Unported License
    # http://creativecommons.org/licenses/by/3.0
    cube = rt.Cube()
    cube.transform = rt.scaling(1000, 1000, 1000)
    cube.material.pattern = rt.CubeMap()

    cube.material.pattern.leftpattern = rt.UVImagePattern('raytracer/test_ppm_files/chapel_negx.ppm', rt.cube_uv_left)
    cube.material.pattern.rightpattern = rt.UVImagePattern('raytracer/test_ppm_files/chapel_posx.ppm', rt.cube_uv_right)
    cube.material.pattern.frontpattern = rt.UVImagePattern('raytracer/test_ppm_files/chapel_posz.ppm', rt.cube_uv_front)
    cube.material.pattern.backpattern = rt.UVImagePattern('raytracer/test_ppm_files/chapel_negz.ppm', rt.cube_uv_back)
    cube.material.pattern.uppattern = rt.UVImagePattern('raytracer/test_ppm_files/chapel_posy.ppm', rt.cube_uv_up)
    cube.material.pattern.downpattern = rt.UVImagePattern('raytracer/test_ppm_files/chapel_negy.ppm', rt.cube_uv_down)

    cube.material.diffuse = 0
    cube.material.specular = 0
    cube.material.ambient = 1
    world.objects.append(cube)

    return camera, world


def orrery_notch(theta=0.0):
    left = rt.Cube()
    left.transform = rt.chain_transforms(rt.scaling(1, 0.25, 1), rt.translation(1, 0, 1), rt.rotation_y(0.7854),
                                         rt.scaling(1, 1, 0.1))
    right = rt.Cylinder()
    right.min_y = -0.26
    right.max_y = 0.26
    right.closed = True
    right.transform = rt.scaling(0.8, 1, 0.8)

    notch = rt.CSG('difference', left, right)
    notch.transform = rt.rotation_y(theta)
    return notch


def orrery_gear():
    left = rt.Cylinder()
    left.min_y = -0.025
    left.max_y = 0.025
    left.closed = True

    right = rt.ObjectGroup()
    centerhole = rt.Cylinder()
    centerhole.min_y = -0.06
    centerhole.max_y = 0.06
    centerhole.closed = True
    centerhole.transform = rt.scaling(0.1, 1, 0.1)
    right.addchild(centerhole)

    crescentleft = rt.Cylinder()
    crescentleft.min_y = -0.06
    crescentleft.max_y = 0.06
    crescentleft.closed = True
    crescentleft.transform = rt.scaling(0.7, 1, 0.7)
    crescentright = rt.Cube()
    crescentright.transform = rt.scaling(1, 0.1, 0.2)
    crescent = rt.CSG('difference', crescentleft, crescentright)
    right.addchild(crescent)

    for i in range(-9, 11):
        right.addchild(orrery_notch(i * math.pi / 10))

    gear = rt.CSG('difference', left, right)
    return gear


def orrery_demo(width=800, height=400):
    # ======================================================
    # orrery.yml
    #
    # This file describes the title image for the "Texture
    # Mapping" bonus chapter at:
    #
    # http://www.raytracerchallenge.com/bonus/texture-mapping.html
    #
    # It requires several additional resources, provided as a
    # separate download. The resources were found on the following
    # sites:
    #
    # * https://www.bittbox.com/freebies/free-hi-resolution-wood-textures
    #   : the wooden texture for the table
    # * https://astrogeology.usgs.gov/search/map/Mercury/Messenger/Global/Mercury_MESSENGER_MDIS_Basemap_LOI_Mosaic_Global_166m
    #   : the map of Mercury
    # * http://planetpixelemporium.com/planets.html
    #   : maps of Earth, Mars, Jupiter, Saturn, Uranus, and Neptune
    # * https://hdrihaven.com/hdri/?c=indoor&h=artist_workshop
    #   : the "artist workshop" environment map
    #
    # by Jamis Buck <jamis@jamisbuck.org>
    # ======================================================

    cameratransform = rt.view_transform(rt.Point(2, 4, -10), rt.Point(-1, -1, 0), rt.Point(0, 1, 0))
    camera = rt.Camera(width, height, 1.2, cameratransform)

    world = rt.World()
    light = rt.AreaLight(rt.Point(-5, 0, -10), rt.Vector(10, 0, 0), 10, rt.Vector(0, 5, 0), 5, True, rt.Color(1, 1, 1))
    world.lights.append(light)

    GOLD = rt.Material()
    GOLD.color = rt.Color(1, 0.8, 0.1)
    GOLD.ambient = 0.1
    GOLD.diffuse = 0.6
    GOLD.specular = 0.3
    GOLD.shininess = 15

    SILVER = rt.Material()
    SILVER.color = rt.Color(1, 1, 1)
    SILVER.ambient = 0.1
    SILVER.diffuse = 0.7
    SILVER.specular = 0.3
    SILVER.shininess = 15

    topplateleft = rt.Cylinder()
    topplateleft.min_y = -1.51
    topplateleft.max_y = -1.5
    topplateleft.closed = True
    topplateright = rt.ObjectGroup()
    child1 = rt.Cylinder()
    child1.min_y = -1.52
    child1.max_y = -1.49
    child1.closed = True
    child1.transform = rt.scaling(0.1, 1, 0.1)
    child2left = rt.Cylinder()
    child2left.min_y = -1.52
    child2left.max_y = -1.49
    child2left.closed = True
    child2left.transform = rt.scaling(0.75, 1, 0.75)
    child2right = rt.Cube()
    child2right.transform = rt.chain_transforms(rt.scaling(1, 0.1, 0.2), rt.translation(0, -1.5, 0))
    child2 = rt.CSG('difference', child2left, child2right)
    topplateright.addchild(child1)
    topplateright.addchild(child2)
    topplate = rt.CSG('difference', topplateleft, topplateright)
    topplate.transform = rt.rotation_y(-1)
    topplate.material = GOLD
    topplate.push_material_to_children()
    world.objects.append(topplate)

    gear = orrery_gear()
    gear.transform = rt.chain_transforms(rt.scaling(0.5, 0.5, 0.5), rt.translation(0.4, -1.45, -0.4))
    gear.material = SILVER
    world.objects.append(gear)

    gear = orrery_gear()
    gear.transform = rt.chain_transforms(rt.rotation_y(0.8), rt.scaling(0.4, 0.4, 0.4),
                                         rt.translation(-0.4, -1.45, 0.2))
    gear.material = SILVER
    world.objects.append(gear)

    sun = rt.ObjectGroup()
    child = rt.Sphere()
    child.casts_shadow = False  # TODO - change this to True
    child.material.color = rt.Color(1, 1, 0)
    child.material.ambient = 0.1
    child.material.diffuse = 0.6
    child.material.specular = 0  # TODO - change this because we aren't using skybox
    child.material.reflective = 0.2
    sun.addchild(child)
    child = rt.Cylinder()
    child.min_y = -4
    child.max_y = -0.5
    child.transform = rt.scaling(0.025, 1, 0.025)
    child.material = GOLD
    sun.addchild(child)
    world.objects.append(sun)

    base = rt.Sphere()
    base.transform = rt.translation(0, -4, 0)
    base.material.pattern = rt.UVCheckersPattern(16, 8, rt.Color(0, 0, 0), rt.Color(0.5, 0.5, 0.5), rt.spherical_map)
    base.material.diffuse = 0.6
    base.material.specular = 0  # TODO - change this because we aren't using skybox
    base.material.ambient = 0.1
    base.material.reflective = 0.2
    world.objects.append(base)

    table = rt.Cube()
    table.transform = rt.chain_transforms(rt.scaling(5, 0.1, 5), rt.translation(0, -4, 0))
    table.material.diffuse = 0.9
    table.material.ambient = 0.1
    table.material.specular = 0
    table.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/woodgrain.ppm', rt.planar_map)
    table.material.pattern.transform = rt.scaling(0.5, 0.5, 0.5)
    world.objects.append(table)

    # gear-plate between top and mercury
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.rotation_y(-0.4), rt.scaling(0.9, 0.9, 0.9), rt.translation(0, -1.75, 0))
    world.objects.append(gear)

    mercury = rt.ObjectGroup()
    mercury.transform = rt.chain_transforms(rt.translation(2, 0, 0), rt.rotation_y(0.7))
    planet = rt.Sphere()
    planet.transform = rt.scaling(0.25, 0.25, 0.25)
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/mercurymap.ppm', rt.spherical_map)
    mercury.addchild(planet)
    world.objects.append(planet)
    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 2
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    mercury.addchild(stand)
    world.objects.append(mercury)

    # gear-plate between Mercury & Venus
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.rotation_y(1.3), rt.translation(0, -2.05, 0))
    world.objects.append(gear)

    venus = rt.ObjectGroup()
    venus.transform = rt.chain_transforms(rt.translation(3, 0, 0), rt.rotation_y(0.3))
    planet = rt.Sphere()
    planet.transform = rt.scaling(0.25, 0.25, 0.25)
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/venusmap.ppm', rt.spherical_map)
    venus.addchild(planet)
    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2.1
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2.1, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 3
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2.1, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    venus.addchild(stand)
    world.objects.append(venus)

    # gear-plate between Venus and Earth
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.scaling(0.9, 0.9, 0.9), rt.rotation_y(-2.2),
                                         rt.translation(0, -2.15, 0))
    world.objects.append(gear)

    earth = rt.ObjectGroup()
    earth.transform = rt.chain_transforms(rt.translation(4, 0, 0), rt.rotation_y(2))
    planet = rt.Sphere()
    planet.transform = rt.scaling(0.25, 0.25, 0.25)
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/earthmap1k.ppm', rt.spherical_map)
    earth.addchild(planet)
    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2.2
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2.2, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 4
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2.2, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    earth.addchild(stand)
    world.objects.append(earth)

    # gear-plate between Earth and Mars
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.scaling(0.8, 0.8, 0.8), rt.rotation_y(1.7),
                                         rt.translation(0, -2.25, 0))
    world.objects.append(gear)

    mars = rt.ObjectGroup()
    mars.transform = rt.chain_transforms(rt.translation(5, 0, 0), rt.rotation_y(-2))
    planet = rt.Sphere()
    planet.transform = rt.scaling(0.25, 0.25, 0.25)
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/marsmap.ppm', rt.spherical_map)
    mars.addchild(planet)
    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2.3
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2.3, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 5
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2.3, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    mars.addchild(stand)
    world.objects.append(mars)

    # gear-plate between Mars and Jupiter
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.rotation_y(-0.9), rt.translation(0, -2.35, 0))
    world.objects.append(gear)

    jupiter = rt.ObjectGroup()
    jupiter.transform = rt.chain_transforms(rt.translation(6.5, 0, 0), rt.rotation_y(-0.75))
    planet = rt.Sphere()
    planet.transform = rt.chain_transforms(rt.rotation_y(math.pi), rt.scaling(0.67, 0.67, 0.67))
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/jupitermap.ppm', rt.spherical_map)
    jupiter.addchild(planet)
    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2.4
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2.4, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 6.5
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2.4, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    jupiter.addchild(stand)
    world.objects.append(jupiter)

    # gear-plate between Jupiter and Saturn
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.scaling(0.95, 0.95, 0.95), rt.rotation_y(-1.1), rt.translation(0, -2.45, 0))
    world.objects.append(gear)

    saturn = rt.ObjectGroup()
    saturn.transform = rt.chain_transforms(rt.translation(8, 0, 0), rt.rotation_y(-2.5))
    planet = rt.Sphere()
    planet.transform = rt.scaling(0.5, 0.5, 0.5)
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/saturnmap.ppm', rt.spherical_map)
    saturn.addchild(planet)

    # rings.  TODO: separate the rings somehow or use a better pattern
    left = rt.Cylinder()
    left.min_y = -0.01
    left.max_y = 0.01
    left.closed = True
    left.transform = rt.scaling(1.2, 1, 1.2)
    left.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/saturnringcolor.ppm', rt.planar_map)
    right = rt.Cylinder()
    right.min_y = -0.02
    right.max_y = 0.02
    right.closed = True
    right.transform = rt.scaling(0.75, 1, 0.75)
    rings = rt.CSG('difference', left, right)
    rings.transform = rt.rotation_z(0.2)
    saturn.addchild(rings)

    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2.5
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2.5, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 8
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2.5, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    saturn.addchild(stand)
    world.objects.append(saturn)

    # gear-plate between Saturn & Uranus
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.scaling(0.9, 0.9, 0.9), rt.rotation_y(1), rt.translation(0, -2.55, 0))
    world.objects.append(gear)

    uranus = rt.ObjectGroup()
    uranus.transform = rt.chain_transforms(rt.translation(9, 0, 0), rt.rotation_y(-3))
    planet = rt.Sphere()
    planet.transform = rt.scaling(0.4, 0.4, 0.4)
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/uranusmap.ppm', rt.spherical_map)
    uranus.addchild(planet)
    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2.6
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2.6, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 9
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2.6, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    uranus.addchild(stand)
    world.objects.append(uranus)

    # gear-plate between Uranus & Neptune
    gear = orrery_gear()
    gear.material = SILVER
    gear.transform = rt.chain_transforms(rt.rotation_y(-1), rt.translation(0, -2.65, 0))
    world.objects.append(gear)

    neptune = rt.ObjectGroup()
    neptune.transform = rt.chain_transforms(rt.translation(10, 0, 0), rt.rotation_y(-1.25))
    planet = rt.Sphere()
    planet.transform = rt.scaling(0.4, 0.4, 0.4)
    planet.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/neptunemap.ppm', rt.spherical_map)
    neptune.addchild(planet)
    stand = rt.ObjectGroup()
    cylinder = rt.Cylinder()
    cylinder.min_y = -2.7
    cylinder.max_y = 0
    cylinder.transform = rt.scaling(0.025, 1, 0.025)
    stand.addchild(cylinder)
    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.025, 0.025, 0.025), rt.translation(0, -2.7, 0))
    stand.addchild(sphere)
    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 10
    cylinder.transform = rt.chain_transforms(rt.scaling(0.025, 1, 0.025), rt.rotation_z(1.5708),
                                             rt.translation(0, -2.7, 0))
    stand.addchild(cylinder)
    stand.material = GOLD
    stand.push_material_to_children()
    neptune.addchild(stand)
    world.objects.append(neptune)

    for i in world.objects:
        i.divide(7)

    environment = rt.Sphere()
    environment.transform = rt.scaling(1000, 1000, 1000)
    # Note - I used the 4k version to generate the demo image, but that is too large for github.
    environment.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/artist_workshop_4k.ppm',
                                                     rt.spherical_map)
    environment.material.pattern.transform = rt.rotation_y(-2.7)
    environment.material.diffuse = 0
    environment.material.specular = 0
    environment.material.ambient = 1
    world.objects.append(environment)

    return camera, world


def shadow_glamour_shot(width=400, height=160):
    cameratransform = rt.view_transform(rt.Point(-3, 1, 2.5), rt.Point(0, 0.5, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 0.7854, cameratransform)

    world = rt.World()
    light = rt.AreaLight(rt.Point(-1, 2, 4), rt.Vector(2, 0, 0), 10, rt.Vector(0, 2, 0), 10,
                         True, rt.Color(1.5, 1.5, 1.5))
    world.lights.append(light)

    cube = rt.Cube()
    cube.material.color = rt.Color(1.5, 1.5, 1.5)  # make it a shining cube
    cube.material.ambient = 1
    cube.material.diffuse = 0
    cube.material.specular = 0
    cube.transform = rt.chain_transforms(rt.scaling(1, 1, 0.01), rt.translation(0, 3, 4))
    cube.casts_shadow = False
    world.objects.append(cube)

    plane = rt.Plane()
    plane.material.color = rt.Color(1, 1, 1)
    plane.material.ambient = 0.025
    plane.material.diffuse = 0.67
    plane.material.specular = 0.9
    world.objects.append(plane)

    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.5, 0.5, 0.5), rt.translation(0.5, 0.5, 0))
    sphere.material.color = rt.Color(1, 0, 0)
    sphere.material.ambient = 0.1
    sphere.material.specular = 0
    sphere.material.diffuse = 0.6
    sphere.material.reflective = 0.3
    world.objects.append(sphere)

    sphere = rt.Sphere()
    sphere.transform = rt.chain_transforms(rt.scaling(0.33, 0.33, 0.33), rt.translation(-0.25, 0.33, 0))
    sphere.material.color = rt.Color(0.5, 0.5, 1)
    sphere.material.ambient = 0.1
    sphere.material.specular = 0
    sphere.material.diffuse = 0.6
    sphere.material.reflective = 0.3
    world.objects.append(sphere)

    return camera, world


def spheres_demo1(width=800, height=533):
    cameratransform = rt.view_transform(rt.Point(6.5, 1.25, -3), rt.Point(0, 0, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi/2, cameratransform, 0.04, 6.27)

    world = rt.WorldWithSky()
    light = rt.AreaLight(rt.Point(-1, 10, 0), rt.Vector(2, 0, 0), 4, rt.Vector(0, 0, 2), 4, True, rt.Color(1, 1, 1))
    world.lights.append(light)

    metal = rt.Material()
    metal.reflective = 0.4
    metal.diffuse = 0.4
    metal.ambient = 0.2
    metal.shininess = 300
    metal.specular = 0.1

    glass = rt.Material()
    glass.color = rt.Color(0.8, 0.8, 0.9)
    glass.ambient = 0
    glass.diffuse = 0.2
    glass.specular = 0.9
    glass.shininess = 300
    glass.transparency = 0.8
    glass.refractive_index = 1.57

    matte = rt.Material()
    matte.specular = 0
    matte.shininess = 0
    matte.reflective = 0
    matte.ambient = 0.2
    matte.diffuse = 0.8

    ground = rt.Sphere()
    ground.transform = rt.chain_transforms(rt.scaling(1000, 1000, 1000), rt.translation(0, -1000, 0))
    ground.material = deepcopy(matte)
    ground.material.color = rt.Color(0.5, 0.6, 0.7)
    world.objects.append(ground)

    big_glass = rt.Sphere()
    big_glass.transform = rt.translation(1, 1, 0)
    big_glass.material = deepcopy(glass)
    world.objects.append(big_glass)

    big_diffuse = rt.Sphere()
    big_diffuse.transform = rt.translation(-2, 1, 0)
    big_diffuse.material = deepcopy(matte)
    big_diffuse.material.color = rt.Color(0.4, 0.2, 0.1)
    world.objects.append(big_diffuse)

    big_metal = rt.Sphere()
    big_metal.transform = rt.translation(4, 1, 0)
    big_metal.material = deepcopy(metal)
    big_metal.material.color = rt.Color(0.7, 0.6, 0.5)
    world.objects.append(big_metal)

    g = rt.ObjectGroup()
    for a in range(-11, 12):
        for b in range(-11, 12):
            mat = random.random()
            sphere = rt.Sphere()
            translation = rt.translation(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())
            sphere.transform = rt.chain_transforms(rt.scaling(0.2, 0.2, 0.2), translation)
            if mat < 0.7:
                sphere.material = deepcopy(matte)
                sphere.material.color = rt.Color(random.uniform(0.2, 1.0),
                                                 random.uniform(0.2, 1.0),
                                                 random.uniform(0.2, 1.0))
            elif mat < 0.9:
                sphere.material = deepcopy(metal)
                sphere.material.fuzz = random.uniform(0, 0.125)
                sphere.material.color = rt.Color(random.uniform(0.5, 1.0), random.uniform(0.5, 1.0),
                                                 random.uniform(0.5, 1.0))

            else:
                sphere.material = deepcopy(glass)

            g.addchild(sphere)

    g.divide(5)
    world.objects.append(g)

    return camera, world


def dof_demo(width=800, height=600):
    cameratransform = rt.view_transform(rt.Point(0, 1, -1), rt.Point(0, 0.5, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi / 2, cameratransform, 0.04, 2.2361)

    world = rt.World()
    light = rt.PointLight(rt.Point(0, 5, -3), rt.Color(1, 1, 1))
    world.lights.append(light)

    metal = rt.Material()
    metal.reflective = 0.4 # 0.4
    metal.diffuse = 0.4 # 0.55
    metal.ambient = 0.2 # 0.15
    metal.shininess = 300
    metal.specular = 0.1 # 0.1

    group = rt.ObjectGroup()
    for x in [-2.0, -1, 0, 1, 2]:
        for z in [0, 0.5, 1, 1.5, 2, 2.5]:
            sphere = rt.Sphere()
            sphere.transform = rt.chain_transforms(rt.scaling(0.25, 0.25, 0.25), rt.translation(x, 0, z))
            r = (z + 2) / 4
            g = (x + z + 2) / 6.5
            b = ((-math.fabs(x) + 2) + (-math.fabs(z - 1) + 1.5)) / 3.5
            sphere.material = deepcopy(metal)
            sphere.material.color = rt.Color(r, g, b)
            group.addchild(sphere)
    group.divide(3)
    world.objects.append(group)

    plane = rt.Plane()
    plane.transform = rt.translation(0, -0.25, 0)
    plane.material.color = rt.Color(0.52, 0.6, 0.71)
    plane.material.reflective = 0.1
    world.objects.append(plane)

    plane = rt.Plane()
    plane.transform = rt.translation(0, 10, 0)
    plane.material.color = rt.Color(1, 1, 1)
    plane.material.reflective = 0
    world.objects.append(plane)

    return camera, world


def torus_demo(width=200, height=200):
    cameratransform = rt.view_transform(rt.Point(-4, 2, 0), rt.Point(-1, 0.75, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi/2, cameratransform)
    world = rt.World()
    light = rt.PointLight(rt.Point(0, 10, 0), rt.Color(1, 1, 1))
    world.lights.append(light)

    torus = rt.Torus()
    torus.transform = rt.scaling(1.25, 1.25, 1.25)
    torus.material.color = rt.Color(0.75, 0, 1.0)
    torus.material.ambient = 0.2
    torus.material.diffuse = 0.8
    world.objects.append(torus)

    return camera, world


def torus_demo2(width=400, height=400):
    w = rt.World()
    cameratransform = rt.view_transform(rt.Point(8, 4.5, -9), rt.Point(0, 1.25, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi/20, cameratransform)

    light = rt.PointLight(rt.Point(1, 6.9, -4.9), rt.Color(1, 1, 1))
    w.lights.append(light)

    floor = rt.Plane()
    A = rt.scaling(0.25, 0.25, 0.25)
    B = rt.rotation_y(0.3)
    floor.material.pattern = rt.CheckersPattern()
    floor.material.pattern.color1 = rt.Color(0.5, 0.5, 0.5)
    floor.material.pattern.color2 = rt.Color(0.75, 0.75, 0.75)
    floor.material.pattern.transform = rt.chain_transforms(A, B)
    floor.material.ambient = 0.1
    floor.material.diffuse = 0.8
    floor.material.reflective = 0.1
    floor.material.specular = 0
    w.objects.append(floor)

    plastic = rt.Material()
    plastic.diffuse = 0.8
    plastic.ambient = 0.2

    basesphere = rt.Sphere()
    basesphere.material = deepcopy(plastic)
    basesphere.material.color = rt.Color(226/255, 1, 253/255)
    basecube = rt.Cube()
    basecube.transform = rt.translation(0, 0.2, 0)
    base1 = rt.CSG('difference', basesphere, basecube)
    basecube2 = rt.Cube()
    basecube2.transform = rt.translation(1.4, 0, 0)
    base2 = rt.CSG('difference', base1, basecube2)
    basecube3 = rt.Cube()
    basecube3.transform = rt.translation(-1.4, 0, 0)
    base3 = rt.CSG('difference', base2, basecube3)

    cone = rt.Cone()
    cone.min_y = -2
    cone.max_y = -0.5
    cone.material = deepcopy(plastic)
    cone.material.color = rt.Color(207/255, 207/255, 0)
    cone.transform = rt.scaling(0.1, 1.5, 0.1)
    ball = rt.Sphere()
    ball.material = deepcopy(plastic)
    ball.material.color = rt.Color(207/255, 207/255, 0)
    ball.transform = rt.chain_transforms(rt.scaling(0.1, 0.1, 0.1), rt.translation(0, -0.75, 0))
    stick = rt.CSG('union', cone, ball)
    stick.transform = rt.translation(0, 1.5, 0)
    base = rt.CSG('union', base3, stick)
    base.transform = rt.scaling(1.2, 1, 1)

    redtorus = rt.Torus()
    redtorus.R = 0.4
    redtorus.r = 0.12
    redtorus.material = deepcopy(plastic)
    redtorus.material.color = rt.Color(1, 0, 40/255)
    redtorus.transform = rt.translation(0, -0.67, 0)

    orangetorus = rt.Torus()
    orangetorus.material = deepcopy(plastic)
    orangetorus.R = 0.35
    orangetorus.r = 0.12
    orangetorus.material.color = rt.Color(1, 175/255, 0)
    orangetorus.transform = rt.translation(0, -0.43, 0)

    yellowtorus = rt.Torus()
    yellowtorus.material = deepcopy(plastic)
    yellowtorus.R = 0.3
    yellowtorus.r = 0.12
    yellowtorus.material.color = rt.Color(0.961, 0.98, 0)
    yellowtorus.transform = rt.translation(0, -0.19, 0)

    greentorus = rt.Torus()
    greentorus.material = deepcopy(plastic)
    greentorus.R = 0.25
    greentorus.r = 0.1
    greentorus.material.color = rt.Color(0, 0.812, 0.094)
    greentorus.transform = rt.translation(0, 0.01, 0)

    bluetorus = rt.Torus()
    bluetorus.material = deepcopy(plastic)
    bluetorus.R = 0.2
    bluetorus.r = 0.1
    bluetorus.material.color = rt.Color(0, 0.518, 0.91)
    bluetorus.transform = rt.translation(0, 0.21, 0)

    purpletorus = rt.Torus()
    purpletorus.material = deepcopy(plastic)
    purpletorus.R = 0.15
    purpletorus.r = 0.1
    purpletorus.material.color = rt.Color(0.467, 0, 0.502)
    purpletorus.transform = rt.translation(0, 0.41, 0)

    toy = rt.ObjectGroup()
    toy.addchild(base)
    toy.addchild(redtorus)
    toy.addchild(orangetorus)
    toy.addchild(yellowtorus)
    toy.addchild(greentorus)
    toy.addchild(bluetorus)
    toy.addchild(purpletorus)

    toy.transform = rt.chain_transforms(rt.rotation_y(math.pi/3), rt.translation(-1, 1, 1))
    w.objects.append(toy)

    return camera, w


def fuzzdemo1(width=400, height=225):

    world = rt.WorldWithSky()
    viewtransform = rt.view_transform(rt.Point(0, 0, 1), rt.Point(0, 0, -1), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi/2, viewtransform)

    light = rt.PointLight(rt.Point(0, 5, 3), rt.Color(1, 1, 1))
    world.lights.append(light)

    diffuse = rt.Material()
    diffuse.ambient = 0.2
    diffuse.diffuse = 0.8
    diffuse.specular = 0
    diffuse.shininess = 0

    metal = rt.Material()
    metal.ambient = 0.2
    metal.diffuse = 0.4
    metal.reflective = 0.4
    metal.shininess = 300
    metal.specular = 0.1


    ground = rt.Sphere()
    ground.transform = rt.chain_transforms(rt.scaling(100, 100, 100), rt.translation(0, -100.5, -1))
    ground.material = deepcopy(diffuse)
    ground.material.color = rt.Color(0.8, 0.8, 0)
    world.objects.append(ground)

    center = rt.Sphere()
    center.transform = rt.chain_transforms(rt.scaling(0.5, 0.5, 0.5), rt.translation(0, 0, -1))
    center.material = deepcopy(diffuse)
    center.material.color = rt.Color(0.7, 0.3, 0.3)
    world.objects.append(center)

    left = rt.Sphere()
    left.transform = rt.chain_transforms(rt.scaling(0.5, 0.5, 0.5), rt.translation(1, 0, -1))
    left.material = deepcopy(metal)
    left.material.color = rt.Color(0.8, 0.8, 0.8)
    left.material.fuzz = 0.075
    world.objects.append(left)

    right = rt.Sphere()
    right.transform = rt.chain_transforms(rt.scaling(0.5, 0.5, 0.5), rt.translation(-1, 0, -1))
    right.material = deepcopy(metal)
    right.material.color = rt.Color(0.8, 0.6, 0.2)
    right.material.fuzz = 0.25
    world.objects.append(right)

    return camera, world


def spotlight_demo1(width=400, height=200):

    world = rt.World()
    camera_transform = rt.view_transform(rt.Point(2, 1, 0), rt.Point(1, 0.75, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi/2, camera_transform)

    light = rt.PointLight(rt.Point(-1, 5, 0), rt.Color(0.1, 0.1, 0.1))
    # world.lights.append(light)
    light = rt.PointLight(rt.Point(-1, 0.99, 0.01), rt.Color(1, 1, 1))
    world.lights.append(light)


    left = rt.Sphere()
    left.material.color = rt.Color(1, 1, 0)
    left.material.transparency = 0.6
    left.material.refractive_index = 1.5
    left.material.ambient = 0.1
    left.material.diffuse = 0.4
    left.material.reflective = 0.4

    right = rt.Cube()
    right.transform = rt.translation(0, 0, 1)

    semisphere = rt.CSG('difference', left, right)
    semisphere.transform = rt.chain_transforms(rt.scaling(0.25, 0.25, 0.5), rt.rotation_x(math.pi/4), rt.translation(-1, 1, 0))
    world.objects.append(semisphere)


    sphere = rt.Sphere()
    sphere.material.color = rt.Color(1, 0, 1)
    sphere.material.reflective = 0.2
    sphere.material.diffuse = 0.8
    sphere.material.ambient = 0.1
    sphere.transform = rt.chain_transforms(rt.scaling(0.25, 0.25, 0.25), rt.translation(-1, 0, 1))
    world.objects.append(sphere)

    plane = rt.Plane()
    plane.material.color = rt.Color(0.5, 0.5, 0.5)
    plane.material.diffuse = 1
    plane.material.ambient = 0
    plane.transform = rt.translation(0, -1, 0)
    world.objects.append(plane)

    return camera, world


def lamp_demo(width=600, height=200):
    w = rt.World()
    cameratransform = rt.view_transform(rt.Point(-6.0, 2.2, 1), rt.Point(.125, 1.75, -1.025), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, math.pi/2, cameratransform)

    light = rt.PointLight(rt.Point(-1, 2, -3.5), rt.Color(0.1, 0.1, 0.1))
    w.lights.append(light)
    vec = rt.Point(0.15 , 2.45, -1.85) - rt.Point(-1, 2, -3.5)
    light2 = rt.SpotLight(rt.Point(-3, 2, -3.5), vec, math.pi/5, math.pi/7.5, rt.Color(0.8, 0.8, 0.8))
    w.lights.append(light2)

    vec = rt.Point(-0.2, 0.35, -1.5) - rt.Point(0.1, 1.7, -0.2)
    light3 = rt.SpotLight(rt.Point(0.1, 1.7, -0.2), vec, math.pi/2, math.pi/4, rt.Color(0.2, 0.2, 0.2), True, 1.0 / (16 * math.pi))
    w.lights.append(light3)
    light4 = rt.PointLight(rt.Point(0.1, 1.7, -0.2) + (vec * 0.1), rt.Color(0.7, 0.7, 0.7), True, 1.0 / (16 * math.pi))
    w.lights.append(light4)

    # big lamp
    vec = rt.Point(-0.2, 0.1, 0.6) - rt.Point(0.15, 2.35, -1.85)
    light5 = rt.SpotLight(rt.Point(0.15, 2.35, -1.85), vec, math.pi/2, math.pi/4, rt.Color(0.2, 0.2, 0.2), True, 1.0 / (16 * math.pi))
    w.lights.append(light5)
    light6 = rt.PointLight(rt.Point(0.15, 2.35, -1.85) + (vec * 0.1), rt.Color(0.7, 0.7, 0.7), True, 1.0 / (16 * math.pi))
    w.lights.append(light6)

    parser = rt.Parser()
    # lamp downloaded from: https://free3d.com/3d-model/lamp-37276.html
    parser.parse_obj_file('raytracer/test_obj_files/lamp.obj')
    g = parser.get_group_by_name('Circle')
    # g.transform = rt.chain_transforms(rt.rotation_y(math.pi), rt.translation(0, 1, 0.5))
    g.transform = rt.chain_transforms(rt.translation(0, 1, -0.3), rt.rotation_y(math.pi))
    g.material.color = rt.Color(0.47, 0.49, 0.64)
    g.material.ambient = 0.2
    g.material.diffuse = 1.4
    g.material.shininess = 200
    g.material.specular = 0.4
    g.material.reflective = 0.2
    g.push_material_to_children()
    g.divide(10)
    w.objects.append(g)

    g2 = deepcopy(g)
    g2.transform = rt.chain_transforms(rt.scaling(1.5, 1.5, 1.5), rt.translation(0, 1.45, -2.5) )
    w.objects.append(g2)

    ball = rt.Sphere()
    ball.transform = rt.chain_transforms(rt.scaling(0.25, 0.25, 0.25), rt.translation(-0.2, 0.35, -1.5) )#, rt.rotation_x(-math.pi/4), rt.rotation_y(-math.pi/4))
    ball.material.diffuse = 0.9
    ball.material.specular = 0.1
    ball.material.shininess = 10
    ball.material.ambient = 0.1
    # image is from http://mdinfotech.net/images/luxo.png
    ball.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/luxo.ppm', rt.spherical_map)
    w.objects.append(ball)

    table = rt.Cube()
    table.transform = rt.chain_transforms(rt.scaling(5, 0.1, 5), rt.translation(0, 0, 0))
    table.material.diffuse = 0.9
    table.material.ambient = 0.1
    table.material.specular = 0
    table.material.reflective = 0.1
    table.material.pattern = rt.UVImagePattern('raytracer/test_ppm_files/woodgrain.ppm', rt.planar_map)
    table.material.pattern.transform = rt.scaling(0.5, 0.5, 0.5)
    w.objects.append(table)

    '''
    r = rt.Sphere()
    r.transform = rt.chain_transforms(rt.scaling(0.1, 0.2, 0.1), rt.translation(0.15 , 2.45, -1.85))
    r.material.ambient = 1
    r.material.color = rt.Color(1, 0, 0)
    w.objects.append(r)
    '''

    return camera, w

