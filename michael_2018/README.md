## Hurricane Michael Storm Report (AL142018)

------

This folder contains the data and code to run a storm surge simulation for Hurricane Michael

### Hurricane Michael

------

Hurricane Michael was a category 5 hurricane (on the Saffir-Simpson Hurricane Wind Scale) that made a catastrophic landfall near Mexico Beach and Tyndall Air Force Base, FL. It was directly responsible for 16 deaths and about $25 billion in damage in the United States. Hurricane Michael got a complex synoptic history, for details, you may refer to the NOAA report on Hurricane Michael [1]. Based on minimum pressure, Michael is the fourth most-powerful hurricane to hit the United States, behind the Labor Day Hurricane (1935), Hurricane Camille (1969) and Hurricane Andrew (1992), and the most powerful storm to impact the Florida Panhandle in recorded history. Hurricane Michael making landfall near Tyndall Air Force Base (AFB) in the Florida Panhandle, southeast of Panama City, near 1730 UTC that day. By that time, the maximum sustained winds had increased to an estimated 140 kt – category 5 on the SaffirSimpson Hurricane Wind Scale (SSHWS). 

If running this example, download setrun.py, setplot.py, and Makefile to the appropriate directory. Execute `$ make all` to compile the code, run the simulation, and plot the results.

*Source: 1. National Hurricane Center Tropical Cyclone Report* (https://www.nhc.noaa.gov/data/tcr/AL142018_Michael.pdf)                                                                                                                      			*2. National Weather Service, NOAA Information Page* ([https://www.weather.gov/tae/HurricaneMichael2018](https://www.nhc.noaa.gov/data/tcr/AL142018_Michael.pdf))

### Storm Data

------

Data to run the simulation was retrieved from NOAA’s storm data archive: http://ftp.nhc.noaa.gov/atcf/archive/2018/bal142018.dat.gz

In setrun.py, data can be directly retrieved from the source by writing code similar to this:

```python
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file(“http://ftp.nhc.noaa.gov/atcf/archive/2018/bal142018.dat.gz”)
atcf_path = os.path.join(data_dir, “bal142018.dat”)
```

For this example, Hurricane Harvey storm data should be placed in the scratch directory ($CLAW/geoclaw/scratch) that the simulation is run in.

### Topography/Bathymetry Data:

------

Topography data is provided in this folder as well in the name of North45_South0_West-105._East-35.tt3. The file should be downloaded and placed in the scratch directory as the Storm Data

### GeoClaw Parameters:

------

Time of landfall was set in the simulation to be 10 Oct, 1700 UTC. Simulation ran from 2 days before landfall to 1 days after.

Gauges were selected based on the National Hurricane Center Tropical Cyclone Report* (https://www.nhc.noaa.gov/data/tcr/AL142018_Michael.pdf) 

The observed gauge data for sea level at each location was de-tided using the `fetch_noaa_tide_data()` method and plotted against the predicted storm surge by GeoClaw.

### Data Results:

------

The following chart gives the details of our simulation.

| Gauge  ID | Gauge Name                   | Original Location   | Simulation Location*     | Observed Data** (m) | GeoClaw Simulation** (m) | Difference (m)  |
| --------- | ---------------------------- | ------------------- | ------------------------ | ------------------- | ------------------------ | --------------- |
| 8728690   | APCF1, Apalachicola, FL      | 29.724N, 84.980W    | 29.724N, 84.980W         | 2.60                | 1.25                     | 1.35            |
| 8726724   | CWBF1, Clearwater Beach, FL  | 29.978N, 82.832W    | 27.9841164N, 82.8532264W | 1.00                | 0.24                     | 0.76            |
| 8729108   | PACF1, Panama City, FL       | 30.1517N, 85.6667W  | 30.1517N, 85.6667W       | 1.75                | 0.50 (0.37***)           | 1.25(1.37***)   |
| 8729210   | PCBF1, Panama City Beach, FL | 30.2133N, 85.87830W | 30.2095418N, 85.8808554W | 1.25 (1.13***)      | 0.51 (0.48***)           | 0.74(0.65***)   |
| 8726607   | OPTF1, Old Port Tampa, FL    | 27.86N, 82.55W      | 27.8602907N, 82.5518544W | 0.73                | 0.20                     | 0.53            |
| 8729840   | PCLF1, Pensacola, FL         | 30.40N, 87.21W      | 30.40N, 87.21W           | 1.00                | 0.25                     | 0.75            |
|           |                              |                     |                          |                     | Average Diff. (m)        | 0.897(0.902***) |

*The simulation location might be different from the original data due to the limitation of topography data precision level.

**Maximum Height of Storm Surge

***The data indicate the maximum storm surge water value after landfall, this value is lower than the data without the sign, which is the water level before landfall.

By adjusting the location, we avoided the discrepancies in results. As a CAT 5 Hurricane, the significant raindrop of Michael is a great contributor to the measured storm surge. This factor is not accounted for in the GeoClaw simulation. 

### Conclusion:

------

Storm surge simulation we obtained from GeoClaw are generally inconsistent with the observed data. In most cases, the observed storm surge greatly exceeded the amount predicted by the GeoClaw model. The reason for this likely comes from the Michael's historic rains, which caused significant flooding. But this rainfall is not accounted in the model of GeoClaw Simulation. Adjustments to the GeoClaw model to incorporate rainfall may lead to more accurate results.



**This project was begun by Yusong Deng under the supervision of K. Mandli.**