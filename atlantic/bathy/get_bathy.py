#!/usr/bin/env python

"""Fetch relevant bathymetry for the Atlantic examples"""

import sys
import os

import clawpack.clawutil.data as data

if __name__ == "__main__":

    # Override download location
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = os.getcwd()

    urls = ["https://www.dropbox.com/s/jkww7jm78azswk5/atlantic_1min.tt3.tar.bz2?dl=0",
            "https://www.dropbox.com/s/vafi7k6zqn5cfs1/newyork_3s.tt3.tar.bz2?dl=0"]

    for url in urls:
        data.get_remote_file(url, output_dir=output_dir)