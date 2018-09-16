# nearestNeighbor
find nearest neighbor using divide &amp; conquer.
----------------------
Command Line Arguments
----------------------
$python3 nearestNeighbor.py --algorithm a filename -v

positional arguments:
  <filename>            Input dataset of points

optional arguments:
  -h, --help            show this help message and exit
  --algorithm ALGORITHM
                        Algorithm: Select the algorithm to run, default is
                        all. (a)ll, (b)ruteforce only or (d)ivide and conquer
                        only
  -v, --verbose
  --profile


----------------------
Discussions
----------------------

The python version I used is Python 3.6.0

function distance(point1,point2) 
calculate the distance between two points.

function closestInStrip(points,d,midx)
find the closest pair and its distance in the middle stripe.

funtion divideAndConquerNearestNeighbor(points)
Recursively call this function to find the closest pair and its distance using divide and conquer.

function bruteForceNearestNeighbor(points)
calculate the distance between every two points to find the closest pair and its distance.

function parseFile(filename)
read the data from the text and construct points

I used cProfile.runctx to profile the running time, and filename_distance.txt to save the result.



