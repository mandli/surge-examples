# Hurricane Lili 2002 Storm Report

This example contains the data and setup for running a storm surge forecast for Hurricane Lili.

## Hurricane Lili:

Hurricane Lili was the second costliest, deadliest, and strongest hurricane of the 2002 Atlantic hurricane season, only surpassed by Hurricane Isidore, which affected the same areas around a week before Lili. Lili was the twelfth named storm, fourth hurricane, and second major hurricane of the 2002 Atlantic hurricane season. The storm developed from a tropical disturbance in the open Atlantic on September 21. It continued westward, affecting the Lesser Antilles as a tropical storm, then entered the Caribbean. As it moved west, the storm dissipated while being affected by wind shear south of Cuba, and regenerated when the vertical wind shear weakened. It turned to the northwest and strengthened up to category 2 strength on October 1. Lili made two landfalls in western Cuba later that day, and then entered the Gulf of Mexico. The hurricane rapidly strengthened on October 2, reaching Category 4 strength that afternoon. It weakened rapidly thereafter, and hit Louisiana as a Category 1 hurricane on October 3. It moved inland and dissipated on October 6

Source: NOAA Tropical Cyclone Report (https://en.wikipedia.org/wiki/Hurricane_Lili)

## Clawpack Installation:

Clawpack requires python(python3), fortran complier, and some environment variable setted to run. Detailed installation instruction found here: https://www.clawpack.org/installing.html

## Storm data:

Data for Clawpack to run simulation was taken from NOAA's storm data archive: https://ftp.nhc.noaa.gov/atcf/archive/2002/

Hurricane Lili storm data was located in bal132002.dat.gz  

In setrun.py, one can retrieve data directly from source by writing a code similar to this:

setrun.py:
line 441

    # Convert ATCF data to GeoClaw format
    clawutil.data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2002/bal132002.dat.gz")
    atcf_path = os.path.join(scratch_dir, "bal132002.dat")

## Topography

Topography data is automatically downloaded from the Columbia databases at:
http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

setrun.py:

line 408
    
topo_path = os.path.join(scratch_dir, 'gulf_caribbean.tt3')


## Simulation:

To run the simulation, make sure setrun.py, setplot.py, and Makefile are within the project folder, the topography file and the path to topography are specified in setrun.py.


## GeoClaw results:

After importing the storm data, gauge data and the topography data into setrun.py, the simulation reported there was half a meter to one meter rise in water level over the Gulf of Mexico near mainland. The simulation ran from 3 days before landfall (Sep 29) to 1 day after landfall (Oct 4). Gauges were taken from 4 locations and comparred to NOAA data. Note: Gauges map from 2 days before landfall and NOAA plots have not been added to Clawplack graphs.

## Conclusion:

Storm surges obtained from Clawpack were within order of magnitudes. Gauges 1 and 2 were the most accurate whilst Gauge 3 had mild inconsistencies predicting slightly greater storm surges. Gauge 4 plot was quite inaccurate likwly due to its distance from the storm track and other gauges.

Overall Geoclaw storm surge result is an comparable model to real-life storm surges.

Nigel Kuamankumah (nk2920@columbia.edu)
