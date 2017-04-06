#!/usr/bin/env python

"""Fetch relevant bathymetry for the Atlantic examples"""

import sys
import os

import clawpack.geoclaw.util as util
import clawpack.geoclaw.topotools as topotools

def convert_netcdf_file(path, file_name="indian_ocean_conv.nc"):
    r"""Needed to rename variables in indian ocean topography"""

    indian_ocean_topo = topotools.Topography("indian_ocean.nc", topo_type=4)
    indian_ocean_topo.read(nc_params={"x_var":"lon", 
                                      "y_var":"lat", 
                                      "z_var":"Band1"})

    indian_ocean_topo.write(file_name, topo_type=4)


if __name__ == "__main__":

    # Override download location
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = os.getcwd()

    # urls = [""]

    # for url in urls:
    #     util.get_remote_file(url, output_dir=output_dir)

    convert_netcdf_file(os.path.join(os.getcwd(), "indian_ocean.nc"))