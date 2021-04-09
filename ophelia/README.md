

# Hurricane Ophelia Storm Report 

This example contains the data and setup for running a storm surge forecast for Hurricane Ophelia. 

## Hurricane Ophelia: 
Hurricane Ophelia was a category 3 hurricane and the sixth major hurricane in the Atlantic in 2017. Ophelia formed into a tropical storm by 0600 UTC October 09, strengthened to become a hurricane by 1800 UTC October 11, made landfall along the southwestern coast of Ireland at 1100 UTC 15 October. Extratropical Ophelia moved north-east across western Island, emerged over the North Sea, maked landfall along the coast of Norway, and dissipated by 0000 UTC 18 October. 

_Source: NOAA Tropical Cyclone Report (https://www.nhc.noaa.gov/data/tcr/AL172017_Ophelia.pdf)_

## Clawpack Installation:

If Clawpack has not been installed, one can install Clawpack from here: 
https://www.clawpack.org/installing.html

Before installation of Clawpack, prerequisites may need to be installed including pip3 and python3.                         
Best of luck installing dependencies!

After installing Clawpack, run examples, either this one here or from Clawpack,                            
for Hurricane Ike: http://www.clawpack.org/gallery/_static/geoclaw/examples/storm-surge/ike/README.html               
for Hurricane Isaac: http://www.clawpack.org/gallery/_static/geoclaw/examples/storm-surge/isaac/README.html

If running this example, download _setrun.py_, _setplot.py_, _and Makefile_  to desired folder. 


## Storm data: 
                                                                  
Data for Clawpack to run simulation was taken from NOAA's storm data archive:                     
_https://ftp.nhc.noaa.gov/atcf/archive/2017/_       

Hurricane Ophelia storm data was located in _bal172017.dat.gz_

In _setrun.py_, one can retrieve data directly from source by writing a code similar to this:
```sh
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2017/bal172017.dat.gz")
atcf_path = os.path.join(scratch_dir, "bal172017.dat")
```

## Topography/Bathymety data: 
_Topography data was accessed using GEBCO 2020 Gridded Bathymetry Data Download tool: 
https://download.gebco.net/_ 

Specifications to download topography:      
Latitude: S 20, N 80                           
Longitude: W -40, E 20                                                 
Format: 2D netCDF Grid or Esri ASCII (depending on size of file one prefers) 

_Topography file already converted to ASC file can be accessed in: https://www.dropbox.com/sh/gyhx2lio1sr5tl9/AAD7Can6yYIfW3I6nChfLFNMa?dl=0_

In this example, the topogaphy was placed in the geoclaw folder and the following code was modified in _setrun.py_ to read in the topography data. 

```sh 
topo_path = os.path.join("/home/socoyjonathan/clawpack_src/clawpack-v5.7.1/geoclaw/topograpy", "topography.asc") 
```
Download topography data, add file to desired folder, but set the correct path from home folder to folder where file will be located, and add the name of the asc file as in this example.

_NETCDF type also works but may need to convert to .tt3 file to be compatible with GeoClaw._

## GeoClaw results:
Simulation ran from 2 days before landfall, 14 October, to 2 days 12 hours after landfall, 18 October. 

Gauges were selected from the British Oceanography Data Centre (BODC): https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/

For this example, four gauge locations were selected and specified in _setrun.py_

```sh
# Portrush:
rundata.gaugedata.gauges.append([1, -6.657948, 55.206390, rundata.clawdata.t0, rundata.clawdata.tfinal]) 
```
For UK based storms, due to limited data availability, comparisons of surges may prove to be rigorous.

Output for gauge data ran from 2 days before landfall to 2 days after landfall

Observed data for sea level for each gauge location was downloaded from: 
https://www.bodc.ac.uk/data/hosted_data_systems/sea_level/uk_tide_gauge_network/processed_customise_time_selection/

Unfortunately, the datum is unknown and is not provided by BODC. Therefore, tide data is unknown, and observed data cannot be de-tided. 

One may resort to the python package _Pytides_ to predict tide data, allow for observed data to be de-tided, and observed surge data to be compared to Clawpack simulation output for surge data.

_Pytides_ may be installed from its source: https://github.com/sam-cox/pytides                                         
However, source files are not compatible with Python 3, and Python 2 installation not recommended.                    Therefore, modifications to the _import_ code is required.          

Alternatively, one can clone this modified package adjusted to work with Python 3.7 and above: https://github.com/yudevan/pytides

After obtaining tide predictions from pytides, de-tide observed data from BODC and save surge data as a text file.

In this example, Clawpack gauge data was downloaded after simulation was complete and using python scripts, Clawpack output and observed data were compared by observing their plots. 

If working with NOAA database and US-based storms, one may obtain observed data from NOAA's database and modify _setplot.py_ to compare surge data within Clawpack 

## Data Results: 
In this example, 

Portrush station in Northern Ireland experienced a storm surge of approximately .486 m.  Clawpack prediction was approximately the same. Time of surge is slightly off.

Tobermory station in Scotland experienced a storm surge of approximately .75 m. Clawpack prediction was approximately .62 m. Time of surge aligns. 

Ullapool station in Scotland experienced a storm surge of approximately .680 m. Clawpack prediction was approximately .63 m. Time of surge is slightly off.

Kinlochbervie station in Scotland experienced a storm surge of approximately .29 m. Clawpack prediction was approximately .52 m. Time of surge aligns.

Comparisons for surge data can be found here:
https://www.dropbox.com/s/1h3xa4d8al9fiuz/Clawpack_Surge_Comparisons.pdf?dl=0

In each case, discrepencies may be due to insuffient refinements in simulation. 
A more powerful machine may provide more accurate forecast models to storm surge simulations. The tidal predictions may have been slightly off too within unknown datum for observed data from BODC. 

## Conclusion: 
Storm surges obtained from Clawpack were consistent. Comparing Clawpack output to observed data, storm surges were a good model of a real-world storm surge. 
More analysis and refinements may lead to more accurate results. 

----------------------------------------------------------------------------------------

Final remarks: 
_setrun.py_ may be modified to have higher levels of refinement as in this example:
```sh
# max number of refinement levels:
amrdata.amr_levels_max = 6  
```
And refinement ratios may be specified in _setrun.py_ too as in this example:
```sh
regions.append([1,3,rundata.clawdata.t0, rundata.clawdata.tfinal, -30.0, -12.0, 30.0, 72.0])
```

----------------------------------------------------------------------------------------

For any questions on the specifics of this example, contact Jonathan Socoy (js5587@columbia.edu).


