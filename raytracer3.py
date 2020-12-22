import tuple
import canvas
import objects
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

    sphere_color = tuple.Color(1, 0, 0)  # Sphere's have no color/material yet.
    shape = objects.Sphere()

    for y in range(100):
        world_y = half - (pixel_size * y)
        for x in range(100):
            world_x = -half + (pixel_size * x)
            position = tuple.Point(world_x, world_y, wall_z)
            r = tuple.Ray(camera_origin, tuple.normalize(position - camera_origin))
            xs = shape.intersect(r)
            if len(xs) > 0:
                canvas.write_pixel(x, y, sphere_color)

    canvas.canvas_to_ppm('chap5.ppm')



if __name__ == '__main__':
    render()
