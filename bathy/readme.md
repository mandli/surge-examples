# Bathymetry for Surge Examples

## Global Strip

Global strip of bathymetry for longitudes and latitudes [-180, 180]  x [-45, 45]
broken up in 15 degree horizontal strips.  Files are enumerated starting with
latitude -45.  The script `get_topo.py` should fetch these files from the
etopo1 data base automatically as NetCDF files.

strip_0.nc - [-45, -30]
strip_1.nc - [-30, -15]
strip_2.nc - [-15,   0]
strip_3.nc - [  0,  15]
strip_4.nc - [ 15,  30]
strip_5.nc - [ 30,  45]

## Irene

atlantic_2min.tt3 - Covers Atlantic Seaboard
    LL = (-92.0,13.0), UR = (-45.0,45.0)

newyork_s3.tt3 - New York and Long Island area
    LL = (74.5 W, 40 N), UR = (71 W, 41.5 N)
