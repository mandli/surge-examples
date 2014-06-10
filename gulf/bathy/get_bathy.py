#!/usr/bin/env python

"""Simple implementation of a file fetcher"""

import sys
import os
import urllib
import tarfile

def strip_archive_extensions(path, extensions=["tar", "tgz", "bz2", "gz"]):
    r"""
    Strip off archive extensions defined in *extensions* list.

    Return stripped path calling this function recursively until all splitext
    does not provide an extension in the *extensions* list.

    """

    if os.path.splitext(path)[-1][1:] in extensions:
        return strip_archive_extensions(os.path.splitext(path)[0])
    else:
        return path


def get_remote_file(url, destination=os.getcwd(), force=False, verbose=False):
    r"""Get bathymetry file located at `url`

    Will check downloaded file's suffix to see if the file needs to be extracted
    """

    file_name = os.path.basename(url)
    output_path = os.path.join(destination, file_name)
    unarchived_output_path = strip_archive_extensions(output_path)

    if not os.path.exists(unarchived_output_path) or force:
        if not os.path.exists(output_path):
            if verbose:
                print "Downloading %s to %s..." % (url, output_path)
            urllib.urlretrieve(url, output_path)
            if verbose:
                print "Done downloading."

        if tarfile.is_tarfile(output_path):
            if verbose:
                print "Un-archiving %s to %s..." % (output_path, unarchived_output_path)
            with tarfile.open(output_path, mode="r:*") as tar_file:
                tar_file.extractall(path=destination)
            if verbose:
                print "Done un-archiving."
    else:
        if verbose:
            print "Skipping %s because it already exists locally." % url


if __name__ == "__main__":
    # Default URLs
    base_url = "http://users.ices.utexas.edu/~kyle/bathy/"

    # Override base_url
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    urls = [os.path.join(base_url, 'gulf_caribbean.tt3.tar.bz2'),
            os.path.join(base_url, 'NOAA_Galveston_Houston.tt3.tar.bz2'),
            os.path.join(base_url, 'galveston_tx.asc.tar.bz2'),
            os.path.join(base_url, 'NewOrleans_3s.tt3.tar.bz2')]

    for url in urls:
        get_remote_file(url, verbose=True)