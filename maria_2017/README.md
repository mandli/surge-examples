# Maria 2017 Storm Surge Report
Within this directory are files for simulating Hurricane Maria (2017).

## Hurricane Maria: A Brief Synopsis
Maria (2017) was an Atlantic storm conceived off the coast of Western Africa. It grew from a tropical wave on September 12th to a powerful Category 5 hurricane by September 18th. Before making landfall on Puerto Rico, it hit a top wind speed of 280 km/h (175 mph), making it one of the most intense Atlantic storms on record. Maria struck Puerto Rico as a Category 4 hurricane on September 20th, 10:15 UTC, before traversing northward towards the East Coast of the United States. It then swung west out to sea, where its intensity was greatly reduced before finally dissipating on October 2nd.

## Storm Data
In order to run a simulation of Maria in GeoClaw, two pieces of data needed to be collected: (a) storm data detailing the coordinates and strength of the storm at regular intervals, and (b) topography data for the oceanic basin the storm took place in. Data for the storm was found within the [NOAA storm data archive](https://ftp.nhc.noaa.gov/atcf/archive/2017/).

The data for Hurricane Maria was found within the file `bal152017.dat.gz` (bal152017 means the storm was the 15th tropical storm in the Atlantic basin during the 2017 season). NOTE: The track file for Maria has a line about a transitioning storm (which this was).  The `setrun.py` file removes the extraneous lines from the original file.

## Topography
From the full GEBCO 2023 data set.  Requires NetCDF capabilities (see Makefile for appropriate flags).
  
## Simulating Maria & Comparing Results
The simulation was set to run from September 18th, 2017--two days before landfall--to September 21st, 2017--one day after landfall. The gauge locations were taken from real gauges on Puerto Rico and adjacent islands. The data for the real gauges were collected from the [NOAA Tides and Inundations website](https://tidesandcurrents.noaa.gov/inundationdb/).
 
Stations 1-4 recorded roughly 0.2 to 0.3 meters of rising water levels at their peak during the simulation. Station 5, which was located at Arecibo, PR, recorded a peak storm surge of approximately 0.5 meters. Compared with the real data collected by the gauges at those corresponding locations, the levels of flooding found in the simulation were consistently much lower. For the Arecibo gauge (Station 5), the simulated peak was 0.5 meters, while the real peak was 1.72 meters. The difference was more pronounced with other stations: the San Juan gauge (Station 4) recorded only about 0.2 meters, while the real data had a peak of 2.34 meters. The differences for Stations 1-3 are as follows: Station 1 on St. Croix in the Virgin Islands had a simulated peak of about 0.3 meters and a true peak of 1.99 meters; Station 2 on Vieques Island, PR had a simulated peak of about 0.3 meters, while having a true peak of 2.04 meters; and Station 3 was not a true gauge in real life, and merely placed to check the storm surge level on the Eastern edge of Puerto Rico. 
 
Based on this data, the simulated peaks were consistently at least a meter smaller than the real data, and in the case of Stations 1, 2, and 4, it was a difference of at least 1.5 meters. Station 4 had the most pronounced difference at 2.1 meters. There are several different ways this discrepancy could be explained. Firstly, it could be personal error; something in my code could have erroneously created a simulation of the storm in such a way that the surges created were significantly reduced. Secondly, it could be due to a discrepancy in the GeoClaw code that creates a simulation that "underestimates" the level of flooding caused by the storm. To test this second theory, one would need to create simulations of other storms and compare. If those same notable differences in simulated versus real data occur again, this would support the second theory; if the opposite occurs, then it is likely an error on my part that caused Maria's simulation to be so inaccurate.

## Conclusion

There were notable inconsistencies in the simulated data when compared with the real life data found at the gauges tested in this simulation. All the simulated data reached peaks that were noticeably smaller than the real ones; however, the times those peaks occurred, and the progression of the gauge graphs otherwise were similar to the real data. This suggests that the simulation was at least partially successful in simulating Maria, albeit with a notably smaller storm surge. This could have been due to a variety of factors: human error on my part, some inaccurate data gathered for either the storm itself or the topography, or, finally, some discrepancy in the calculations made by the GeoClaw program itself. 

Future simulations of Maria should attempt to correct these discrepancies, and/or diagnose their origins. 
