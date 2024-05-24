# Storm Report: Hurricane Nicole

## General Information

Hurricane Nicole, originating from a mid- to upper-level trough in the western Atlantic around November 3, 2022, intensified to a subtropical storm by November 7 and reached category 1 hurricane strength with landfalls on Great Abaco Island and Grand Bahama Island. On November 10, it made landfall at Vero Beach, Florida, with winds of 65 kt. Due to its size and interaction with an anticyclone, Nicole produced a considerable storm surge along Florida's east coast. Damages in the state were further exacerbated by the region's vulnerability from the preceding Hurricane Ian's erosion and flooding in late September of 2022. 

Sources: https://www.nhc.noaa.gov/data/tcr/AL172022_Nicole.pdf ; https://storymaps.arcgis.com/stories/95d77e39b6fb4959b691ce89961392c8

## Topography & Bathymetry Data


Topography data can be obtained from: https://www.gebco.net/data_and_products/gridded_bathymetry_data/

The topography from the Hurricane Ike example was reused for Hurricane Nicole due to the similarity of regions impacted. 

## Storm Data

Storm data for Hurricane Nicole was pulled from the National Oceanic and Atmospheric Administration (NOAA) storm data archive: http://ftp.nhc.noaa.gov/atcf/archive/2022/bal172022.dat.gz

Data was then fetched by modifying code in setrun.py:


```python
# Converting ATCF data to GeoClaw
clawutil.data.get_remote_file("http://ftp.nhc.noaa.gov/atcf/archive/2022/bal172022.dat.gz")
atcf_path = os.path.join(data_dir, "bal172022.dat")
```

This adjustment places the storm data in the same scratch directory defined for the topography data.

## GeoClaw Set Up

### Landfall & Time Range
Time of landfall was set in the simulation to be November 10, 0700 UTC. Simulation should run from 1 day prior to landfall (November 9) to 1 day post (November 11).

### Gauges
Gauges were selected from the NOAA Inundations dashboard: https://tidesandcurrents.noaa.gov/map/index.html

## Comparison & Remarks

The NOAA verified water levels varied often from the surges predicted by the GeoClaw simulation. This is likely a result of the placement of the gauges in inlets or along highways - areas difficult to isolate for water levels.

Further refinement layers would be beneficial in some of these cases to minimize the effect of the land in the simulation - similarly, inclusion of higher resolution topographical area would assist with the accuracy of the results.

\
Contact information: nf2495@columbia.edu


```python

```
