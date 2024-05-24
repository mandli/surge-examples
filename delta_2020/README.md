## Hurricane Delta Storm Report (AL262020)

------

This folder contains the data and code to run a storm surge simulation for Hurricane Michael

### Hurricane Delta

------

Delta was a category 4 hurricane on the Saffir-Simpson Hurricane Wind Scale. It made two landfalls, both at category 2 intensity, on the Yucatan Peninsula and in southwestern Louisiana. Delta made landfall near Creole, Louisiana, at 2300 UTC that day with maximum winds of about 85 kt. This landfall location was only about 10 n mi east of where Hurricane Laura’s eye struck the coast a little more than a month prior. With Southwest Louisiana still in recovery after Major Hurricane Laura, the winds and rainfall from Delta further delayed the recovery efforts, and in many cases, caused significant additional damage to homes and businesses. Many buildings that had roof or structural damage caused by Hurricane Laura still had temporary tarping, which was ripped off by the hurricane force winds of Delta.

If running this example, download setrun.py, setplot.py, and Makefile to the appropriate directory. Execute `$ make all` to compile the code, run the simulation, and plot the results.

*Source: 1. National Hurricane Center Tropical Cyclone Report* (https://www.nhc.noaa.gov/data/tcr/AL262020_Delta.pdf)                                                                                                                      			 *2. National Weather Service, NOAA Tropical Weather Information Page* ([https://www.weather.gov/lch/2020Delta](https://www.nhc.noaa.gov/data/tcr/AL142018_Michael.pdf))

### Storm Data

------

Data to run the simulation was retrieved from NOAA’s storm data archive: http://ftp.nhc.noaa.gov/atcf/archive/2020/bal262020.dat.gz

In setrun.py, data can be directly retrieved from the source by writing code similar to this:

```python
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file(“http://ftp.nhc.noaa.gov/atcf/archive/2020/bal262020.dat.gz”)
atcf_path = os.path.join(data_dir, “bal262020.dat”)
```

For this example, Hurricane Harvey storm data should be placed in the scratch directory ($CLAW/geoclaw/scratch) that the simulation is run in.

### Topography/Bathymetry Data:

------

Topography data is automatically downloaded from the Columbia databases at: http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

### GeoClaw Parameters:

------

Time of landfall was set in the simulation to be 9 Oct 2020, 2300 UTC. Simulation ran from 2 days before landfall to 1 days after.

Gauges were selected based on the National Hurricane Center Tropical Cyclone Report* (https://www.nhc.noaa.gov/data/tcr/AL262020_Delta.pdf) 

The observed gauge data for sea level at each location was de-tided using the `fetch_noaa_tide_data()` method and plotted against the predicted storm surge by GeoClaw.

### Data Results:

------

The following chart gives the details of our simulation.

| Gauge  ID | Gauge Name                          | Original Location | Simulation Location*     | Observed Data** (m) | GeoClaw Simulation** (m) | Difference (m) |
| --------- | ----------------------------------- | ----------------- | ------------------------ | ------------------- | ------------------------ | -------------- |
| 8766072   | FRWL1, Freshwater Canal Locks, LA   | 29.55N,92.31W     | 29.5338694N, 92.31W      | 2.85                | 2.35                     | 0.5            |
| 8764227   | AMRL1, LAWMA, Amerada Pass, LA      | 29.45N, 91.34W    | 29.45N, 91.34W           | 2.00                | 1.37                     | 0.63           |
| 8768094   | CAPL1, Calcasieu Pass, LA           | 29.77N,93.34W     | 29.77N,93.34W            | 1.75                | 1.11                     | 0.64           |
| 8764314   | EINL1, North of Eugene Island, LA   | 29.37N,91.38W     | 29.37N,91.38W            | 0.9                 | 0.62                     | 0.28           |
| 8771341   | GNJT2, Galveston Bay Entrance, TX   | 29.37N,91.38W     | 29.37N,91.38W            | 1.1                 | 0.37                     | 0.73           |
| 8771972   | LUIT2, San Luis Pass, TX            | 29.08N,95.12W     | 29.08N,95.12W            | 1.1                 | 0.25                     | 0.85           |
| 8770822   | TXPT2, Texas Point, Sabine Pass, TX | 29.69N,93.84W     | 29.6658299N, 93.8235194W | 1.26                | 1.6                      | 0.34***        |
| 8772471   | FPST2, Freeport SPIP, TX            | 28.94N,95.29W     | 28.94N,95.29W            | 1                   | 0.3                      | 0.7            |
| 8771486   | GRRT2, Galveston RR Bridge, TX      | 29.30N,94.90W     | 29.30N,94.90W            | 1                   | 0.62                     | 0.38           |
|           |                                     |                   |                          |                     | Average Diff. (m)        | 0.561          |

*The simulation location might be different from the original data due to the limitation of topography data precision level.

**Maximum Height of Storm Surge

***The simulation value is higher than the observation data and we took the absolute value.

By adjusting the location, we avoided the discrepancies in results. 

### Conclusion:

------

Storm surge simulation we obtained from GeoClaw are generally inconsistent with the observed data. In most cases, the observed storm surge greatly exceeded the amount predicted by the GeoClaw model. The reason for this likely comes from the Michael's historic rains, which caused significant flooding. But this rainfall is not accounted in the model of GeoClaw Simulation. Adjustments to the GeoClaw model to incorporate rainfall may lead to more accurate results.



**This project was begun by Yusong Deng under the supervision of K. Mandli.**