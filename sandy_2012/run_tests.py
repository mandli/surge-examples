#!/usr/bin/env python

import os
import shutil
import gzip
import datetime

import numpy as np

import batch.batch
from clawpack.geoclaw.surge.storm import Storm
import clawpack.clawutil as clawutil

scratch_dir = os.path.join(os.environ["CLAW"], 'geoclaw', 'scratch')

str_val = lambda value: str(int(value * 10)).zfill(2)

class SandyJob(batch.batch.Job):

    def __init__(self, article=False, strength=1.0, sea_level=0.0):

        super(SandyJob, self).__init__()

        self.article = article
        self.strength = strength
        self.sea_level = sea_level

        self.type = "storm-surge"
        self.name = "sandy"
        self.prefix = f"S{str_val(self.strength)}_L{str_val(self.sea_level)}_A{str(self.article)[0]}"
        self.executable = "xgeoclaw"

        # Create base data object
        import setrun
        self.rundata = setrun.setrun()

        if self.article:
            recurrence = 24 * 4
        else:
            recurrence = 24
        clawdata = self.rundata.clawdata
        clawdata.num_output_times = int((clawdata.tfinal - clawdata.t0) *
                                                     recurrence / (60**2 * 24))

        self.rundata.geo_data.sea_level = self.sea_level

        # Storm
        # Handled when writing data objects below


    def __str__(self):
        output = super(SandyJob, self).__str__()
        output += f"  Strength: {self.strength}\n"
        output += f"  Sea-Level: {self.sea_level}\n"
        output += f"  Article: {self.article}\n"
        return output


    def write_data_objects(self):
        r""""""

        # Assume that we are in the data directory
        data = self.rundata.surge_data
        data_path = os.getcwd()
        data.storm_file = os.path.join(data_path, f"{self.prefix}.storm")

        # Write new storm out
        clawutil.data.get_remote_file("http://ftp.nhc.noaa.gov/atcf/archive/2012/bal182012.dat.gz")
        atcf_path = os.path.join(scratch_dir, "bal182012.dat")
        with gzip.open(".".join((atcf_path, 'gz')), 'rb') as atcf_file,    \
                open(atcf_path, 'w') as atcf_unzipped_file:
            atcf_unzipped_file.write(atcf_file.read().decode('ascii'))
        sandy = Storm(path=atcf_path, file_format="ATCF")
        sandy.time_offset = datetime.datetime(2012, 10, 29, 23, 30)
        # Increase strength of storm
        sandy.max_wind_speed = sandy.max_wind_speed * self.strength
        sandy.write(data.storm_file, file_format='geoclaw')

        # Write out all data files
        super(SandyJob, self).write_data_objects()


if __name__ == '__main__':

    jobs = []
    # Make sure to set this to True in setplot as well
    article = True
    for sea_level in [0.0, 0.25, 0.5]:
        for strength in [1.0, 1.1, 1.2, 1.25]:
            jobs.append(SandyJob(strength=strength, sea_level=sea_level, article=article))

    controller = batch.batch.BatchController(jobs)
    controller.wait = True
    controller.plot = True
    print(controller)
    controller.run()
