<h1>Maria 2017 Storm Surge Report</h1>
Within this directory are files for simulating Hurricane Maria (2017).

<h2>Hurricane Maria: A Brief Synopsis</h2>
Maria (2017) was an Atlantic storm concieved off the coast of Western Africa. It grew from a tropical wave on September 12th to a powerful Category 5 hurricane by September 18th. Before making landfall on Puerto Rico, it hit a top wind speed of 280 km/h (175 mph), making it one of the most intense Atlantic storms on record. Maria struck Puerto Rico as a Category 4 hurricane on September 20th, 10:15 UTC, before traversing northward towards the East Coast of the United States. It then swung west out to sea, where its intensity was greatly reduced before finally dissipating on October 2nd.

<h2>Storm Data</h2>
In order to run a simulation of Maria in GeoClaw, two pieces of data needed to be collected: (a) storm data detailing the coordinates and strength of the storm at regular intervals, and (b) topography data for the oceanic basin the storm took place in. Data for the storm was found within the NOAA storm data archive.

LINK: https://ftp.nhc.noaa.gov/atcf/archive/2017/

The data for Hurricane Maria was found within the file "bal152017.dat.gz" (bal152017 means the storm was the 15th tropical storm in the Atlantic basin during the 2017 season). NOTE: Unlike other data files on the site, the file for Maria had an erroneous extra column of data in each row that made it impossible for GeoClaw to simulate it. In order to reproduce this simulation, one must either manually go through and delete each line of this data, or use the .dat.gz file I've attached in this directory for convenience. 

In order to simulate the storm, there must be code added to your setrun.py file that extracts a .dat file from the given .dat.gz file. See below:

```
clawutil.data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2002/bal152017.dat.gz")
atcf_path = os.path.join(scratch_dir, "bal152017.dat")
```

<h2>Topography Data</h2>
After finding the storm data, the next step was to locate and download topography data for the Atlantic basin. There are several sites where this can be done, but topography for the Maria simulation was downloaded from the GEBCO site: https://download.gebco.net
To download the topography data, four coordinates encompassing the area that Hurricane Maria traversed in 2017 were input into the "Boundaries" section, "GEBCO 2021" was selected as the preferred map, and finally, Esri ASCII was chosen as the format for the data given. The format is up to one's personal preference; if using ASCII, a similar section of code to the one below should be in the setrun.py file:

From setrun.py:

lines 399-400:

```
topo_path = os.path.join(scratch_dir, 'maria-atlantic17.asc')
topo_data.topofiles.append([3, topo_path])
```
 
 <h2>File Organization</h2>
 The unique files necessary to run the simulation are as follows: setrun.py, setplot.py, Makefile, name_of_storm_data_file, name_of_topography_file
 
 The setrun.py, setplot.py, and Makefile files should all be within the main directory for the storm (e.g. "/Maria"), while the storm and topography data files should be in a separate file for data (e.g. "/Maria/data"). Modify the code within setrun.py to reflect the proper path to your data files. In this case, the storm and topography files were placed in the pre-existing directory "/scratch", and a short-cut to the path of this directory was written into setrun.py as the variable "scratch_dir". One could use a similar method to reproduce this example or others. 
 
 <h2>Simulating Maria & Comparing Results</h2>
 The simulation was set to run from September 18th, 2017--two days before landfall--to September 21st, 2017--one day after landfall. The gauge locations were taken from real gauges on Puerto Rico and adjacent islands. The data for the real gauges were collected from the NOAA Tides and Inundations website: https://tidesandcurrents.noaa.gov/inundationdb/
 
 Stations 1-4 recorded roughly 0.2 to 0.3 meters of rising water levels at their peak during the simulation. Station 5, which was located at Arecibo, PR, recorded a peak storm surge of approximately 0.5 meters. Compared with the real data collected by the gauges at those corresponding locations, the levels of flooding found in the simulation were consistently much lower. For the Arecibo gauge (Station 5), the simulated peak was 0.5 meters, while the real peak was 1.72 meters. The difference was more pronounced with other stations: the San Juan gauge (Station 4) recorded only about 0.2 meters, while the real data had a peak of 2.34 meters. The differences for Stations 1-3 are as follows: Station 1 on St. Croix in the Virgin Islands had a simulated peak of about 0.3 meters and a true peak of 1.99 meters; Station 2 on Vieques Island, PR had a simulated peak of about 0.3 meters, while having a true peak of 2.04 meters; and Station 3 was not a true gauge in real life, and merely placed to check the storm surge level on the Eastern edge of Puerto Rico. 
 
Based on this data, the simulated peaks were consistently at least a meter smaller than the real data, and in the case of Stations 1, 2, and 4, it was a difference of at least 1.5 meters. Station 4 had the most pronounced difference at 2.1 meters. There are several different ways this discrepancy could be explained. Firstly, it could be personal error; something in my code could have erroneously created a simulation of the storm in such a way that the surges created were significiantly reduced. Secondly, it could be due to a discrepancy in the GeoClaw code that creates a simulation that "underestimates" the level of flooding caused by the storm. To test this second theory, one would need to create simulations of other storms and compare. If those same notable differences in simulated versus real data occur again, this would support the second theory; if the opposite occurs, then it is likely an error on my part that caused Maria's simulation to be so inaccurate.
