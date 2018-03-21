# Bathymetry Coverage

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
