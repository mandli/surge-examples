#!/usr/bin/env python

"""Simple implementation of a file fetcher"""

import sys
import os
import urllib
import subprocess

def get_bathy(url, destination=os.getcwd(), force=False):
    r"""Get bathymetry file located at `url`

    Will check downloaded file's suffix to see if the file needs to be extracted
    """

    file_name = os.path.basename(url)
    output_path = os.path.join(destination, file_name)
    if not os.path.exists(output_path) or force:
        print "Downloading %s to %s..." % (url, output_path)
        urllib.urlretrieve(url, output_path)
        print "Finished downloading."
    else:
        print "Skipping %s, file already exists." % file_name

    tar = False
    gunzip = False
    split_file_name = file_name.split('.')
    if split_file_name[-1] == 'gz':
        gunzip = True
        if split_file_name[-2] == 'tar':
            tar = True
    if split_file_name[-1] == 'tgz':
        gunzip = True
        tar = True

    if gunzip or tar:
        print "Extracting %s" % file_name
        if gunzip and tar:
            subprocess.Popen('tar xvzf %s' % output_path, shell=True)
        elif gunzip:
            subprocess.Popen('gunzip %s' % output_path, shell=True)
        elif tar:
            subprocess.Popen('tar xvf %s' % output_path, shell=True)


if __name__ == "__main__":
    # Default URLs
    base_url = "http://users.ices.utexas.edu/~kyle/bathy/"

    # Override base_url
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    urls = [os.path.join(base_url, 'gulf_caribbean.tt3'),
            os.path.join(base_url, 'NOAA_Galveston_Houston.tt3'),
            os.path.join(base_url, 'galveston_tx.asc')]

    for url in urls:
        get_bathy(url)