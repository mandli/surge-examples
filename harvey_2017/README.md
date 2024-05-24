# Hurricane Harvey Storm Report
This example contains the data and Python code to run a storm surge simulation for Hurricane Harvey.

## Hurricane Harvey:
Hurricane Harvey was a category 4 hurricane that was the eighth named and first major hurricane of the 2017 Atlantic Hurricane season. Harvey began as a weak tropical storm which affected the Lesser Antilles before dissipating over the central Caribbean Sea. It reformed over the Bay of Campeche, quickly intensifying to a category 4 hurricane before making landfall over San Jose island, near Rockport, Texas, at 0300 UTC, August 26 2017. It is estimated that at this landfall, sustained winds reached 115 kt and minimum central pressure was 937 mb. Harvey made a second landfall 3 hours later, this time over the Texas mainland. Hurricane Harvey then stalled over the Texas coast for four days, dropping over 60 inches of rain on southeastern Texas, causing historic flooding. Harvey made a final landfall over southwestern Louisiana at 0800 UTC 30 August. Sustained winds during this landfall were 40 kt.

If running this example, download setrun.py, setplot.py, and Makefile to the appropriate directory. Execute `$ make all` to compile the code, run the simulation, and plot the results.

*Source: National Hurricane Center Tropical Cyclone Report*
(https://www.nhc.noaa.gov/data/tcr/AL092017_Harvey.pdf)

## Storm Data:
Data to run the simulation was retrieved from NOAA’s storm data archive:
http://ftp.nhc.noaa.gov/atcf/archive/2017/bal092017.dat.gz

In setrun.py, data can be directly retrieved from the source by writing code similar to this:
```python
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file(“http://ftp.nhc.noaa.gov/atcf/archive/2017/bal092017.dat.gz”)
atcf_path = os.path.join(data_dir, “bal092017.dat”)
```

For this example, Hurricane Harvey storm data should be placed in the same directory that the simulation is run in.

## Topography/Bathymetry Data:
Topography data is automatically downloaded from the Columbia databases at:
http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

## GeoClaw Parameters:
Time of landfall was set in the simulation to be 26 August, 0400 UTC. Simulation ran from 4 days before landfall to 5 days after.

Gauges were selected in the NOAA Inundations dashboard:
https://tidesandcurrents.noaa.gov/map/index.html

The observed gauge data for sea level at each location was de-tided using the `fetch_noaa_tide_data()` method and plotted against the predicted storm surge by GeoClaw.

## Data Results:
In this example,
Freeport Harbor, TX (ID: 8772471) experienced a storm surge of approximately 1 meter. GeoClaw predicted approximately 0.3 meters. 
San Luis Pass, TX (ID: 8771972) experienced a storm surge of 1.1 meters. GeoClaw predicted approximately .4 meters. 
Galveston Railroad, TX (ID: 8771486) experienced a storm surge of .9 meters. GeoClaw predicted approximately 1.3 meters. 
Galveston Pier 21, TX (ID: 8771450) experienced a storm surge of .8 meters. GeoClaw predicted approximately .3 meters. 
Galveston Bay Entrance, TX (ID: 8771341) experienced a storm surge of .8 meters. GeoClaw predicted approximately .4 meters. 
Rollover Pass, TX (ID: 8770971) experienced a storm surge of 1.2 meters. GeoClaw predicted approximately .8 meters.  (Do I take global max, or max after 0?)
High Island, TX (ID: 8770808) experienced a storm surge of 1.6 meters. GeoClaw predicted approximately 2.2 meters. Time of surge aligns. (Do I ignore clearly anomalous values?)
Morgans Point, TX (ID: 8770613) experienced a storm surge of 1.3 meters. GeoClaw predicted approximately 2.2 meters. 
Manchester, TX (ID: 8770777) experienced a storm surge of 3.2 meters. This value was singled out in the NOAA report as being significantly affected by rainfall runoff. GeoClaw predicted 0 meters. 
Calcasieu Lake, LA (ID: 8768094) experienced a storm surge of 1 meter. GeoClaw predicted approximately .5 meters. 
Sabine Pass, LA (ID: 8770822) experienced a storm surge of 1 meter. GeoClaw predicted approximately .5 meters. 

Significant discrepancies in results may stem from the gauges being located in “dry cells” in the simulation. Harvey’s historic rains and the resulting flooding are other significant contributors to the measured storm surge; these factors are not accounted for in the GeoClaw simulation.

## Conclusion:
Storm surges obtained from GeoClaw were generally inconsistent with the observed data. In most cases, the observed storm surge greatly exceeded the amount predicted by the GeoClaw model. The reason for this likely comes from Harvey’s historic rains, which caused significant flooding but are not accounted for in the model. Adjustments to the GeoClaw package to incorporate rainfall may lead to more accurate results.

This project was begun by Reuben Solnick.
