from __future__ import absolute_import
from __future__ import print_function

import os

import numpy as np
import math

from clawpack.geoclaw.surge.storm import Storm
import clawpack.clawutil as clawutil
from clawpack.geoclaw import topotools

##### 
# to automatically place your gauges, first add your topography
# and storm files below. Then, in setrun, import this module ("import auto_gauges")
# and call "auto_gauges.return_gauge_points(rundata)" to place gauges
#####

## directory where your data is
DATA = os.path.join(os.environ.get('DATA_DIR', os.getcwd()))

####
# make topography file(s) into topo objects (topotools.Topography()) and
# add to topofiles list
####
topofiles = []

for n in range(1,13):
    topo = topotools.Topography()
    topo.read('../topofilesagain/world_' + str(n) + '.tt3', topo_type=3)
    topofiles.append(topo)

## replace with your storm
storm=Storm('./00009.storm', file_format='geoclaw')

## finds the nearest points to the storm on the shoreline by using topotools 
## makeshoreline method and finding the minimum distance from the eyelocation 
## of the storm and the shoreline

## if read in storm as atcf file, use this method:
# def points_on_shoreline(storm):
    
#     shoreline = []
    
#     for n in topofiles:
#         for i in n.make_shoreline_xy():
#             shoreline.append(i)
    
#     sub_sample_storm = storm.eye_location[::3] 
#     # this takes every third coordinate, for more gauges decrease steps,
#     # for less gauges increase steps

#     points = np.empty([len(sub_sample_storm), 2])
    
#     count = 0
    
#     for n in sub_sample_storm:
    
#         nearest_shore = near_shoreline(n[0], n[1], shoreline)
        
#         points[count] = (shoreline[nearest_shore])
#         count = count + 1
        
    
#     return points

## if storm file is read in as geoclaw file, use this method:

def points_on_shoreline(storm):
    
    location_x = storm.eye_location[0]
    
    location_y = storm.eye_location[1]
    
    shoreline = []
    
    for n in topofiles:
        for i in n.make_shoreline_xy():
            shoreline.append(i)

    points = np.empty([len(location_y), 2])
    
    count = 0
    
    for n in range(0, len(points)):
    
        nearest_shore = near_shoreline(location_x[n], location_y[n], shoreline)
        
        points[count] = (shoreline[nearest_shore])
        count = count + 1
        
    
    return points


## returns shoreline closest to storm by calculating distance
## between storm coordinate and every point on shoreline
def near_shoreline(storm_x, storm_y, shoreline):
    
    dis = []
    
    for n in shoreline:
        dis.append((distance(storm_x, storm_y, n[0], n[1])))
        
    minimum = dis.index(min(dis))
    return minimum
 
    
## find distance between two points by using haversine formula    
def distance(x1, y1, x2, y2):
    
    # convert to radians
    x1 = x1*math.pi/180
    x2 = x2*math.pi/180
    y1 = y1*math.pi/180
    y2 = y2*math.pi/180
    
    distance = 2*6378.137*np.arcsin(math.sqrt(math.sin((y2-y1)/2)**2 + math.cos(y1)*math.cos(y2)*(math.sin((x2-x1)/2)**2)))
    
    return distance

## returns the index of the closest values in the topo arrays to the desired coordinate 
def index(array, float_num):    
    
    for n,k in enumerate(array):
        
        if(math.isclose(k, float_num)):
            return n
        
        if(array[n-1] < float_num < array[n]):
            if(abs(float_num - array[n-1]) < abs(float_num - array[n])):
                return n - 1
            else:
                return n
            
## finds which topography file contains point we're looking for            
def which_topo(topo_array, point):   
    count = 0
    for n in topo_array:
        if(index(n.x, point[0]) != None and index(n.y, point[1]) != None):
            array_index = count
            return array_index
        else:
            count += 1


