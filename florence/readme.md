# Example of Storm Surge from Hurricane Florence

This example provides the data and Python code to run a simulation of Hurricane Florence along the coast of North and South Carolina. Florence made landfall near Wrightsville Beach, NC on Sept. 14, 2018 as a Category 1 storm. 

Executing `$ make all` will compile the Fortran code, run the simulation, and plot the results. 

## Topography

atlantic_2min.tt3 - Covers Atlantic Seaboard LL = (-92.0,13.0), UR = (-45.0,45.0)

Topography file is hosted in ../bathy/get_bathy.py. Alternatively, download the topography file at https://www.dropbox.com/s/jkww7jm78azswk5/atlantic_1min.tt3.tar.bz2?dl=0 

## Storm Data

Storm data file automatically downloads from https://ftp.nhc.noaa.gov/atcf/archive/ to `$CLAW/geoclaw/scratch`.

## Gauges

The functions `fetch_noaa_tide_data()` and `fetch_usgs_gauge_data()` in setplot.py fetch data for gauges 1-6 from https://tidesandcurrents.noaa.gov/map/ and data for gauges 7-8 from https://maps.waterdata.usgs.gov/mapper/index.html, respectively. Gauge data will download to `$CLAW/geoclaw/scratch`. All data points lie between the time period 9/12/2018 - 9/16/2018. 

USGS water level data is referenced to vertical datum NAVD88. For consistency, this example sets NOAA data to reference to NAVD88 as well.  

*Note:* Tide levels are subtracted from NOAA gauge water levels before plotting, but no tide data is available for USGS gauges. The area surrounding gauge 7 and 8 has very little tidal influence, so the observed water levels should be only minimally disturbed by tides.   

## AMR Flagregions

This example specifies three ruled rectangle flagregions, covering the: South Carolina coast, North Carolina coast, and North Carolina barrier islands (Ocracoke and Hatteras Islands). 

`$ make data` creates flagregion data files in the current directory.  


Contact Mirah Shi (ms5638@barnard.edu) for questions. 
