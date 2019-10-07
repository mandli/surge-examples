#!/usr/bin/env python

"""Script for plotting number of cells or grids in time
"""

from __future__ import print_function

import os
import sys
import glob
import datetime

import numpy

# Plot customization
import matplotlib

# Markers and line widths
matplotlib.rcParams['lines.linewidth'] = 2.0
matplotlib.rcParams['lines.markersize'] = 6
matplotlib.rcParams['lines.markersize'] = 8

# Font Sizes
matplotlib.rcParams['font.size'] = 16
matplotlib.rcParams['axes.labelsize'] = 16
matplotlib.rcParams['legend.fontsize'] = 12
matplotlib.rcParams['xtick.labelsize'] = 16
matplotlib.rcParams['ytick.labelsize'] = 16

# DPI of output images
matplotlib.rcParams['savefig.dpi'] = 300

import matplotlib.pyplot as plt

convert2rgbfloat = lambda rgb: [value / 256.0 for value in rgb]
days2seconds = lambda days: days * 60.0**2 * 24.0
seconds2days = lambda seconds: seconds / (60.0**2 * 24.0)

def get_num_cells_grids(output_path="./_output"):

    MAX_LEVELS = 10

    num_files = len(glob.glob(os.path.join(output_path, "fort.q*")))

    time = numpy.empty(num_files, dtype=float)
    num_grids = numpy.zeros((num_files, MAX_LEVELS), dtype=int)
    num_cells = numpy.zeros((num_files, MAX_LEVELS), dtype=int)
    num_levels = 0

    for n in range(num_files):
        # Read t file
        path = os.path.join(output_path, "fort.t%s" % (str(n).zfill(4)))
        with open(path, 'r') as t_file:
            time[n] = seconds2days(float(t_file.readline().split()[0]))
            t_file.readline()
            t_file_num_grids = int(t_file.readline().split()[0])

        # Read q_file
        path = os.path.join(output_path, "fort.q%s" % (str(n).zfill(4)))
        with open(path, 'r') as q_file:
            line = "\n"
            while line != "":
                line = q_file.readline()
                if "grid_number" in line:
                    # print "grid number:", int(line.split()[0])
                    level = int(q_file.readline().split()[0])
                    num_levels = max(level, num_levels)
                    num_grids[n,level - 1] += 1 
                    mx = int(q_file.readline().split()[0])
                    my = int(q_file.readline().split()[0])
                    num_cells[n,level - 1] += mx * my

        # File checking
        if numpy.sum(num_grids[n,:]) != t_file_num_grids:
            raise ValueError("Number of grids in fort.t* file and fort.q*"
                             " file do not match.")

    return num_levels, time, num_grids, num_cells


def plot_num_cells_grids(num_levels, time, num_grids, num_cells):
    
    # Plot cascading time histories per level
    colors = [ (value / 256.0, value / 256.0, value / 256.0) 
                                for value in [247, 217, 189, 150, 115, 82, 37] ]
    proxy_artists = [plt.Rectangle((0, 0), 1, 1, fc=colors[level], 
            label="Level %s" % (str(level+1))) for level in range(num_levels)]

    # Number of grids
    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.set_yscale('log')
    axes.stackplot(time ,num_grids.transpose(), colors=colors)
    axes.set_xlabel('Days from landfall')
    plt.subplots_adjust(left=0.13, bottom=0.12, right=0.90, top=0.90)
    set_day_ticks()
    axes.set_ylabel('Number of Grids')
    axes.set_title("Number of Grids per Level in Time")
    axes.legend(proxy_artists, ["Level %s" % (str(level+1)) 
                                    for level in range(num_levels)], loc=2)
    axes.set_ylim(bottom=0.0)
    axes.set_xlim([-3,1])
    fig.savefig("num_grids.png")

    # Number of cells
    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.set_yscale('log')
    axes.stackplot(time, num_cells.transpose(), colors=colors)
    set_day_ticks()
    plt.subplots_adjust(left=0.13, bottom=0.12, right=0.90, top=0.90)
    axes.set_xlabel('Days from landfall')
    axes.set_ylabel('Number of Cells')
    axes.set_title("Number of Cells per Level in Time")
    axes.legend(proxy_artists, ["Level %s" % (str(level+1)) 
                                    for level in range(num_levels)], loc=2)
    axes.set_ylim(bottom=0.0) 
    axes.set_xlim([-3,1]) 
    fig.savefig("num_cells.png")

    plt.show()


def set_day_ticks(new_ticks=[-3, -2, -1, 0, 1]):
    plt.xticks(new_ticks, [str(tick) for tick in new_ticks])


if __name__ == "__main__":

    output_path = "./_output"    
    verbose = False
    if len(sys.argv) > 1:
        output_path = sys.argv[1]


    num_levels, time, num_grids, num_cells = get_num_cells_grids(output_path)
    if verbose:
        print(num_levels, time, num_grids, num_cells)
    plot_num_cells_grids(num_levels, time, num_grids, num_cells)
