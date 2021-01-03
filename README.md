### Third raytracer

Built using _The Ray Tracer Challenge_ by Jamis Buck

To execute unit tests, run _python3 unit_tester.py_

As of now, I have implemented all features in the book.  Added several performance optimizations, such as storing the inverse transform and transpose of inverse transform for each object, rather than having to compute it with every intersection.  

The book lists several optional features.  So far, I have implemented anti-aliasing by shooting several rays into random spots in each pixel, instead of just pixel center.

The "saved_renders" folder contains samples from the end of each chapter, once we started rendering.  I have posted PNGs of the files from chapter 11 forward below.


* _chap5.ppm_ - rendered the silhouette of a sphere
* _chap6.ppm_ - rendered a transformed (rotated, scaled in one dimension) sphere
* _chap7.ppm_ - rendered a scene of 6 spheres (3 of them appear to be walls)
* _chap8.ppm_ - added shadows
* _chap9.ppm_ - added planes (the floor is a plane instead of a sphere)
* _chap10.ppm_ - added various patterns
* _chap11_demo.ppm_ - added reflection and refraction. 
* _chap12_demo.ppm_ - added cubes and ability to set object as not casting a shadow
* _chap13_demo.ppm_ - added cylinders.  Note I tweaked the demo image to use scaled glass cube instead of glass cylinder, as in the original image it was unclear to me that the cylinder was glass, so it looked a bit odd.
* _chap13_demo2.ppm_ - added cones.  Added a cone to the demo image and moved the light.
* _chap14_demo.ppm_ - added groups of objects, which can be transformed as a group, and support for multiple lights in a scene.
* _chap15_demo.ppm_ - added triangles and ability to read a limited set of Wavefront .obj files
* _chap15_demo2.ppm_ - the obligatory teapot.  Low-res.  Rendering this model, which contains 241 triangles, took over 18 minutes on my machine with 6 cores/6 threads.
* _chap16_demo.ppm_ - added Constructive Solid Geometry (CSG) supports for intersections, unions, and differences.

Jamis Buck posted details for the scenes shown in the book for chapters 11-14 and 16 on-line.  Links can be found in demoscenes.py.

![chap11_demo.ppm](saved_renders/chap11_demo.png)
![chap12_demo.ppm](saved_renders/chap12_demo.png)
![chap13_demo.ppm](saved_renders/chap13_demo.png)
![chap13_demo2.ppm](saved_renders/chap13_demo2.png)
![chap14_demo.ppm](saved_renders/chap14_demo.png)
![chap15_demo.ppm](saved_renders/chap15_demo.png)
![chap15_demo2.ppm](saved_renders/chap15_demo2.png)
![chap16_demo2.ppm](saved_renders/chap16_demo.png)
