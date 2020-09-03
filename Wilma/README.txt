Created by Arjun Choudhry (a.choudhry@columbia.edu)


This directory contains the requisite files needed to run the validation simulation for Hurricane Wilma (2005).

Within the setplot.py and setrun.py files contain code that works to generate as accurate a simulation as possible.

For instance, within setrun.py, 7 levels of refinement exist (down to the ~100m order of magnitude) as well as a ruled rectangle implementation (primarily for the Ft. Myers gauge, which exists within a deep, winding channel) and the specification of four gauges spread throughout the Florida Keys and southwest Florida. 

In setplot.py, there exists a call to the fetch_noaa_tide_data() function, which allows for the generation of plots with real gauge data superimposed upon simulation data.



