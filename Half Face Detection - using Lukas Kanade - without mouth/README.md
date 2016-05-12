##### Half Face Detection - using Lukas Kanade - without mouth detection
==============
I am using Python and OpenCV 3.1.0.
Face detection is achieved with the typical front face cascade andfor the tracking I'm using Lukas-Kanade 
algorithm. The cascade detection is ignored when the
good points movements are under a threshold value (10pxl).
Cascade detection is forced when roi box gets distorted
and when the number of good points are under a threshold (15 points)

Here is a video demonstration of the results http://tinyurl.com/glw8efp .

