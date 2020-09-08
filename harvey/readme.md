# Example of Storm Surge from Hurricane Harvey

This example provides the data and Python code to run a simulation of Hurricane Harvey. Harvey initially passed over the Yucatan Peninsula as a Tropical Wave before strengthening into a category 4 hurricane and making landfall over the gulf coast of Texas in late August of 2017. The simulation models 4 days of the storm, beginning the day before landfall over Texas.

Running `make all` will compile all the necessary code for running the simulation

## Topography

Topography data is automatically downloaded from the Columbia databases at: http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

## Storm Data

Storm data is automatically downloaded from the NOAA atcf archive at: 
http://ftp.nhc.noaa.gov/atcf/archive/2017/bal092017.dat.gz

## Gauges

Gauges 1-5 in the example correspond to five NOAA gauges which lie along the Texas gulf coast. `fetch_noaa_tide_data()` is used to pull tide data from the gauges and compare it to the simulated output in setplot.py. Normal tidal behaviors are factored out so that only storm-surge is compared, and for consistency, water level data is referenced to vertical datum NAVD88 in both the simulated and actual data.

For questions, contact Reuben Solnick at rfs2146@columbia.edu
