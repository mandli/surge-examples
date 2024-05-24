#!/usr/bin/env python

import os
import sys
import datetime

import scipy.io
import numpy as np

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

import clawpack.amrclaw.data as amrclaw
import clawpack.visclaw.gaugetools as gaugetools

# Conversion shortcuts
days2seconds = lambda days: days * 60.0**2 * 24.0
date2seconds = lambda date: days2seconds(date.days) + date.seconds
seconds2days = lambda secs: secs / (24.0 * 60.0**2)
min2deg = lambda minutes: minutes / 60.0
ft2m = lambda x:0.3048 * x

def read_tide_gauge_data(base_path, skiprows=5, verbose=True):
    r"""Read the gauge info data file.

    Returns a dictionary for each gauge in the table.
      Keys: 'location': (tuple), 'depth': float, 'gauge_no': int
            'mean_water': (ndarray), 't': (ndarray)

    """
    stations = {}
    station_info_file = open(os.path.join(base_path,'Ike_Gauges_web.txt'),'r')

    # Skip past header
    for i in range(skiprows):
        station_info_file.readline()

    # Read in each station
    for line in station_info_file:
        data_line = line.split()
        if data_line[6] == "OK":
            stations[data_line[0]] = {
                    'location':[float(data_line[4]) + min2deg(float(data_line[5])),
                                float(data_line[2]) + min2deg(float(data_line[3]))],
                         'depth':float(data_line[8]) + float(data_line[9]),
                      'gauge_no':0}
            if data_line[1] == '-':
                stations[data_line[0]]['gauge_no'] = ord(data_line[0])
            else:
                stations[data_line[0]]['gauge_no'] = int(data_line[1])
            if verbose:
                print("Station %s: %s" % (data_line[0],stations[data_line[0]]))
            
            # Load and extract real station data
            data = scipy.io.loadmat(os.path.join(base_path,'result_%s.mat' % data_line[0]))
            stations[data_line[0]]['t'] = data['yd_processed'][0,:]
            stations[data_line[0]]['mean_water'] = data['mean_water'].transpose()[0,:]

    station_info_file.close()

    return stations


def read_adcirc_gauge_data(only_gauges=None, base_path="", verbose=True):
    r""""""

    if only_gauges is None:
        gauge_list = [120, 121, 122, 123]
    else:
        gauge_list = only_gauges

    gauge_file_list = [os.path.join(base_path, "stat%s.dat" % str(i).zfill(4)) 
                 for i in gauge_list]

    stations = {}
    for (i,gauge_file) in enumerate(gauge_file_list):
        data = np.loadtxt(gauge_file)
        stations[i+1] = data
        if verbose:
            print("Read in ADCIRC gauge file %s" % gauge_file)

    return stations


def load_geoclaw_gauge_data(only_gauges=None, base_path="_output", verbose=True):
    r"""Load all gauge data in gauge file at base_path/fort.gauge

    Returns a dictionary of GaugeSolution objects keyed by their gauge numbers.
    """

    gauges = {}

    # Read in gauge.data file
    gauge_info_file = amrclaw.GaugeData()
    gauge_info_file.read(data_path=base_path,file_name='gauges.data')

    if only_gauges is None:
        gauge_list = gauge_info_file.gauge_numbers
    else:
        gauge_list = only_gauges

    locations = {}
    for (n,gauge) in enumerate(gauge_info_file.gauges):
        locations[gauge[0]] = gauge[1:3]

    # Read in each gauge solution
    import time
    import sys
    start = time.clock()

    # Read in all gauges
    try:
        file_path = os.path.join(base_path,'fort.gauge')
        if not os.path.exists(file_path):
            print('*** Warning: cannot find gauge data file %s'%file_path)
            pass
        else:
            print("Reading gauge data from %s" % file_path)
            raw_data = np.loadtxt(file_path)

            gauge_read_string = ""
            raw_numbers = np.array(raw_data[:,0], dtype=int)    # Convert type for equality comparison
            for n in gauge_list:
                gauge = gaugetools.GaugeSolution(n, 
                                                 location=locations[n])
                gauge_indices = np.nonzero(n == raw_numbers)[0]

                gauge.level = [int(value) for value in raw_data[gauge_indices,1]]
                gauge.t = raw_data[gauge_indices,2]
                gauge.q = raw_data[gauge_indices,3:].transpose()
                gauge.number = n
                gauge_read_string = " ".join((gauge_read_string,str(n)))

                gauges[n] = gauge

            if verbose:
                print("Read in GeoClaw gauge [%s]" % gauge_read_string[1:])
        
    except Exception as e:
        print('*** Error reading gauges in ClawPlotData.getgauge')
        print('*** outdir = ', base_path)
        raise e

    # for (i,gauge_no) in enumerate(gauge_list):
    #     gauge = gaugetools.GaugeSolution(gauge_no, location=gauge_info_file.gauges[i][1:3])
    #     gauge.read(output_path=base_path, file_name='fort.gauge')
    #     gauges[gauge_no] = gauge


    elapsed = (time.clock() - start)
    print("Single gauge reading elapsed time = %s" % elapsed)
    
    start = time.clock()
    raw_data = np.loadtxt(os.path.join(base_path,'fort.gauge'))
    raw_numbers = np.array([int(value) for value in raw_data[:,0]])
    for n in gauge_list:
        gauge = gaugetools.GaugeSolution(n, 
                                         location=locations[n])
        gauge_indices = np.nonzero(n == raw_numbers)[0]

        gauge.level = [int(value) for value in raw_data[gauge_indices,1]]
        gauge.t = raw_data[gauge_indices,2]
        gauge.q = raw_data[gauge_indices,3:].transpose()
        # gauge_read_string = " ".join((gauge_read_string,str(n)))

        # self.gaugesoln_dict[(n, outdir)] = gauge

    elapsed = (time.clock() - start)
    print("All gauges reading elapsed time = %s" % elapsed)
    return gauges


