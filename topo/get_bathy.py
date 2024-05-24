#!/usr/bin/env python

"""Fetch relevant bathymetry for the storm surge examples"""

import argparse
import sys
import os

# Only import matplotlib if needed
# import matplotlib.pyplot as plt

# import clawpack.clawutil.data as data
# import clawpack.geoclaw.topotools as topotools

# Dictionary containing storm mappings to topography data files
storm_topo = {"global": None,
              "ike": ["carribean", "houston"],
              "katrina": ["carribean", "nola"]
             }


def plot_topo():
    pass


if __name__ == "__main__":

    # get_bathy.py [STORM_NAME(s)] --verbose --force --plot --output

    # Find unique set of topography files
    # Prompt whether to get the requested files (force option to just go do that)

    parser = argparse.ArgumentParser(prog="get_bathy", description="Fetch topography for each of the storms requested.", epilog="The dude abides.")
    parser.add_argument("storms", type=str, nargs="+", help="list of storms to fetch topography for")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose command output")
    parser.add_argument("-f", "--force", default=False, action="store_true", help="force command to proceed without asking")
    parser.add_argument("-p", "--plot", default=False, action="store_true", help="plot topography files that have been requested")
    parser.add_argument("-o", "--output", type=str, default=os.getcwd(), action="store", dest="output_dir", help="path to directory to place topography")
    args = parser.parse_args()

    # Handle request for all storms
    if 'all' in [value.lower() for value in args.storms]:
        args.storms = set(storm_topo.keys())

    # Reduce topography list to unique list
    topo_list = []
    for storm_name in args.storms:
        if storm_name not in storm_topo.keys():
            # Probably should just move on and ignore
            # raise ValueError()
            print("*** Warning: {} was not a known storm.".format(storm_name))
        else:
            if storm_name.lower() == "global":
                # Handle this special case
                topo_list.append("global_strips")
            else:
                for topo_file in storm_topo[storm_name]:
                    topo_list.append(topo_file)
    topo_list = set(topo_list)

    # Print out helpful message on list of topography files we will fetch
    # Probably just describe what we are about to do
    print("{} -> {}".format(args.storms, topo_list))

    # Query user to continue
    if not args.force:
        value = input("Continue ([yes]/no): ")
        if len(value) == 0:
            value = 'y'
        if not value[0].lower() == "y":
            sys.exit(0)

    for topo_file in topo_list:
        # Fetch file
        if topo_file == "global":
            print("Fetching strips for global topography.")
        else:
            print("Fetching {}".format(topo_file))

    if args.plot:
        print("Plotting topography...")
