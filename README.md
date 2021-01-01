### Third raytracer

Built using _The Ray Tracer Challenge_ by Jamis Buck

To execute unit tests, run _python3 unit_tester.py_

The "saved_renders" folder contains samples from the end of each chapter, once we started rendering.

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

Jamis Buck posted details for the scenes shown in the book for chapters 11-14 on-line.  Links can be found in demoscenes.py.

![chap11_demo.ppm](saved_renders/chap11_demo.png)
![chap12_demo.ppm](saved_renders/chap12_demo.png)
![chap13_demo.ppm](saved_renders/chap13_demo.png)
![chap13_demo2.ppm](saved_renders/chap13_demo2.png)
![chap14_demo.ppm](saved_renders/chap14_demo.png)
