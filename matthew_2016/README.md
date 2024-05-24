
# Example of Storm Surge from Hurricane Matthew

This example provides the data and Python code for running a simulation of Hurricane Matthew along the Eastern Seaboard. 
Matthew made landfall approximately 30 miles northeast of Charleston, South Carolina, on October 8, 2016, as a Category 
1 storm. The simulation models three days of the storm, beginning two days before landfall over South Carolina.
* Start Date: 10 / 6 / 2016 - 12 UTC
* End Date: 10 / 9 / 2016 - 12 UTC

Running `make all` will compile all the necessary code for running the simulation.

## Topography

Topography data can be downloaded from 
* https://download.gebco.net
  * Use boundaries of N: 50.0, S: 10.0, W: -90.0, E: -60.0 
  * Use the Esri ASCII Grid format when downloading.
  
* https://www.ngdc.noaa.gov/thredds/fileServer/crm/crm_vol2.nc

It is automatically downloaded, however, by _setrun_.py
* The GEBCO topography file is stored here 
  * https://www.dropbox.com/s/s58bi1l45tw9uka/gebco_2020_n50.0_s10.0_w-90.0_e-60.0.asc?dl=1

into the `matthew/scratch` directory.

## Storm Data

Storm data is automatically downloaded from the NOAA atcf archive at 
http://ftp.nhc.noaa.gov/atcf/archive/2016/bal142016.dat.gz

into the `matthew/scratch` directory.

## Gauges

Gauges 1-5 in the example correspond to five NOAA Tides and Currents Stations along the Eastern Seaboard, selected from 
https://stn.wim.usgs.gov/FEV/#MatthewOctober2016. The`fetch_noaa_tide_data()` method is used to retrieve the observed 
gauge data (minus the tides) for comparison with GeoClaw's predictions.

1. Mayport (Bar Pilots Dock), FL 8720218 
2. Fort Pulaski, GA 8670870 
3. Charleston, Cooper River Entrance, SC 8665530 
4. Wrightsville Beach, NC 8658163 
5. Wilmington, NC 8658120

Coordinates for each gauge can be found in _setrun.py_.

## AMR Flagregions

Regions refined at higher levels are drawn in Google Earth as polygons and downloaded to _regions.kml_. The .kml file is
run through _kml2slu.py_ to allow its usage in setting AMR flagregions. 

Levels assigned to each flagregion can be found in _setrun.py_.

Raising the levels assigned to each region in _setrun_.py may provide more accurate storm surge predictions but will 
increase runtime.

The flagregions in this example are "Ruled Rectangles," covering the bodies of water surrounding each gauge. Opening 
_regions.kml_ in Google Earth will display the locations of the gauges along with their respective flagregions. 
## Storm Surge Comparison

Under the current AMR refinement ratios and levels, the following is a comparison between the observed and predicted 
storm surge peaks at each gauge.  

Gauge | Observed (m) | Observed Time (UTC) | GeoClaw (m) | GeoClaw Time (UTC) 
--- | --- | --- | --- | --- |
1| 1.428 | 10 / 7 / 2016 - 20:42 | 1.067 | 10 / 7 / 2016 - 19:32
2| 2.348 | 10 / 8 / 2016 - 07:48 | 1.294 | 10 / 8 / 2016 - 06:13
3| 1.890 | 10 / 8 / 2016 - 10:00 | 1.154 | 10 / 8 / 2016 - 11:46
4| 0.938 | 10 / 8 / 2016 - 13:30 | 0.468 | 10 / 8 / 2016 - 21:44
5| 1.245 | 10 / 8 / 2016 - 15:06 | 0.646 | 10 / 8 / 2016 - 20:54

* GeoClaw's surge predictions have been rounded to the nearest thousandth, and its time predictions have been rounded to
the nearest minute.

Observations in the table can be found on page 10 of this 
[NOAA report](https://tidesandcurrents.noaa.gov/publications/Hurricane_Matthew_2016_Water_Level_and_Meteorological_Data_Report.pdf).
</br>
The GeoClaw predictions in the table can be reproduced with the following code after running the simulation.
```
import os
import numpy as np
import datetime

total_gauges = 5
landfall_date = datetime.datetime(2016, 10, 8, 12)

for i in range(1, total_gauges + 1):
    with open((os.getcwd() + "/_output/gauge0000" + str(i) + ".txt"), "r") as file:
        surges, times = [], []
        for num, line in enumerate(file, 1):
            if num < 4:
                continue
            line = line.strip().split()
            surges.append(float(line[5]))
            times.append(line[1])

        msurge = np.max(surges)
        date = landfall_date + datetime.timedelta(seconds=float(times[surges.index(msurge)]))
        print(f"Gauge {i}:  surge = {msurge}  date = {date}")
```
## Conclusion

Storm surges predicted by GeoClaw occurred at relatively similar times as the actual surges, but GeoClaw consistently
undershot the peaks. Higher-resolution topography files and higher AMR refinement ratios or levels may be needed for 
more accurate predictions.

For questions, contact Brandon Maher at brandmaher@gmail.com