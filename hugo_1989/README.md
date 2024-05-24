# Hurricane Hugo Validation Study

## Introduction

Hurricane Hugo was a category 5 storm that developed in the Atlantic during the
1989 season. It traveled west to the Caribbean, hitting Puerto Rico and
surrounding islands September 18, 1989. At 4:00 UTC (or midnight EST) on
September 22, 1989, Hurricane Hugo made its final landfall as a category 4
hurricane in Sullivan’s Island, SC, a barrier island just north of Charleston.
The storm’s winds reached 140 mph and a minimum central pressure of 27.58
inches Hg. This caused tremendous damage along the South Carolina coast and
surrounding areas, making Hugo the costliest U.S. storm with damages totaling
$7 billion. There were 49 deaths related to the storm. Hurricane Hugo produced
the highest storm tide heights on the American East Coast in recorded history.

Source: https://www.weather.gov/chs/HurricaneHugo-Sep1989

## Storm Data

Data to run the simulation was retrieved from NOAA’s storm data archive:
http://ftp.nhc.noaa.gov/atcf/archive/2017/bal111989.dat.gz

As this hurricane occurred in 1989, there are missing pieces of data necessary
for this simulation that were not recorded in the storm data file. This missing
data was extracted using a separate Python script containing functions that
relate known data to these unknowns.

## Topography/Bathymetry Data

A topography data file for the entire Atlantic was used for this simulation.  It
is recommended that you fetch a topography file that covers the computational
domain from GEBCO to your desired resolution.

Domain - (90 W, 60 W) Longitude
         (15 N, 40 N) Latitude

Source: https://download.gebco.net/

## Geoclaw setup
* Landfall: September 22, 1989 4:00 UTC
* Maximum levels of refinement: 4

Extra refinement was added around the gauges to account for detailed topography along the coast.
* Gauge 1: min 4, max 6
* Gauge 2: min 8, max 8
* Gauge 3: min 4, max 6

## Comparison Data

Water levels from three gauges in the area of Hurricane Hugo’s impact were
compared to the simulation’s results. Gauge data was taken from the NOAA
inundations dashboard: https://tidesandcurrents.noaa.gov/inundationdb/ 

The data had to be manually downloaded from the dashboard and uploaded into the
script due to its age. The folder titled ‘gauges’ houses data for the three
gauges, under their NOAA IDs.

Gauge 1: Charleston, SC
* NOAA ID: 8665530
* Location: -79.92351, 32.7806818
* Max Surge: ~3m

Gauge 2: Wilmington, NC
* NOAA ID: 8658120
* Location: -77.9534709, 34.2274321
* Max Surge: ~1m

Gauge 3: Duke Marine Lab, NC
* NOAA ID: 8656483
* Location: -76.6699314, 34.7200556
* Max Surge: ~1m

## Results

The simulation returns data for gauges 1 and 3. The general timing and height of
the surge match for these gauges. The model predicts the surge occurring a bit
before the actual surge both times, but this is likely due to estimations in
the landfall time rather than a modeling error. There is insufficient
refinement for gauge 2. This gauge is located deep into the Cape Fear River, so
higher refinement levels are necessary for the model to accurately estimate
this detailed topography.

There were simplifications taken in extracting the missing storm data, but they
did not significantly affect accuracy. Added extra refinement around the gauges
worked 2 of out 3 times without a loss of efficiency.

## Conclusion

The model ran using estimations of missing data without significant loss of
accuracy. The model was able to refine areas with detailed topography while
maintaining efficiency to an extent.

## Future Work

Next steps include running the simulation with higher refinement levels and
modifying the model to account for river topography. The estimation of missing
storm data can be extended to create fully synthetic storms. We can use these
storms to model effects due to climate change by running them through this
software.

This study was completed by Riley Fisher as a part of the Columbia-Amazon Summer
Undergraduate Research Experience (2022).
