import argparse
import os
import cProfile
import math

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the nearest two points on a plan')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ruteforce only or (d)ivide and conquer only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',\
    help='Input dataset of points')


#define function that calculate the distance
def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
#end def distance(point1,point2)


#define function that find the minimal distance
def closestInStrip(points,d,midx):
    dm=d
    pm = (-1,-1)
    qm = (-1,-1)
    cpoints=[p for p in points if midx-d <=p[0] <=midx+d] #candidate points
    cpoints.sort(key=lambda cpoints:cpoints[1])          
    for i in cpoints[:-1]:
        for j in cpoints[cpoints.index(i)+1:]:
            if j[1]>cpoints[cpoints.index(i)][1]+d:
                break
            if distance(i,j)<d:
                dm=distance(i,j)
                pm=i
                qm=j
            #endif
        #endforj
    #endfori
    return (dm,pm,qm) if pm[0]<qm[0] else (dm,qm,pm) 
#end def Closestinstrip(points,d,midx)


#Divide and conquer version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def divideAndConquerNearestNeighbor(points):
    minimum_distance = math.inf
    point1 = (-1,-1)
    point2 = (-1,-1)
    if len(points)<=5:
        return bruteForceNearestNeighbor(points)
    #endif
    points.sort(key=lambda points:points[0])
    mid=int(len(points)/2)
    (dl,pl,ql)=divideAndConquerNearestNeighbor(points[:mid])
    (dr,pr,qr)=divideAndConquerNearestNeighbor(points[mid:])
    minimum_distance=min(dl,dr)
    point1=pl if dl<dr else pr
    point2=ql if dl<dr else qr
    (dm,pm,qm)=closestInStrip(points,minimum_distance,points[mid][0])
    return (minimum_distance,point1,point2) if minimum_distance<=dm else (dm,pm,qm)
#end def divide_and_conquer(points):

#Brute force version of the nearest neighbor algorithm
#Input: points := unsorted array of (x,y) coordinates 
#   [(x,y),(x,y),...,(x,y)]
#Output: tuple of smallest distance and coordinates (distance,(x1,y1),(x2,y2))
def bruteForceNearestNeighbor(points):
    minimum_distance = math.inf;
    point1 = (-1,-1)
    point2 = (-1,-1)
    for i in points[:-1]:
        for j in points[points.index(i)+1:]:
            PointDistance=distance(i,j)
            if PointDistance<minimum_distance:
                minimum_distance=PointDistance
                point1=i
                point2=j
            #endif
        #endforj
    #endfori
    return (minimum_distance,point1,point2) if point1[0]<point2[0] else (minimum_distance,point2,point1) 
#end def brute_force_nearest_neighbor(points):

#Parse the input file
#Input: filename := string of the name of the test case
#Output: points := unsorted array of (x,y) coordinates
#   [(x,y),(x,y),...,(x,y)]
def parseFile(filename):
    points = []
    f = open(filename,'r') 
    lines = f.readlines()
    for line in lines:
        coordinate = line.split(' ')
        points.append((float(coordinate[0]),float(coordinate[1])))
    return points
#end def parse_file(filename):


#Main
#Input: filename  := string of the name of the test case
#       algorithm := flag for the algorithm to run, 'a': all 'b': brute force, 'd': d and c
def main(filename,algorithm):
    points = parseFile(filename)
    result = bruteForceResult = divideAndConquerResult = None
    if algorithm == 'a' or algorithm == 'b':
        #TODO: Insert timing code here
        bruteForceResult = bruteForceNearestNeighbor(points)
        cProfile.runctx('bruteForceNearestNeighbor(points)',{'bruteForceNearestNeighbor':bruteForceNearestNeighbor,'points':points},None)
    if algorithm == 'a' or algorithm == 'd':
        #TODO: Insert timing code here
        divideAndConquerResult = divideAndConquerNearestNeighbor(points)
        cProfile.runctx('divideAndConquerNearestNeighbor(points)',{'divideAndConquerNearestNeighbor':divideAndConquerNearestNeighbor,'points':points},None)       
    if algorithm == 'a': # Print whether the results are equal (check)
        if args.verbose:
            print('Brute force result: '+str(bruteForceResult))
            print('Divide and conquer result: '+str(divideAndConquerResult))
            print('Algorithms produce the same result? '+str(bruteForceResult == divideAndConquerResult))
        result = bruteForceResult if bruteForceResult == divideAndConquerResult else ('Error','N/A','N/A')
    else:  
        result = bruteForceResult if bruteForceResult is not None else divideAndConquerResult
    with open(os.path.splitext(filename)[0]+'_distance.txt','w') as f:
        f.write(str(result[1])+'\n')
        f.write(str(result[2])+'\n')
        f.write(str(result[0])+'\n')
#end def main(filename,algorithm):

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
#end if __name__ == '__main__':