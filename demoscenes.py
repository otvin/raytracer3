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

    light = rt.PointLight(rt.Point(1, 6.9, -4.9), rt.Color(1, 1, 1))
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
    world.lights.append(rt.PointLight(rt.Point(-9, 8, -7), rt.Color(1, 1, 1)))

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


def texture_mapping_demo1(width=400, height=400):
    world = rt.World()
    cameratransform = rt.view_transform(rt.Point(0, 0, -5), rt.Point(0, 0, 0), rt.Vector(0, 1, 0))
    camera = rt.Camera(width, height, 0.5, cameratransform)

    light = rt.PointLight(rt.Point(-10, 10, -10), rt.Color(1, 1, 1))
    world.lights.append(light)

    sphere = rt.Sphere()
    sphere.material.pattern = rt.UVCheckersPattern(20, 10)
    sphere.material.pattern.mapfn = rt.spherical_map
    sphere.material.pattern.color1 = rt.Color(0.0, 0.5, 0.0)
    sphere.material.pattern.color2 = rt.Color(1, 1, 1)
    sphere.material.shininess = 10
    sphere.material.ambient = 0.1
    sphere.material.diffuse = 0.6
    sphere.material.specular = 0.4
    world.objects.append(sphere)

    return camera, world
