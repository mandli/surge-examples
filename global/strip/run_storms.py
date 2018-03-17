#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

# from batch.habanero import HabaneroJob as Job
# from batch.habanero import HabaneroBatchController as BatchController
from batch import Job, BatchController

import clawpack.geoclaw.surge.storm


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

        # Modify storm data
        import setrun
        self.rundata = setrun.setrun()

        surge_data = self.rundata.surge_data
        surge_data.storm_file = 'storm_%s.storm' % (str(i).zfill(5))
        self.storm.time_offset = storm.t[0]

    def __str__(self):
        output = super(StormJob, self).__str__()
        output += "\n\tStorm %s:\n" % self.storm_number
        output += "\n\t\t%s" % self.storm
        output += "\n"
        return output

    def write_data_objects(self):
        storm.write(self.rundata.surge_data.storm_file)

        super(StormJob, self).write_data_objects()


if __name__ == '__main__':
    print("Loading Emmanuel tracks...")
    path = os.path.expandvars(os.path.join("$DATA_PATH", "storms", "global",
                                           "Trial1_GB_dkipsl_rcp60cal.mat"))
    storms = clawpack.geoclaw.surge.storm.load_emmanuel_storms(path)
    print("Done.")
    num_storms = len(storms)
    # Temporary override
    num_storms = 2

    if len(sys.argv) > 1:
        # Take this to be the number of storms to run
        num_storms = 10

    # Convert Emmanuel data to GeoClaw format
    print("Writing out GeoClaw storms...")
    jobs = []
    for (i, storm) in enumerate(storms[:num_storms]):
        jobs.append(StormJob(storm, i))
    print("Done.")

    controller = BatchController(jobs)
    controller.wait = False
    controller.plot = False
    print(controller)
    controller.run()
