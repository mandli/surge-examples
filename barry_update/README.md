# Hurricane Barry Storm Report (AL022019)
This example contains the data and Python code to run a storm surge simulation for Hurricane Barry.

## Hurricane Barry
Hurricane Barry was an asymmetrical Category 1 hurricane and the first hurricane of the 2019 Atlantic hurricane season.

The origin of Barry was non-tropical, and the cyclone can be traced back to a mesoscale convective system that formed over the central United States. 

The area of disturbed weather moved eastward across the southcentral United States, and it reached northern Georgia on 7 July. The disturbance slowed down and turned southeastward and then southward over Georgia and the Florida Panhandle on the east side of a low- to mid-level ridge during the next couple of days, with showers and thunderstorms gradually increasing during that time. The elongated low emerged over the far northeastern Gulf of Mexico late on 9 July with a large area of disorganized convection. Barry slowly strengthened with its associated convectionincreasing in intensity and coverage. While gaining strength, Barry moved slowly westward to west-northwestward on the south and southwest sides of the above-mentioned ridge. Barry turned northwestward early on 13 July when it began to move toward a weakness in the ridge over the Mississippi Valley, and it strengthened to a category 1 hurricane on the Saffir-Simpson Hurricane Wind Scale around 1200 UTC that day when it was located just offshore of the southcentral Louisiana coast. After landfall, Barry turned north-northwestward and weakened, falling below hurricane strength by 1800 UTC 13 July when the center passed near Intracoastal City, Louisiana. The tropical storm’s center moved across the western portion of Louisiana and Barry weakened to a tropical depression while centered just south of the Arkansas border by 0000 UTC 15 July.

If running this example, download setrun.py, setplot.py, and Makefile to the appropriate directory. Execute ``` $ make all ``` to compile the code, run the simulation, and plot the results.

*Source: National Hurricane Center Tropical Cyclone Report* (https://www.nhc.noaa.gov/data/tcr/AL022019_Barry.pdf)

## Storm Data
Data for Clawpack to run simulation was taken from NOAA's storm data archive:
http://ftp.nhc.noaa.gov/atcf/archive/2019/bal022019.dat.gz

In setrun.py, one can retrieve data directly from source by writing code similar to this:
``` python
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file("http://ftp.nhc.noaa.gov/atcf/archive/2019/bal022019.dat.gz")
atcf_path = os.path.join(scratch_dir, "bal022019.dat")
```
For this example, Hurricane Barry storm data should be placed in the same directory that the simulation is ran in.

## Topography & Bathymetry Data
Topography data is automatically downloaded from the Columbia databases at: http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

## Geoclaw Parameters
Time of landfall was set in the simulation to be 13 July 2019, 1500 UTC. Simulation ran from 2 days before landfall to 2 days after.

Gauges were selected in the NOAA Inundations dashboard: https://tidesandcurrents.noaa.gov/map/index.html

The observed gauge data for sea level at each location was de-tided using the fetch_noaa_tide_data() method and plotted against the predicted storm surge by GeoClaw.  For this example, four gauge locations were selected in Eugene Island, LAWMA, Calcasieu Pass, and Texas Point. Precise coordinates and data for each of these locations can be found in the setrun.py file.

## Data Results
In this example, 
  1. Eugene Island, North of, Atchafalaya Bay, LA (ID: 8764314) experienced a storm surge of approximately 1.4 meters. GeoClaw predicted approximately 0.9 meters. Time of surge aligns.
  2. LAWMA, Amerada Pass, LA (ID: 8764227) experienced a storm surge of approximately 1.5 meters. GeoClaw predicted approximately 1.2 meters. Time of surge aligns.
  3. Calcasieu Pass, LA (ID: 8768094) experienced a storm surge of approximately -0.2 meters. GeoClaw predicted approximately -0.7 meters. Time of surge aligns.
  4. Texas Point, Sabine Pass, TX (ID: 8770822) experienced a storm surge of approximately -0.2 meters. GeoClaw predicted approximately -0.6 meters. Time of surge aligns.

In each case, discrepencies may be due to insuffient refinements in simulation or the limited resolution of topography/bathymetry data. A more powerful machine may provide more accurate forecast models to storm surge simulations. The gauge tidal predictions may have been slightly off too.

## Conclusion
The storm surge data obtained from GeoClaw are generally consistent with the observed data. However, in most cases, the observed storm surge slightly exceeded the amount predicted by the GeoClaw model. The reason for this likely comes from Barry’s historic rains, which caused significant flooding but are not taken into account in the model. More analysis and refinements may lead to more accurate results. 

----------------------------------------------------------------------------------------

Final remarks: 
_setrun.py_ may be modified to have higher levels of refinement as in this example:
```sh
# max number of refinement levels:
    amrdata.amr_levels_max = 6
# List of refinement ratios at each level (length at least mxnest-1)
    amrdata.refinement_ratios_x = [2,2,2,6,6,16]
    amrdata.refinement_ratios_y = [2,2,2,6,6,16]
    amrdata.refinement_ratios_t = [2,2,2,6,6,16]
```
And refinement ratios may be specified in _setrun.py_ too as in this example:
```sh
regions.append([1, 3, clawdata.t0, clawdata.tfinal, clawdata.lower[0], clawdata.upper[0], clawdata.lower[1], clawdata.upper[1]])
regions.append([1, 5, clawdata.t0, clawdata.tfinal, -95, -90, 29.2, 30.0])

regions.append([4, 5, clawdata.t0, clawdata.tfinal, -91.5, -91.2, 29.3, 29.5])  # Gauge 1,2 
regions.append([6, 7, clawdata.t0, clawdata.tfinal, -93.6, -93.2, 29.5, 29.9])  
regions.append([6, 7, clawdata.t0, clawdata.tfinal, -94.0, -93.5, 29.5, 29.9])    
```
----------------------------------------------------------------------------------------

