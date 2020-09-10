# Example of Storm Surge - Hurricane Barry

This example provides the data and Python code to run a simulation of Hurricane Barry along the coast of Louisiana. On July 13, 2019, Barry made landfall on Marsh Island and second landfall in Intracoastal City, Louisiana, both times as a Category 1 hurricane.

Executing `$ make all` will compile the Fortran code, run the simulation, and plot the results.

## Topography Data

Download `NetCDF` topography data from NOAA at: https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ngdc.mgg.dem:728/html

## Storm Data

Storm data is automatically downloaded from the NOAA atcf archive at: https://ftp.nhc.noaa.gov/atcf/archive/2019/bal022019.dat.gz

## Gauges

Gauges 1-5 in the example correspond to 5 NOAA gauges along the US South Coast in Louisiana. The `fetch_noaa_tide_data()` method is used to compare the simulated gauge data to real data in setplot.py. 


```python

```
