
# Hurricane Irma Storm Report

This example contains the data and Python code to run a storm surge simulation for Hurricane Irma.

## Hurricane Irma:
Hurricane Irma was a powerful category 5 hurricane that was the ninth named and second major hurricane during the 2017 Atlantic Hurricane season. Irma developed as a tropical disturbance on August 27th and became a tropical depression by 0000 UTC August 30th near the Cape Verde Islands. Very favorable conditions allowed Irma to strengthen to a hurricane just 30 hours later, quickly intensifying and reaching its maximum intensity by 1800 UTC September 5th as a category 5 hurricane. Irma made several landfalls, including one in Barbuda around 0545 UTC September 6th as a category 5, one in Cayo Romano, Cuba, at 0300 UTC September 9th as a category 5, one in Cudjoe Key, Florida at 1300 UTC September 10th as a category 4, and one in Marco Island, Florida at 1930 UTC later that same day as a category 3. Irma then moved along the Florida peninsula as it quickly dissipated to a tropical storm the next day.

Irma achieved a peak intensity of 155 knot winds and 914 millibars of pressure. The hurricane caused widespread wind and flooding damage from rainfall and storm surge along its path, with coastal flooding levels reaching up to 2 - 3 meters above normal at Irma's landfall locations.

If running this example, download _setrun.py_, _setplot.py_, _and Makefile_  to desired folder. Execute `$ make all` to compile the code, run the simulation, and plot the results.

_Source: NOAA Tropical Cyclone Report (https://www.nhc.noaa.gov/data/tcr/AL112017_Irma.pdf)_

## Storm Data:

Data for Clawpack to run simulation was taken from NOAA's storm data archive:                  
_https://ftp.nhc.noaa.gov/atcf/archive/2017/bal112017.dat.gz_

In _setrun.py_, one can retrieve data directly from source by writing code similar to this:
```sh
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2017/bal112017.dat.gz")
atcf_path = os.path.join(data_dir, "bal112017.dat")
```
For this example, Hurricane Irma storm data should be placed in the same directory that the simulation is ran in.

## Topography/Bathymetry Data:
_Topography data was accessed using GEBCO 2020 Gridded Bathymetry Data Download tool:
https://download.gebco.net/_

Specifications to download topography:      
Latitude: S 15, N 35
Longitude: W -90, E -60                                                
Format: 2D netCDF Grid or Esri ASCII (depending on size of file one prefers)

In this example, the .asc topogaphy file was placed in the same directory that the simulation was ran in and the following code was modified in _setrun.py_ to read in the topography data.

```sh
topo_path = os.path.join(data_dir, "gebco_irma_topo.asc")
```
Download topography data, add file to desired folder, but set the correct path from home folder to folder where file will be located, and add the name of the asc file as in this example.

_NETCDF type also works but may need to convert to .tt3 file to be compatible with GeoClaw._

## GeoClaw Results:
Landfall time in the simulation was set to be in Cudjoe Key, Florida at 1300 UTC September 10th. Simulation ran from 4 days before landfall (September 6th) to 2 days after landfall (September 12th).

Gauges were selected in NOAA Inundations dashboard: https://tidesandcurrents.noaa.gov/map/index.html

The observed gauge data for sea level at each location was de-tided using the `fetch_noaa_tide_data()` method and plotted against the predicted storm surge by GeoClaw. For this example, six gauge locations were selected in San Juan, Vaca Key, Key West, Naples, Port Manatee, and Clearwater Beach. Precise coordinates and data for each of these locations can be found in the _setrun.py_ file.

## Data Results:
In this example,

1. Vaca Key, Florida Bay, FL (ID: 8723970) experienced a storm surge of approximately 0.8 meters. GeoClaw predicted approximately 0.6 meters. Time of surge aligns.

2. Key West, FL (ID: 8724580) experienced a storm surge of approximately 1.0 meters. GeoClaw predicted approximately 1.1 meters. Time of surge aligns.

3. Naples, Gulf of Mexico, FL (ID: 8725110) experienced a storm surge of approximately 1.4 meters. GeoClaw predicted approximately 1.4 meters. Time of surge aligns.

4. Port Manatee, FL (ID: 8726384) experienced a storm surge of approximately 0.7 meters. GeoClaw predicted approximately 0.35 meters. Time of surge is slightly off.

5. Clearwater Beach, FL (ID: 8726724) experienced a storm surge of approximately 0.4 meters. GeoClaw predicted approximately 0.3 meters. Time of surge is slightly off.

6. San Juan, PR (ID: 9755371) experienced a storm surge of approximately 0.5 meters. GeoClaw predicted approximately 0.3 meters. Time of surge aligns.

In each case, discrepencies may be due to insuffient refinements in simulation or the limited resolution of topography/bathymetry data. A more powerful machine may provide more accurate forecast models to storm surge simulations. The gauge tidal predictions may have been slightly off too.

## Conclusion:
Storm surges obtained from GeoClaw were consistent with the observed data. Comparing GeoClaw output to the observed data, storm surges were a good model of a real-world storm surge. More analysis and refinements may lead to more accurate results.

----------------------------------------------------------------------------------------

Final remarks:
_setrun.py_ may be modified to have higher levels of refinement as in this example:
```sh
# max number of refinement levels:
amrdata.amr_levels_max = 6  
```
Higher refinement levels tend to increase surge accuracy. Refinement ratios may be specified in _setrun.py_ too as in this example:
```sh
regions.append([3, 5, rundata.clawdata.t0, rundata.clawdata.tfinal, -66.5, -65.5, 18.0, 19.0])
```

----------------------------------------------------------------------------------------

For questions, contact Corey Conzett at coreyconzett@gmail.com
