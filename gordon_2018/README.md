# Tropical Storm Gordon Report (AL072018)
This example contains the data and Python code to run a storm surge simulation for Storm Gordon.

## Storm Gordon
Gordon formed near the southeastern coast of Florida, moved across the Florida
Keys and extreme southwestern Florida, and made a final landfall as a strong tropical storm
along the north-central Gulf of Mexico coast just west of the Mississippi-Alabama border. 

Gordon quickly strengthened and made landfall around 1115 UTC 3 September near Tavernier in the
Florida Keys with an estimated intensity of 45 kt. After crossing Florida Bay, Gordon made a
second landfall near Flamingo on the southern tip of the Florida peninsula around 1315 UTC
that day. The center of Gordon emerged over the extreme eastern Gulf of Mexico an hour or so
later, and the convective structure of the tropical storm continued to improve. Gordon
strengthened into a 50-kt tropical storm as an eye-like feature became apparent in National
Weather Service (NWS) Doppler radar imagery shortly before 1800 UTC 3 September when it 
was centered just off the coast of Marco Island, Florida. 
Gordon reached its peak intensity of 60 kt at 1800 UTC the next day while centered over
the north-central Gulf of Mexico about 115 n mi south-southeast of Pascagoula, Mississippi.
The tropical storm turned northwestward, and although the convective structure improved
somewhat in the few hours before the center reached the coast, surface and radar data indicate
that Gordon remained a 60-kt tropical storm when it made landfall between the
Alabama/Mississippi border and Pascagoula around 0315 UTC 5 September. 
After landfall, Gordon quickly weakened and became a tropical depression by 1200 UTC when it
was located about 30 n mi southeast of Jackson, Mississippi. The depression slowed down but
continued on a northwestward heading while it moved over southeastern Arkansas shortly after
0000 UTC 6 September. 

If running this example, download setrun.py, setplot.py, and Makefile to the appropriate directory. Execute ``` $ make all ``` to compile the code, run the simulation, and plot the results.

*Source: National Hurricane Center Tropical Cyclone Report* (https://www.nhc.noaa.gov/data/tcr/AL072018_Gordon.pdf)

## Storm Data
Data for Clawpack to run simulation was taken from NOAA's storm data archive:
http://ftp.nhc.noaa.gov/atcf/archive/2018/bal072018.dat.gz

In setrun.py, one can retrieve data directly from source by writing code similar to this:
``` python
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file("http://ftp.nhc.noaa.gov/atcf/archive/2018/bal072018.dat.gz")
atcf_path = os.path.join(scratch_dir, "bal072018.dat")
```
For this example, Gordon storm data should be placed in the same directory that the simulation is ran in.

## Topography & Bathymetry Data
Topography data is provided with the name of North45_South0_West-105._East-35.tt3. The file should be downloaded and placed in the scratch directory as the Storm Data.

The topography file can be downloaded from https://www.gebco.net/data_and_products/gridded_bathymetry_data/ with coordinates North 45, South 0, West -105, and East -35.

## Geoclaw Parameters
Time of landfall was set in the simulation to be 5 September, 1200 UTC. Simulation ran from 2 days before landfall to 2 days after.

Gauges were selected in the NOAA Inundations dashboard: https://tidesandcurrents.noaa.gov/map/index.html

The observed gauge data for sea level at each location was de-tided using the fetch_noaa_tide_data() method and plotted against the predicted storm surge by GeoClaw.  For this example, four gauge locations were selected in Pascagoula NOAA Lab, Dauphin Island, Coast Guard Sector Mobile, and Pensacola. Precise coordinates and data for each of these locations can be found in the setrun.py file.

## Data Results
In this example, 
  1. Pascagoula NOAA Lab, MS (ID: 8741533) experienced a storm surge of approximately 0.3 meters. GeoClaw predicted approximately 0.4 meters. Time of surge aligns.
  2. Dauphin Island, AL (ID: 8735180) experienced a storm surge of approximately 0.5 meters. GeoClaw predicted approximately 0.3 meters. Time of surge aligns.
  3. Coast Guard Sector Mobile, AL (ID: 8736897) experienced a storm surge of approximately 0.70 meters. GeoClaw predicted approximately 1.1 meters. Time of surge aligns.
  4. Pensacola, FL(ID: 8729840) experienced a storm surge of approximately 0.4 meters. GeoClaw predicted approximately 0.2 meters. Time of surge aligns.

In each case, discrepencies may be due to insuffient refinements in simulation or the limited resolution of topography/bathymetry data. A more powerful machine may provide more accurate forecast models to storm surge simulations. The gauge tidal predictions may have been slightly off too.

## Conclusion
The storm surge data obtained from GeoClaw were mostly inconsistent with the observed data, which may due to low resolution or difficulty of simulating extremely detailed topography, but their timing is accurate. 
For Gauge 2 and 4, the observed storm surge exceeded the amount predicted by the GeoClaw model. 
The reason for this likely comes from Gordon’s historic rains, which caused significant flooding but are not taken into account in the model.
More analysis and refinements may lead to more accurate results. 

----------------------------------------------------------------------------------------

Final remarks: 
_setrun.py_ may be modified to have higher levels of refinement as in this example:
```sh
# max number of refinement levels:
amrdata.amr_levels_max = 8

# List of refinement ratios at each level (length at least mxnest-1)
amrdata.refinement_ratios_x = [2,2,2,3,3,3,4,4]
amrdata.refinement_ratios_y = [2,2,2,3,3,3,4,4]
amrdata.refinement_ratios_t = [2,2,2,3,3,3,4,4]
```
And refinement ratios may be specified in _setrun.py_ too as in this example:
```sh
regions.append([1, 3, clawdata.t0, clawdata.tfinal, clawdata.lower[0], clawdata.upper[0], clawdata.lower[1], clawdata.upper[1]])
regions.append([2, 4, clawdata.t0, clawdata.tfinal, -88.6, -88.5, 30.3, 30.4])      # Gauge 1 
regions.append([6, 7, clawdata.t0, clawdata.tfinal, -88.10, -88.00, 30.20, 30.30])  # Gauge 2
regions.append([2, 3, clawdata.t0, clawdata.tfinal, -88.06, -88.04, 30.63, 30.71])  # Gauge 3
regions.append([5, 7, clawdata.t0, clawdata.tfinal, -87.28, -87.18, 30.38, 30.42])  # Gauge 4
```

----------------------------------------------------------------------------------------


