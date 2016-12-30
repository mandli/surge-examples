#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import datetime

import numpy
import scipy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

category_color = {5: 'red',
                  4: 'yellow',
                  3: 'orange',
                  2: 'green',
                  1: 'blue',
                  0: 'gray'}
mumbai = (72.8562, 19.0176)


def create_storm_file(storm):

    # Read in and create reference storm data
    with open("../../gulf/ike/ike.storm", 'r') as ref_storm_file:
        RRP = []
        max_winds = []
        central_pressure = []
        radius_max_winds = []
        for line in ref_storm_file:
            data = line.split(',')
            central_pressure.append(int(data[9]))
            max_winds.append(int(data[11]))
            RRP.append(int(data[18]))
            radius_max_winds.append(int(data[19]))

    ref_storm = {'max_winds': numpy.array(max_winds),
                 'central_pressure': numpy.array(central_pressure),
                 'radius_max_winds': numpy.array(radius_max_winds),
                 'RRP': numpy.array(RRP)}

    # Write new synthetic storm
    with open('mumbai.storm', 'w') as storm_file:
        # "(8x      i4  i2i2i26x    a4  2x,i3,1x,i4,a1,2x,i4,a1,2x,i3,2x,i4,47x,i3,2x,i3)"
        # "(8x      i4  i2i2i26x    a4  2xi3 xi4  a i4   a i3 2x,i4,47x,i3,2x,i3)"
        # "(        YYYYMMDDHH      BEST  FOR lat_D long_D max  cpre                                               rrp  rad"
        for n in xrange(len(storm['track'][0])):
            # AL, 00, HHHHMMDDHH,   , BEST,  0, LATN, LONW, XX, CPRE, TS,  , 0, 0, 0, 0,
            date = "%s%s%s%s" % (    storm['time'][n].year, 
                                 str(storm['time'][n].month).zfill(2),
                                 str(storm['time'][n].day).zfill(2),
                                 str(storm['time'][n].hour).zfill(2))
            storm_file.write("        %s" % date)
            if storm['track'][1][n] < 0:
                lat_dir = "S"
            else:
                lat_dir = "N"
            lon_dir = "W"
            storm_file.write("      XXXX  XXX  %s%s  %s%s" 
                                    % (str(int(storm['track'][1][n] * 10)).rjust(4), lat_dir,
                                       str(int(storm['track'][1][n] * 10)).rjust(4), lon_dir))
            storm_file.write("  %s" % str(int(storm['max_winds'][n])).rjust(3))
            storm_file.write("  %s" % str(int(storm['central_pressure'][n])).rjust(4))
            storm_file.write(" " * 47)
            storm_file.write("%s" % str(1e3).rjust(3))
            storm_file.write("  %s" % str(storm['radius_max_winds'][n]).rjust(3))
            storm_file.write('\n')


def plot_tracks(storms, plot_cat=True):

    if not isinstance(storms, list):
        storms = [storms]

    fig = plt.figure()
    axes = fig.add_subplot(1, 1, 1)
    coord = ((47.0, -10), (100.0, 31.0))
    mapping = Basemap(llcrnrlon=coord[0][0], llcrnrlat=coord[0][1],
                      urcrnrlon=coord[1][0], urcrnrlat=coord[1][1],
                      projection='lcc', lat_1=-10, lat_2=31, lon_0=75,
                      resolution='l', area_thresh=1000.0)

    # Plot storm tracks and intensity
    for storm in storms:
        longitude, latitude = mapping(storm['track'][0], storm['track'][1])
        for i in xrange(len(longitude)):
            if plot_cat:
                color = category_color[storm['category'][i]]
            else:
                color = 'red'
            mapping.plot(longitude[i:i+2], latitude[i:i+2], color=color)

    # Plot Mumbai's location
    mumbai = (72.8562, 19.0176)
    longitude, latitude = mapping(mumbai[0], mumbai[1])
    mapping.plot(longitude, latitude, 'bs')

    mapping.drawcoastlines()
    mapping.drawcountries()
    mapping.fillcontinents()
    mapping.drawparallels((0.0, 20.0), labels=[1, 1])
    mapping.drawmeridians(numpy.arange(coord[0][0], coord[1][0], 20),
                          labels=[0, 1, 1, 1])
    # axes.set_title('Typhoon Tracks')

    return fig


def storm_category(wind_speed):

    category = numpy.zeros(wind_speed.shape) + \
               (wind_speed >= 64) * (wind_speed < 83) * 1 + \
               (wind_speed >= 83) * (wind_speed < 96) * 2 + \
               (wind_speed >= 96) * (wind_speed < 113) * 3 + \
               (wind_speed >= 113) * (wind_speed < 135) * 4 + \
               (wind_speed >= 135) * 5
    return category


def extract_data(path, mask_dist=numpy.infty, mask_category=0):

    # Load the mat file and extract pertinent data
    import scipy.io
    mat = scipy.io.loadmat(path)

    lon = mat['longstore']
    lat = mat['latstore']
    hour = mat['hourstore']
    day = mat['daystore']
    month = mat['monthstore']
    year = mat['yearstore']
    radius_max_winds = mat['rmstore']
    max_winds = mat['vstore']
    central_pressure = mat['pstore']

    # Convert into storms and truncate zeros
    storms = []
    for n in xrange(lon.shape[0]):
        m = len(lon[n].nonzero()[0])

        distance = numpy.sqrt(  (lon[n, :m] - mumbai[0])**2
                              + (lat[n, :m] - mumbai[1])**2)

        storm = {'track': (lon[n, :m], lat[n, :m]),
                 'time': [datetime.datetime(year[0, n],
                                            month[n, i],
                                            day[n, i],
                                            hour[n, i]) for i in xrange(m)],
                 'max_winds': max_winds[n, :m],
                 'radius_max_winds': radius_max_winds[n, :m],
                 'central_pressure': central_pressure[n, :m],
                 'category': storm_category(max_winds[n, :m]),
                 'dist_mumbai': distance
                 }

        if (numpy.any(storm['dist_mumbai'] < mask_dist) and
            numpy.any(storm['category'] > mask_category)):

            storms.append(storm)

    return storms


if __name__ == '__main__':
    file_name = "Mumbai_IO_ncep_reanal.mat"
    base_path = os.path.expanduser("~/Dropbox/emmanuel_data/Mumbai_IO_ncep_reanal/")
    path = os.path.join(base_path, file_name)
    if len(sys.argv) > 1:
        path = sys.argv[1]

    storms = extract_data(path, mask_dist=0.5, mask_category=3)

    # plot_tracks(storms[10])
    # plot_tracks(storms[20])
    # plot_tracks(storms[30])
    # plot_tracks(storms[40])
    # plot_tracks(storms[50])
    # plot_tracks(storms[60])
    fig = plot_tracks(storms[70], plot_cat=False)
    fig.savefig('track.pdf')
    # plt.show()

    create_storm_file(storms[70])
