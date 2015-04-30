#!/usr/bin/env python

"""Fetch relevant bathymetry for the Atlantic examples"""

import sys
import os

import clawpack.geoclaw.util as util

if __name__ == "__main__":

    # Override download location
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = os.getcwd()

    urls = ["https://dl.dropboxusercontent.com/u/8449354/bathy/gulf_caribbean.tt3.tar.bz2",
            "https://dl.dropboxusercontent.com/u/8449354/bathy/NOAA_Galveston_Houston.tt3.tar.bz2",
            "https://dl.dropboxusercontent.com/u/8449354/bathy/galveston_tx.asc.tar.bz2",
            "https://dl.dropboxusercontent.com/u/8449354/bathy/NewOrleans_3s.tt3.tar.bz2"]

    for url in urls:
        util.get_remote_file(url, output_dir=output_dir)