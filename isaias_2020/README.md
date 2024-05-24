# Hurricane Isaias Storm Report
This example provides the data and python code to run a GeoClaw storm surge simulation of Hurricane Isaias.

## Hurricane Isaias (AL092020) Information:
July 30, 2020 - August 4, 2020
Hurricane Isaias was a Category 1 hurricane and tropical storm that caused damage across the Caribbean and the East Coast of the United States. It made landfall in the Dominican Republic, southern Bahamas, and Andros Island before reaching the US. It made landfall with the US near Ocean Isle Beach, North Carolina, on 0310 UTC 04 August.

NOAA Report: https://www.nhc.noaa.gov/data/tcr/AL092020_Isaias.pdf

## Storm Data
The storm data is located in https://ftp.nhc.noaa.gov/atcf/archive/2020/, file name _bal092020.dat.gz_

In _setrun.py_, this data can be retrieved with the following code:
```sh
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file(
               "http://ftp.nhc.noaa.gov/atcf/archive/2020/bal092020.dat.gz")
atcf_path = os.path.join(scratch_dir, "bal092020.dat")
```

## Topography and Bathymetry Data
The topography file was taken from GEBCO Gridded Bathymetry Data Download, https://download.gebco.net/

Latitude: S 12, N 47
Longitude: W -88, E -60

It can be downloaded as an Esri ASCII file. This file must be downloaded, named, and saved to a location, and then its path must be linked in _setrun.py_.
It is stored here: https://www.dropbox.com/s/8dnctldn7ljstm5/isaias.asc?dl=0

For example, if you named the topography file "isaias.asc":
```sh
topo_path = os.path.join("/name_of_path_to_folder", "isaias.asc")
```

## GeoClaw Simulation Parameters
In _setrun.py_:
Landfall was set to 0000 UTC 31 July, and the simulation was ran from 1 day before landfall (0000 UTC July 30) to 5 days after landfall (0000 UTC 05 August).

Gauges were selected from the NOAA Inundations dashboard: https://tidesandcurrents.noaa.gov/inundationdb/. Their coordinates were appended. Coordinates were initially taken from their NOAA pages and Google Earth estimations, however some gauges had to be moved slightly because they would end up on land in the simulation even at very high levels of refinement.

The regions around each gauge that were given higher refinement levels were specified for each gauge and appended in the file.

I appended a friction region for around Savannah, Georgia.

I set the max number of refinement levels to 6.

I utilized the _amrdata.memsize_ variable, because this simulation requires a lot more memory than the default allocation of 2^22-1. Instead of copying data and doubling the size due to the limited space, we are just going to allocate enough memory at first. 2^26-1 bytes needed.

In _setplot.py_:
I gave each gauge a separate topography plot around its location so we can see what's going on.

Along with plotting the simulation's produced gauge data, I also plotted the NOAA confirmed gauge data. I used the _fetch_noaa_tide_data()_ method to pull tide data from the gauges and compare it to the simulated output. Tide data from gauges were calculated by _(recorded water level - predicted water level)_. GMT time zone and metric units were used as default.

## Comparing Results with Real Life
1. __Magueyes Island, Puerto Rico 9759110__: Real surge of about 0.40m.
GeoClaw predicts a smaller storm surge of about 0.15m. The time of surge aligns.

2. __Lake Worth Pier, Florida 8722670__: Real surge of about 0.31m.
GeoClaw predicts a smaller storm surge of about 0.14m. The time of surge aligns.

3. __Savannah, Georgia's Fort Pulaski 8670870__: Real surge of about 0.95m.
GeoClaw predicts a smaller storm surge of about 0.13m. The time of surge aligns.

4. __Springmaid Pier, South Carolina 8661070__: Real surge of about 1.30m.
GeoClaw predicts a storm surge with a lower maximum (about 0.99m) and a lower minimum (about -0.95m). The time of surge aligns.

5. __Wilmington, North Carolina 8658120__: Real surge of about 1.70m.
GeoClaw predicts a negative surge of about -0.15m, very different from the real gauge data. See limitations section for the reason. The time of surge aligns.

6. __Marcus Hook, Pennsylvania 8540433__: Real surge of about 0.85m.
GeoClaw predicts a smaller storm surge of about 0.63m. The time of surge aligns.

## Notes on the Results
Even with a very high level of refinement, I ran into problems with gauges in narrow rivers surrounded with a lot of land. The topography file taken from GEBCO may think those gauges are landlocked when they are really not, resulting in no simulated surge reaching the gauge and no simulated gauge data. My fifth gauge in Wilmington, NC, had the largest recorded surge at roughly 1.70m, but it is almost fully landlocked in the GeoClaw simulation, leading to weird results.

GeoClaw generally did a very good job at getting the time of storm surge correct. I noticed it will mostly underestimate the surge height though. This difference between simulated data and the gauge data may be due to inadequate refinement levels of the simulation. The topography/bathymetry data taken from GEBCO may also have too low of a resolution, or today's topography/bathymetry may be different from how it was in 2020, when Isaias occured.

If I ran the simulation at higher refinement levels on a more powerful machine, I may have gotten better results. The NOAA gauge predicted levels may have been inaccurate, which would alter the recorded gauge data.

## Conclusion
Storm surges obtained from GeoClaw generally underestimated the observed data, but their timing was accurate. More analysis and higher refinement may lead to more accurate results.
See this file for the visual representation of gauge plots: https://www.dropbox.com/s/ioz7anvoggosa0y/Gauge%20Data%20Plots.png?dl=0

If you want to modify the simulation to have higher levels of refinement, you can modify these lines in _setrun.py_:
```sh
# max number of refinement levels:
amrdata.amr_levels_max = 6

# List of refinement ratios at each level (length at least mxnest-1)
amrdata.refinement_ratios_x = [2, 2, 2, 6, 16]
amrdata.refinement_ratios_y = [2, 2, 2, 6, 16]
amrdata.refinement_ratios_t = [2, 2, 2, 6, 16]
```
You can alter the max number of refinement levels in the simulation, or alter the refinement ratios so they are higher.

Then, you can increase the refinement in certain regions in _setrun.py_, for example:
```sh
regions.append([5,6,rundata.clawdata.t0, rundata.clawdata.tfinal, -67.1, -66.9, 17.9, 18.1])
```
----------------------------------------------------------------------------------------

For any questions, contact Bernard Wang at bxw2101@columbia.edu!
