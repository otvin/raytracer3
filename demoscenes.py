import math
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
    floorceiling.transform = rt.matmul4x4(B, A)
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
    tabletop.transform = rt.matmul4x4(B, A)
    C = rt.rotation_y(0.1)
    D = rt.scaling(0.05, 0.05, 0.05)
    patternxform = rt.matmul4x4(D, C)
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
    leg1.transform = rt.matmul4x4(B, A)
    leg1.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg1.material.ambient = 0.2
    leg1.material.diffuse = 0.7
    w.objects.append(leg1)

    leg2 = rt.Cube()
    A = rt.scaling(0.1, 1.5, 0.1)
    B = rt.translation(2.7, 1.5, 1.7)
    leg2.transform = rt.matmul4x4(B, A)
    leg2.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg2.material.ambient = 0.2
    leg2.material.diffuse = 0.7
    w.objects.append(leg2)

    leg3 = rt.Cube()
    A = rt.scaling(0.1, 1.5, 0.1)
    B = rt.translation(-2.7, 1.5, -1.7)
    leg3.transform = rt.matmul4x4(B, A)
    leg3.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg3.material.ambient = 0.2
    leg3.material.diffuse = 0.7
    w.objects.append(leg3)

    leg4 = rt.Cube()
    A = rt.scaling(0.1, 1.5, 0.1)
    B = rt.translation(-2.7, 1.5, 1.7)
    leg4.transform = rt.matmul4x4(B, A)
    leg4.material.color = rt.Color(0.5529, 0.4235, 0.3255)
    leg4.material.ambient = 0.2
    leg4.material.diffuse = 0.7
    w.objects.append(leg4)

    glasscube = rt.Cube()
    A = rt.scaling(0.25, 0.25, 0.25)
    B = rt.rotation_y(0.2)
    C = rt.translation(0, 3.45001, 0)
    glasscube.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
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
    littlecube1.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
    littlecube1.material.color = rt.Color(1, 0.5, 0.5)
    littlecube1.material.reflective = 0.6
    littlecube1.material.diffuse = 0.4
    w.objects.append(littlecube1)

    littlecube2 = rt.Cube()
    A = rt.scaling(0.15, 0.07, 0.15)
    B = rt.rotation_y(0.4)
    C = rt.translation(-1.5, 3.27, 0.3)
    littlecube2.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
    littlecube2.material.color = rt.Color(1, 1, 0.5)
    w.objects.append(littlecube2)

    littlecube3 = rt.Cube()
    A = rt.scaling(0.2, 0.05, 0.05)
    B = rt.rotation_y(0.4)
    C = rt.translation(0, 3.25, 1)
    littlecube3.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
    littlecube3.material.color = rt.Color(0.5, 1, 0.5)
    w.objects.append(littlecube3)

    littlecube4 = rt.Cube()
    A = rt.scaling(0.05, 0.2, 0.05)
    B = rt.rotation_y(0.8)
    C = rt.translation(-0.6, 3.4, -1)
    littlecube4.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
    littlecube4.material.color = rt.Color(0.5, 0.5, 1)
    w.objects.append(littlecube4)

    littlecube5 = rt.Cube()
    A = rt.scaling(0.05, 0.2, 0.05)
    B = rt.rotation_y(0.8)
    C = rt.translation(2, 3.4, 1)
    littlecube5.transform = rt.matmul4x4(rt.matmul4x4(C, B), A)
    littlecube5.material.color = rt.Color(0.5, 1, 1)
    w.objects.append(littlecube5)

    frame1 = rt.Cube()
    frame1.transform = rt.matmul4x4(rt.translation(-10, 4, 1), rt.scaling(0.05, 1, 1))
    frame1.material.color = rt.Color(0.7098, 0.2471, 0.2196)
    frame1.material.diffuse = 0.6
    w.objects.append(frame1)

    frame2 = rt.Cube()
    frame2.transform = rt.matmul4x4(rt.translation(-10, 3.4, 2.7), rt.scaling(0.05, 0.4, 0.4))
    frame2.material.color = rt.Color(0.2667, 0.2706, 0.6902)
    frame2.material.diffuse = 0.6
    w.objects.append(frame2)

    frame3 = rt.Cube()
    frame3.transform = rt.matmul4x4(rt.translation(-10, 4.6, 2.7), rt.scaling(0.05, 0.4, 0.4))
    frame3.material.color = rt.Color(0.3098, 0.5961, 0.3098)
    frame3.material.diffuse = 0.6
    w.objects.append(frame3)

    mirrorframe = rt.Cube()
    mirrorframe.transform = rt.matmul4x4(rt.translation(-2, 3.5, 9.95), rt.scaling(5, 1.5, 0.05))
    mirrorframe.material.color = rt.Color(0.3882, 0.2627, 0.1882)
    mirrorframe.material.diffuse = 0.7
    w.objects.append(mirrorframe)

    mirror = rt.Cube()
    mirror.transform = rt.matmul4x4(rt.translation(-2, 3.5, 9.95), rt.scaling(4.8, 1.4, 0.06))
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
    cameratransform = rt.view_transform(rt.Point(8, 3.5, -9), rt.Point(0, 0.3, 0), rt.Point(0, 1, 0))
    camera = rt.Camera(width, height, 0.314, cameratransform)

    light = rt.PointLight(rt.Point(1, 6.9, -4.9), rt.Color(1, 1, 1))
    w.lights.append(light)

    floor = rt.Plane()
    A = rt.scaling(0.25, 0.25, 0.25)
    B = rt.rotation_y(0.3)
    floor.material.pattern = rt.CheckersPattern()
    floor.material.pattern.color1 = rt.Color(0.5, 0.5, 0.5)
    floor.material.pattern.color2 = rt.Color(0.75, 0.75, 0.75)
    floor.material.pattern.transform = rt.matmul4x4(B, A)
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
    cyl1.transform = rt.matmul4x4(B, A)
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
    con1.transform = rt.matmul4x4(B, A)
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
    con2.transform = rt.matmul4x4(B, A)
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
    con3.transform = rt.matmul4x4(B, A)
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
    con4.transform = rt.matmul4x4(B, A)
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
    dec1.transform = rt.matmul4x4(B, A)
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
    dec2.transform = rt.matmul4x4(D, rt.matmul4x4(C, rt.matmul4x4(B, A)))
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
    dec3.transform = rt.matmul4x4(D, rt.matmul4x4(C, rt.matmul4x4(B, A)))
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
    dec4.transform = rt.matmul4x4(D, rt.matmul4x4(C, rt.matmul4x4(B, A)))
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
    glass.transform = rt.matmul4x4(B, A)
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
    light = rt.PointLight(rt.Point(0, 0.75, 0), rt.Color(1, 1, 1))
    w.lights = [light]

    cone1 = rt.Cone()
    A = rt.scaling(0.5, 0.5, 0.5)
    B = rt.translation(0.5, 0.25, 1.5)
    cone1.transform = rt.matmul4x4(B, A)
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
    # sphere.transform = rt.matmul4x4(B, rt.matmul4x4(A, trans))
    sphere.transform = rt.matmul4x4(trans, rt.matmul4x4(B, A))
    leg.addchild(sphere)

    cylinder = rt.Cylinder()
    cylinder.min_y = 0
    cylinder.max_y = 1
    A = rt.scaling(0.25, 1, 0.25)
    B = rt.rotation_z(-1.5708)
    C = rt.rotation_y(-0.5236)
    D = rt.translation(0, 0, -1)
    cylinder.transform = rt.matmul4x4(trans, rt.matmul4x4(D, rt.matmul4x4(C, rt.matmul4x4(B, A))))
    leg.addchild(cylinder)

    return leg


