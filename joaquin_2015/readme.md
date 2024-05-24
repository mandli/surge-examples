# Example of Storm Surge from Hurricane Joaquin
This example runs a simulation of Hurricane Joaquin from late September and early October 2015. Joaquin made landfall in the Bahamas in addition to passing close by Bermuda.

Running `make all` will compile all the necessary code to run the simulation.

# Topography
The file atlantic_1min.tt3 can be accessed in ../bathy/get_bathy.py or can be downloaded from https://www.dropbox.com/s/jkww7jm78azswk5/atlantic_1min.tt3.tar.bz2?dl=0.

# Gauges
Gauges 1-6 in the example correspond to six NOAA gauges along the US East Coast and in Bermuda. The `fetch_noaa_tide_data()` method is used to compare the simulated gauge data to real data in setplot.py. This comparison confirms that the surge observed along the East Coast during the period Joaquin hit was likely due to another storm system in the area at the time and not from Joaquin itself.

Gauges 7 and 8 are in the general vicinity of two sets of islands in the Bahamas where Joaquin made landfall. No time-based gauge data exists for these locations although a maximum surge height was [recorded after the storm passed](https://www.nhc.noaa.gov/data/tcr/AL112015_Joaquin.pdf).

For any questions contact Joshua Kapilian (jhk2199@columbia.edu).