import numpy as np
import time
import math
import tuple
import canvas
import objects
import lights
import random
import transformations


def render():
    # this is more accurately computing the sphere's shadow, not rendering the sphere
    # itself.  End of chapter 5 shows the image of what we are doing.

    camera_origin = tuple.Point(0, 0, -5)
    wall_z = 10
    wall_size = 7
    canvas.init_canvas(100, 100)
    pixel_size = wall_size/100.0
    half = wall_size/2.0
    num_samples = 10  # for antialiasing

    shape = objects.Sphere()
    shape.material.color = tuple.Color(1, 0.2, 1)  # purple
    # shape.transform = np.matmul(transformations.rotation_z(math.pi/4), transformations.scaling(1, 0.5, 1))

    light = lights.PointLight(tuple.Point(-10, 10, -10))

    timestart = time.time()
    for y in range(100):
        world_y = half - (pixel_size * y)
        for x in range(100):
            world_x = -half + (pixel_size * x)
            color = tuple.Color(0, 0, 0)
            for i in range(num_samples):
                x_perturb = world_x + (random.uniform(-0.5, 0.5) * pixel_size)
                y_perturb = world_y + (random.uniform(-0.5, 0.5) * pixel_size)
                position = tuple.Point(x_perturb, y_perturb, wall_z)
                r = tuple.Ray(camera_origin, tuple.normalize(position - camera_origin))
                xs = shape.intersect(r)
                if len(shape.intersect(r)) > 0:
                    hit = objects.hit(xs)
                    point = r.at(hit.t)
                    normal = shape.normal_at(point)
                    eyev = -r.direction
                    color += lights.lighting(hit.objhit.material, light, point, eyev, normal)
            canvas.write_pixel(x, y, color / num_samples)

        print ('line {} complete.'.format(y))
    timeend = time.time()
    print('Elapsed time: {} seconds'.format(timeend - timestart))

    canvas.canvas_to_ppm('chap6.ppm')


if __name__ == '__main__':
    render()