def chap14_demo_cap(trans=rt.identity4(), trans2=rt.identity4()):
    cap = rt.ObjectGroup()

    cone1 = rt.Cone()
    cone1.min_y = -1
    cone1.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    cone1.transform = rt.matmul4x4(trans2, rt.matmul4x4(trans, rt.matmul4x4(B, A)))
    cap.addchild(cone1)

    cone2 = rt.Cone()
    cone2.min_y = -1
    cone2.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(1.0472)
    cone2.transform = rt.matmul4x4(trans2, rt.matmul4x4(trans, rt.matmul4x4(C, rt.matmul4x4(B, A))))
    cap.addchild(cone2)

    cone3 = rt.Cone()
    cone3.min_y = -1
    cone3.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(2.0944)
    cone3.transform = rt.matmul4x4(trans2, rt.matmul4x4(trans, rt.matmul4x4(C, rt.matmul4x4(B, A))))
    cap.addchild(cone3)

    cone4 = rt.Cone()
    cone4.min_y = -1
    cone4.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(3.1416)
    cone4.transform = rt.matmul4x4(trans2, rt.matmul4x4(trans, rt.matmul4x4(C, rt.matmul4x4(B, A))))
    cap.addchild(cone4)

    cone5 = rt.Cone()
    cone5.min_y = -1
    cone5.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(4.1888)
    cone5.transform = rt.matmul4x4(trans2, rt.matmul4x4(trans, rt.matmul4x4(C, rt.matmul4x4(B, A))))
    cap.addchild(cone5)

    cone6 = rt.Cone()
    cone6.min_y = -1
    cone6.max_y = 0
    A = rt.scaling(0.24606, 1.37002, 0.24606)
    B = rt.rotation_x(-0.7854)
    C = rt.rotation_y(5.236)
    cone6.transform = rt.matmul4x4(trans2, rt.matmul4x4(trans, rt.matmul4x4(C, rt.matmul4x4(B, A))))
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
    cameratransform = rt.view_transform(rt.Point(0, 0, -9), rt.Point(0, 0, 0), rt.Point(0, 1, 0))
    camera = rt.Camera(width, height, 0.9, cameratransform)

    w.lights.append(rt.PointLight(rt.Point(10000, 10000, -10000), rt.Color(0.25, 0.25, 0.25)))
    w.lights.append(rt.PointLight(rt.Point(-10000, 10000, -10000), rt.Color(0.25, 0.25, 0.25)))
    w.lights.append(rt.PointLight(rt.Point(10000, -10000, -10000), rt.Color(0.25, 0.25, 0.25)))
    w.lights.append(rt.PointLight(rt.Point(-10000, -10000, -10000), rt.Color(0.25, 0.25, 0.25)))

    # a white backdrop
    backdrop = rt.Plane()
    A = rt.rotation_x(1.5708)
    B = rt.translation(0, 0, 100)
    backdrop.transform = rt.matmul4x4(B, A)
    backdrop.material.color = rt.Color(1, 1, 1)
    backdrop.material.ambient = 1
    backdrop.material.diffuse = 0
    backdrop.material.specular = 0
    w.objects.append(backdrop)

    wacky1 = chap14_demo_wacky()
    A = rt.rotation_y(0.1745)
    B = rt.rotation_x(0.4363)
    C = rt.translation(-2.8, 0, 0)
    wacky1.transform = rt.matmul4x4(C, rt.matmul4x4(B, A))
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
    wacky3.transform = rt.matmul4x4(C, rt.matmul4x4(B, A))
    wacky3.material.color = rt.Color(0.2, 0.3, 1.0)
    wacky3.material.ambient = 0.2
    wacky3.material.diffuse = 0.8
    wacky3.material.specular = 0.7
    wacky3.material.shininess = 20
    wacky3.push_material_to_children()
    w.objects.append(wacky3)

    return camera, w
