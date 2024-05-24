# Example of Storm Surge from Hurricane Wilma

This example provides the data and Python code to run a simulation of Hurricane Wilma along the southwest coast of Florida. Wilma initially passed over the Yucatan Peninsula as a Category 4 hurricane before making landfall in the Floridian peninsula as a Category 3 in late October, 2005. The simulation begins the day before landfall over Florida, right after the storm moved through the Yucatan.

Running `make all` will compile the Fortran code, run the simulation, and plot the results.

## Topography

Topography data is automatically downloaded from the Columbia databases at: http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

## Storm Data

Storm data is automatically downloaded from the NOAA atcf archive at: 
http://ftp.nhc.noaa.gov/atcf/archive/2005/bal252005.dat.gz

## Gauges

Gauges 1-4 in the example correspond to four NOAA gauges which lie along the southwestern coast of Florida and the Florida Keys. The `fetch_noaa_tide_data()` function within the setplot.py file is used to pull real tide data from the gauges during the storm and compare it to the simulated output.

For questions, contact Arjun Choudhry at a.choudhry@columbia.edu
