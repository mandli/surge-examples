#!/usr/bin/env python

"""Fetch relevant bathymetry for the storm surge examples"""

import sys
import os

import matplotlib.pyplot as plt

import clawpack.clawutil.data as data
import clawpack.geoclaw.topotools as topotools

# These are the URLs to the topography needed to run each storm
topo_urls = {"sandy": ["https://www.dropbox.com/s/jkww7jm78azswk5/atlantic_1min.tt3.tar.bz2?dl=0",
                       "https://www.dropbox.com/s/vafi7k6zqn5cfs1/newyork_3s.tt3.tar.bz2?dl=0"],
             "irene": ["https://www.dropbox.com/s/jkww7jm78azswk5/atlantic_1min.tt3.tar.bz2?dl=0",
                       "https://www.dropbox.com/s/vafi7k6zqn5cfs1/newyork_3s.tt3.tar.bz2?dl=0"],
             "isabel": ["https://www.dropbox.com/s/jkww7jm78azswk5/atlantic_1min.tt3.tar.bz2?dl=0",
                        "chesapeake.nc"],
             "florence": ["https://www.dropbox.com/s/jkww7jm78azswk5/atlantic_1min.tt3.tar.bz2?dl=0"]
            }

# Etopo support
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


def plot_topo(path, stride=[1, 1], axes=None):
    """"""
    
    if axes is None:
        fig, axes = plt.subplots(1, 1)

    topo = topotools.Topography(path=path)


    for i in range(len(strips)):
        topo = topotools.Topography(
                           path=os.path.join(output_dir, "strip%s.nc" % i))
        topo.read(stride=stride)
        topo.plot(axes=axes)
    
    return axes


if __name__ == "__main__":

    # Input:  Storm names, location to download to, plot, verbose 
    #
    #
    #

    output_dir = os.getwcd()
    force = False
    verbose = False


    # Override download location
    if len(sys.argv) > 1:
        storm_names = sys.argv[1:]
    else:
        # TODO: Add better failure
        sys.exit()

    if name == "global_strip":
        strips = [-45.0, -30.0, -15.0, 0.0, 15.0, 30.0]
        for (i, lower_bound) in enumerate(strips):
            file_name = "strip%s.nc" % i
            urls.append(form_etopo_URL([-180, lower_bound],
                                       [180, lower_bound + 15.0]))
            # TODO specify file name

        storm_names.pop("global_strip")

    # Construct list of downloads
    urls = []
    for name in storm_names:
        urls.append(topo_urls[name])

    for url in urls:
        data.get_remote_file(url, output_dir=output_dir, verbose=verbose, force=force)
