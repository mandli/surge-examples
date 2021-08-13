

# Hurricane Laura 2020 Storm Report 

This example contains the data and setup for running a storm surge forecast for Hurricane Laura in 2020. 

## Hurricane Ophelia: 
Hurricane Laura can be traced as early as Augest 16, and became a tropical storm at Augest 21, causing minor surges near Puerto Rico, Dominican Republic and Cuba. 

It reached its max intensity of 130kt as it head toward coast of southwestern Louisiana, causing major landfall near the area and catogrized as a catogory 4 hurricane. Laura was the strongest hurricane to strike Louisiana since Hurricane Camille of 1969.

It then weakens as it moves through central America, causing no more major damage.

_Source: NOAA Tropical Cyclone Report (https://www.nhc.noaa.gov/data/tcr/AL132020_Laura.pdf)_

## Clawpack Installation:


Clawpack requires python(python3), fortran complier, and some environment variable setted to run.
Detailed installation instruction found here: https://www.clawpack.org/installing.html

Download _setrun.py_, _setplot.py_, and _Makefile_  to desired folder to run this example. 


## Storm data: 
                                                                  
Data for Clawpack to run simulation was taken from NOAA's storm data archive:
_https://ftp.nhc.noaa.gov/atcf/archive/2020/_

Hurricane Laura storm data was located in _bal132020.dat.gz_

In _setrun.py_, one can retrieve data directly from source by writing a code similar to this:
```sh
setrun.py:
line 421
    # Convert ATCF data to GeoClaw format
    clawutil.data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2020/bal132020.dat.gz")
    atcf_path = os.path.join(scratch_dir, "bal132020.dat")
```

## Topography/Bathymety data: 
_Topography data was accessed using GEBCO 2020 Gridded Bathymetry Data Download tool: 
https://download.gebco.net/_ 

Specifications to download topography:
Latitude: N 50, S 10
Longitude: W -105, E -50
Format: 2D netCDF Grid or Esri ASCII (depending on size of file one prefers) 

_Topography file in ASC format can be accessed in: https://www.dropbox.com/s/prnik1cr05hmn0v/Laura-2020-topo.asc?dl=0

In this example, the topography is located in the _Data_ folder within the project folder, create the folder as needed and change the following part of the code to access the topography file in your desired locaiton. 

```sh
setrun.py:
line 391
    topo_path = os.path.join("/home/michael/Desktop/Storm-Validation/Laura-2020/Data", "Laura-2020-topo.asc") 
```
Download topography data, add file to desired folder, but set the correct path from home folder to folder where file will be located, and add the name of the asc file as in this example.

##Simulation
To run the simulation, make sure _setrun.py_, _setplot.py_, and _Makefile_ are within the project folder, the topography file and the path to topography are specified in _setrun.py_.

Running
```
Make all
```
will run the whole simulation from start to finish. Run this to see the result for the first time

One can also specify only running output and plots by running
```
Make output
Make plots
```
This is mostly used to changes only plots without running the output (which takes the longest)

Adding dot in front of make argument will automatically run required command if previous step is missing
```
Make .output
Make .plots
```
This is highly recommanded to ensure all required data are generated


## GeoClaw results:
Simulation ran from 5 days before landfall: 2020-8-22, to 1 days after landfall: 2020-8-28. 

Gauges were selected from the NOAA current and Tide: https://tidesandcurrents.noaa.gov/map/index.shtml

Gauge locations were selected and specified in _setrun.py_ at line 327

```sh
setrun.py:
line 327
    # 1. Magueyes Island, PR,                                Station ID: 9759110,      17.9700 N, 67.0465 W        Landfall near Dominican Republick
    rundata.gaugedata.gauges.append([1, -67.0465, 17.9680, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # 2. Key West, FL,                                       Station ID: 8724580,      24.5510 N, 81.8085 W  
    rundata.gaugedata.gauges.append([2, -81.8085, 24.5510, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # 3. Cedar Key, FL,                                      Station ID: 8727520,      29.1300 N, 83.0313 W
    rundata.gaugedata.gauges.append([3, -83.0313, 29.1300, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # 4. Eugene Island, North of , Gulf of Mexico, LA,       Station ID: 8764314,      29.3730 N, 91.3830 W
    rundata.gaugedata.gauges.append([4, -91.3830, 29.3780, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # 5. Texas Point, Sabine Pass, TX,                       Station ID: 8770822,      29.6895 N,-93.8418 W        Major landfall Cameron Louisiana
    rundata.gaugedata.gauges.append([5, -93.8388, 29.6895, rundata.clawdata.t0, rundata.clawdata.tfinal])
```

The gauge data is obtained in _setplot.py_, no manual download needed. But if one is working with other data, modification of code and possibly manual download is needed for observation comparison. The following code add NOAA data to the gauge plot, removing the code will only show geoclaw output.

```sh
setplot.py:
line 174
    noaaArr = ["9759110", "8724580", "8727520", "8764314", "8770822", "None"]
    gaugeNumber = cd.gaugeno
    # Looking at  NOAA Gauges for corresponding gauge
    realData = geoutil.fetch_noaa_tide_data(noaaArr[gaugeNumber-1], datetime.datetime(2020, 8, 22, hour=6), datetime.datetime(2020, 8, 29, hour=6))
    values = realData[1]-realData[2] # de-tide NOAA data
    times = []
    for time in realData[0]:
        times.append((time-numpy.datetime64("2020-08-27T06:00")).astype(float)/1440)
    plt.plot(times, values, color="g", label="real")
```

## Data Results: 

Gauge 2-3 have no significant surges and geoclaw predicted the water level to be 0.25m lower than observed data.

Gauge 1 have minor surges about 4 day before major landfall. Geoclaw prediction have water level being 0.25m lower and time to be about 6h before observed data

Gauge 4-5 are near major landfall at texas point (Cameron Louisiana). Geoclaw predicted the water level 0.5m lower on average with accurate timing.

Since Geoclaw always assume sealevel is at 0, one could justify normalizing the NOAA data, then Geoclaw is accurate for gauge 1-3, while having only 0.25m lower water level for gauge 4-5. Geoclaw also predicted a large water level spike at exact landfall time for gauge 5, which is higher than observed.

One significant problem is that at 2 day after major landfall, the simulation result in the whole atlantic ocean having lower water level, which isn't realistic. On the otherhand the surges water level and time are all fairly accurate

## Conclusion: 
Storm surges obtained from Clawpack were within order of magnitude, although containing mild inconsistency between different gauges, but for gauges that are close to each other (gauge 4-5 are close, gauge 1-3 are far from 4-5 while also being spread out between itself) geoclaw is precise. 

These inconsistency could arise from gauges location close to land, thus a higher resolution of topography file maybe needed along with better refinement resolution (the refinement level used in the example exceed the topography file's resolution already), or other gauges further from land should be selected.

Overall Geoclaw storm surge result is an comparible model to real-life storm surges.

----------------------------------------------------------------------------------------

Michael Liu (yl4654@columbia.edu)


