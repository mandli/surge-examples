#!/usr/bin/env python

"""Download strips of the global bathymetry"""

import sys
import os

import matplotlib.pyplot as plt

import clawpack.clawutil.data as data
import clawpack.geoclaw.topotools as topotools


def form_etopo_URL(lower, upper, file_name="etopo1.nc", file_format="netcdf"):

    URL = "https://maps.ngdc.noaa.gov/mapviewer-support/wcs-proxy/wcs.groovy"
    URL += "?filename=%s" % file_name
    URL += "&request=getcoverage"
    URL += "&version=1.0.0"
    URL += "&service=wcs"
    URL += "&coverage=etopo1"
    URL += "&CRS=EPSG:4326"
    URL += "&format=%s" % file_format
    URL += "&resx=0.016666666666666667"
    URL += "&resy=0.016666666666666667"
    URL += "&bbox=%1.4f,%1.4f,%1.4f,%1.4f" % (lower[0], lower[1],
                                              upper[0], upper[1])
    return URL


def get_topo(output_dir=None, force=False, plot=False, verbose=False):
    """Retrieve ETOPO1 data from NOAA"""

    if output_dir is None:
        output_dir = os.getcwd()

    strips = [-45.0, -30.0, -15.0, 0.0, 15.0, 30.0]
    for (i, lower_bound) in enumerate(strips):
        file_name = "strip%s.nc" % i
        URL = form_etopo_URL([-180, lower_bound],
                             [180, lower_bound + 15.0],
                             file_name=file_name)
        file_path = os.path.join(output_dir, file_name)
        if os.path.exists(file_path) and (not force):
            print("Skipping download... file already exists: ", file_path)

        else:
            data.get_remote_file(URL, output_dir=output_dir,
                                      file_name=file_name,
                                      verbose=verbose,
                                      force=force)

            # TODO: Check output for errors

    if plot:
        fig = plt.figure()
        axes = fig.add_subplot(1, 1, 1)
        for i in range(len(strips)):
            topo = topotools.Topography(
                               path=os.path.join(output_dir, "strip%s.nc" % i))
            topo.read(stride=[100, 100])
            topo.plot(axes=axes)
        plt.show()


if __name__ == '__main__':
    plot = False
    if len(sys.argv) > 1:
        plot = bool(sys.argv[-1])
    get_topo(verbose=True, plot=plot)