## using bilinear interpolation, finds bilinear function by finding coefficients
## based on this wikipedia page: https://en.wikipedia.org/wiki/Bilinear_interpolation
def equation_from_bilinear_interpolation(x, y, x_array, y_array, z_array, x_min, x_max, y_min, y_max):
    
    x_index = index(x_array, x)
    y_index = index(y_array, y)
    x_1 = x_index
    y_1 = y_index
    
    
    x_2 = x_index - 1
    y_2 = y_index - 1        
            
    z11 = z_array[y_1, x_1]
    z12 = z_array[y_1, x_2]
    z21 = z_array[y_2, x_1]
    z22 = z_array[y_2, x_2]
    
    x1 = x_array[x_1]
    y1 = y_array[y_1]
    x2 = x_array[x_2]
    y2 = y_array[y_2]
    
        
    # finding equation of format f(x,y) = a0 + a1x + a2y + a3xy
    
    a0 = (z11*x2*y2 + z22*x1*y1)/((x1-x2)*(y1-y2)) + \
        (z12*x2*y1 + z21*x1*y2)/((x1-x2)*(y2-y1)) 
        
    a1 = (z11*y2 + z22*y1)/((x1-x2)*(y2-y1)) + \
       (z12*y1 + z21*y2)/((x1-x2)*(y1-y2))
    
    a2 = (z11*x2 + z22*x1)/((x1-x2)*(y2-y1)) + \
       (z12*x2 + z21*x1)/((x1-x2)*(y1-y2))
    
    a3 = (z11 + z22)/((x1-x2)*(y1-y2)) + \
       (z12 + z21)/((x1-x2)*(y2-y1))
        
    coefficients = [a0, a1, a2, a3]
    
    return integrate_bilinear_function(coefficients, x_min, x_max, y_min, y_max)


## integrates the bilinear function
def integrate_bilinear_function(coefficients_array, x_min, x_max, y_min, y_max):
    
    a0 = coefficients_array[0]
    a1 = coefficients_array[1]
    a2 = coefficients_array[2]
    a3 = coefficients_array[3]
    
    value_y_max = a0*(x_max - x_min)*y_max + \
                (a1/2)*(x_max**2 - x_min**2)*y_max + \
                (a2/2)*(x_max - x_min)*(y_max**2) + \
                (a3/4)*(x_max**2 - x_min**2)*(y_max**2)
    
    value_y_min = a0*(x_max - x_min)*y_min + \
                (a1/2)*(x_max**2 - x_min**2)*y_min + \
                (a2/2)*(x_max - x_min)*(y_min**2) + \
                (a3/4)*(x_max**2 - x_min**2)*(y_min**2)
    
    return value_y_max - value_y_min
    
## appends the gauge points
## to find the gauge points, first an array of points on the coast were found
## then, the resolution at each point was increased
## we then predict the z value, or the depth/height at that point by integrating
## and then dividing by the area (the grid cell size was made 0.008 since 
## 0.008 degrees approx = 1 km) 
## if the predicted z < 0, which is sea level, this point is on the water and 
## a gauge is placed there
def return_gauge_points(rundata):
    
    points_gauges = []    

    points_coast = points_on_shoreline(storm)
    
    for n in points_coast:
        
        rundata.regiondata.regions.append([15,15,rundata.clawdata.t0,rundata.clawdata.tfinal, \
        n[0] + 0.01, n[0] -0.01, n[1] + 0.01, n[1] -0.01]) ## refine data as much as possible
       
        topo = topofiles[which_topo(topofiles, n)]
    
        integral = equation_from_bilinear_interpolation(n[0], n[1], topo.x, topo.y, topo.Z, \
                                                       n[0] - 0.008, n[0] + 0.008, n[1] - 0.008, n[1] + 0.008)  
    
        z_predicted = integral/((0.008*2)**2)
    
        if (z_predicted < 0):
            points_gauges.append(n)
   
    for k, n in enumerate(points_gauges):

        rundata.gaugedata.gauges.append([(k+1), n[0] , n[1],
                                         rundata.clawdata.t0,
                                         rundata.clawdata.tfinal])
