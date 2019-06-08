#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

import numpy
import scipy.io

import clawpack.geoclaw.surge.storm

# from batch.habanero import HabaneroJob as Job
# from batch.habanero import HabaneroBatchController as BatchController
from batch import Job, BatchController

import clawpack.geoclaw.surge.storm

def load_emmanuel_storms(path, mask_dist=numpy.infty, mask_category=0, 
                               location=None, t_offset=0.0):
    """Load storms from ensemble matlab file from Kerry Emmanuel

    :Input:
     - *mask_dist* (float)
     - *mask_category* (int)
     - *location* (tuple)

    :Output:
     - (list) List of storms that have been read from the file at *path* and 
       satisfy the filter criteria.

    """

    # Load and parse data from file
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

    # Assume that the shape of the lon array provides the number of storms
    num_storms = lon.shape[0]
    storms = []
    for n in range(num_storms):
        # Dimension of particular storm track
        m = len(lon[n].nonzero()[0])

        # Construct storm
        storm = clawpack.geoclaw.surge.storm.Storm()
        storm.t = 0.0

         # 'time': [datetime.datetime(year[0, n],
         #                            month[n, i],
         #                            day[n, i],
         #                            hour[n, i]) for i in xrange(m)],

        storm.eye_location = (lon[n, :m], lat[n, :m])
        storm.max_wind_speed = max_winds[n, :m]
        storm.max_wind_radius = radius_max_winds[n, :m]
        storm.central_pressure = central_pressure[n, :m]
        storm.storm_radius = numpy.ones(m) * 1e3

        # Filters - location
        if location is not None:
            distance = numpy.sqrt(  (lon[n, :m] - location[0])**2
                                  + (lat[n, :m] - location[1])**2)
            if distance > mask_dist:
                continue

        # Filters - category
        # if storm.category() < mask_category:
        #      continue

        storms.append(storm)


    return storms

class StormJob(Job):
    r"""Run a number of jobs specific to storm surge"""

    def __init__(self, storm, storm_number):
        r"""
        Initialize Habanero storm surge job

        See :class:`StormJob` for full documentation
        """

        super(StormJob, self).__init__()

        self.storm_number = storm_number
        self.storm = storm

        # Habanero queue settings
        self.omp_num_threads = 24
        self.time = "1:00:00"
        self.queue = ""

        # General job info
        self.type = "surge"
        self.name = "global_1"
        self.prefix = "storm_%s" % self.storm_number
        self.executable = "xgeoclaw"

        # Modify run data
        import setrun
        self.rundata = setrun.setrun()

        # Modify output times
        self.rundata.clawdata.output_style = 2
        recurrence = 6.0
        tfinal = (storm.t[-1] - storm.t[0]).total_seconds()
        N = int(tfinal / (recurrence * 60**2))
        self.rundata.clawdata.output_times = [t for t in
                 numpy.arange(0.0, N * recurrence * 60**2, recurrence * 60**2)]
        self.rundata.clawdata.output_times.append(tfinal)

        # Modify storm data
        surge_data = self.rundata.surge_data
        base_path = os.path.expandvars(os.path.join("$DATA_PATH", "storms",
                                                    "global", "storms"))
        surge_data.storm_file = os.path.join(base_path,
                                             'storm_%s.storm'
                                             % (str(i).zfill(5)))
        self.storm.time_offset = storm.t[0]

        print("Writing out GeoClaw storms...")
        self.storm.write(self.rundata.surge_data.storm_file)

        # TODO:  Figure out how to add gauges relative to storm track.  Probably
        #        need to limit these and perhaps detect landfall?

    def __str__(self):
        output = super(StormJob, self).__str__()
        output += "\n\tStorm %s:\n" % self.storm_number
        output += "\n\t\t%s" % self.storm
        output += "\n"
        return output

    def write_data_objects(self):

        super(StormJob, self).write_data_objects()


if __name__ == '__main__':
    print("Loading Emmanuel tracks...")
    path = os.path.expandvars(os.path.join("$DATA_PATH", "storms", "global",
                                           "Trial1_GB_dkipsl_rcp60cal.mat"))
    storms = load_emmanuel_storms(path)
    print("Done.")
    num_storms = len(storms)

    if len(sys.argv) > 1:
        # Take this to be the number of storms to run
        num_storms = int(sys.argv[1])

    # Convert Emmanuel data to GeoClaw format

    jobs = []
    for (i, storm) in enumerate(storms[:num_storms]):
        jobs.append(StormJob(storm, i))
    print("Done.")

    controller = BatchController(jobs)
    controller.wait = False
    controller.plot = False
    print(controller)
    # controller.run()
