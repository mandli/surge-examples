# Bathymetry for Surge Examples

## Global Strip

Global strip of bathymetry for longitudes and latitudes [-180, 180]  x [-45, 45]
broken up in 15 degree horizontal strips.  Files are enumerated starting with
latitude -45.

strip_0.nc - [-45, -30]
strip_1.nc - [-30, -15]
strip_2.nc - [-15,   0]
strip_3.nc - [  0,  15]
strip_4.nc - [ 15,  30]
strip_5.nc - [ 30,  45]

## Sandy

atlantic_2min.tt3 - Covers Atlantic Seaboard
    LL = (-92.0,13.0), UR = (-45.0,45.0)

newyork_s3.tt3 - New York and Long Island area
    LL = (74.5 W, 40 N), UR = (71 W, 41.5 N)


## Irene

atlantic_2min.tt3 - Covers Atlantic Seaboard
    LL = (-92.0,13.0), UR = (-45.0,45.0)

newyork_s3.tt3 - New York and Long Island area
    LL = (74.5 W, 40 N), UR = (71 W, 41.5 N)

## Isabel

atlantic_2min.tt3 - Covers Atlantic Seaboard
    LL = (-92.0,13.0), UR = (-45.0,45.0)

chesapeake.nc - Chesapeake bay
    LL = , UR = 

## Ike

## Katrina

## Karen

## Michael

 - gulf_carribean.tt3 - Bathymetry covering larger region including Carribean
   and part of the Atlantic sea-board.  Lower left corner = (99W,8N), upper
   right corner = (50W,17N)
 - gulf_coarse_bathy.tt3 - Bathymetry covering entire gulf at 2 minute
   resolution Lower left corner = (99W,17N), upper right corner = (80W,17N)
 - NOAA_Galveston_Houston.tt3 - New larger bathymetry coveraged for Galveston
   and Houston area with 3 second resolution. (from NOAA Design-a-grid)
 - NewOrleans_3s.nc - Bathymetry from NOAA at 3 second resolution.

## Mumbai

 - Indian Ocean: india.nc (47 W, 100 E, 31 N, -10 S) - ETOPO1 data fetched from
   https://maps.ngdc.noaa.gov/ on  Dec 15, 2016.
 - Mumbai area:  Conributed by Haider Hasan <haiderhasan@hotmail.co.uk> as part
   of a tsunami study.  Please contact him if you are interested in the
   bathymetry.  It is based on digitization of soundings and contours from
   nautical charts of the area, GEBCO data in the deeper water and SRTM data on
   land.

 Tsunami simulations for Karachi and Bombay: Sensitivity to source parameters of
 the 1945 Makran earthquake, by H. Hasan, H. A. Lodhi, and R. J. LeVeque: poster
 presented at Regional Conference on “Reducing Tsunami Risk in the Western
 Indian Ocean” in Muscat, Oman Jointly organised by the Intergovernmental
 Oceanographic Commission of UNESCO and Oman's Directorate General of
 Meteorology, Public Authority for Civil Aviation 22-23 March 2015.