def plot_comparison(gauge_path, adcirc_path, geoclaw_path, single_plot=True, format='png'):

    # Parameters
    surface_offset = [0.0, 0.0]
    landfall = []
    landfall.append(datetime.datetime(2008,9,13 + 1,7) 
                                                - datetime.datetime(2008,1,1,0))
    landfall.append(datetime.datetime(2008,9,13 - 1,7) 
                                                - datetime.datetime(2008,1,1,0))
    landfall.append(days2seconds(4.25))

    # Gauge name translation
    gauge_name_trans = {"W":1, "X":2, "Y":3, "Z":4}

    # Load gauge data
    kennedy_gauges = read_tide_gauge_data(gauge_path)
    keys = kennedy_gauges.keys()
    for gauge_label in keys:
        if kennedy_gauges[gauge_label]['gauge_no'] not in [1, 2, 3, 4]:
            kennedy_gauges.pop(gauge_label)
    gauge_list = [gauge['gauge_no'] for gauge in kennedy_gauges.itervalues()]

    adcirc_gauges = read_adcirc_gauge_data(base_path=
                                           os.path.join(adcirc_path,'old_data'))
    new_adcirc_gauges = read_adcirc_gauge_data(base_path=
                                           os.path.join(adcirc_path,'new_data'))
    geoclaw_gauges = load_geoclaw_gauge_data(base_path=geoclaw_path,
                                             only_gauges=gauge_list)

    # Plot each matching gauge
    if single_plot:
        fig = plt.figure(figsize=(16,10),dpi=80)
        fig.suptitle('Surface from Sea Level')
    index = 0
    for (name,kennedy_gauge) in kennedy_gauges.iteritems():
        geoclaw_gauge = geoclaw_gauges[kennedy_gauge['gauge_no']]
        adcirc_gauge = adcirc_gauges[kennedy_gauge['gauge_no']]
        new_adcirc_gauge = new_adcirc_gauges[kennedy_gauge['gauge_no']]
        index = index + 1
        if single_plot:
            axes = fig.add_subplot(2,len(kennedy_gauges)/2,index)
        else:
            fig = plt.figure(figsize=(8,4))
            # 16 / 10 = 4 / 2
            # fig.suptitle('Surface from Sea Level')
            axes = fig.add_subplot(111)

        # Plot actual gauge data
        axes.plot(kennedy_gauge['t'] - seconds2days(date2seconds(landfall[0])),
                  kennedy_gauge['mean_water'] + kennedy_gauge['depth'], '-', 
                  label="Gauge Data")

        # Plot GeoClaw gauge data
        axes.plot(seconds2days(geoclaw_gauge.t - date2seconds(landfall[1])),
                  geoclaw_gauge.q[3,:] + surface_offset[0], '--', 
                  label="GeoClaw")

        # Plot ADCIRC gauge data
        # axes.plot(seconds2days(adcirc_gauge[:,0] - landfall[2]),
        #           adcirc_gauge[:,1] + surface_offset[1], 'g', 
        #           label="ADCIRC[1]")

        # Plot new ADCIRC gauge data
        axes.plot(seconds2days(new_adcirc_gauge[:,0] - landfall[2]),
                  new_adcirc_gauge[:,1] + surface_offset[1], '..', 
                  label="ADCIRC")
                  # label="ADCIRC[2]")

        # Plot new ADCIRC gauge data

        axes.set_xlabel('Landfall Day')
        axes.set_ylabel('Surface (m)')
        axes.set_title("Station %s" % gauge_name_trans[name])
        axes.set_xticks([-2,-1,0,1,2])
        axes.set_xticklabels([-2,-1,0,1,2])
        axes.set_xlim([-2,2])
        axes.set_ylim([-1,5])
        axes.grid(True)
        axes.legend()

        if not single_plot:
            plt.savefig("gauge%s.%s" % (kennedy_gauge['gauge_no'],format))

    plt.savefig("tide_gauge_comparison.%s" % format)
    return fig


if __name__ == '__main__':
    kennedy_gauge_path = './gauge_data'
    geoclaw_output_path = "./_output"
    adcirc_gauge_path = "./gauge_data"
    if len(sys.argv) > 1:
        geoclaw_output_path = sys.argv[1]
        if len(sys.argv) > 2:
            kennedy_gauge_path = sys.argv[2]

    # Plot Andrew Kennedy's gauge data versus corresponding GeoClaw data
    figure = plot_comparison(kennedy_gauge_path, adcirc_gauge_path, 
                             geoclaw_output_path, single_plot=False)
    plt.show()