<h1>Maria 2017 Storm Surge Report</h1>
Within this directory are files for simulating Hurricane Maria (2017).

<h2>Hurricane Maria: A Brief Synopsis</h2>
Maria (2017) was an Atlantic storm concieved off the coast of Western Africa. It grew from a tropical wave on September 12th to a powerful Category 5 hurricane by September 18th. Before making landfall on Puerto Rico, it hit a top wind speed of 280 km/h (175 mph), making it one of the most intense Atlantic storms on record. Maria struck Puerto Rico as a Category 4 hurricane on September 20th, 10:15 UTC, before traversing northward towards the East Coast of the United States. It then swung west out to sea, where its intensity was greatly reduced before finally dissipating on October 2nd.

<h2>Storm Data</h2>
In order to run a simulation of Maria in GeoClaw, two pieces of data needed to be collected: (a) storm data detailing the coordinates and strength of the storm at regular intervals, and (b) topography data for the oceanic basin the storm took place in. Data for the storm was found within the NOAA storm data archive.

LINK: https://ftp.nhc.noaa.gov/atcf/archive/2017/

The data for Hurricane Maria was found within the file "bal152017.dat.gz" (bal152017 means the storm was the 15th tropical storm in the Atlantic basin during the 2017 season). NOTE: Unlike other data files on the site, the file for Maria had an erroneous extra column of data in each row that made it impossible for GeoClaw to simulate it. In order to reproduce this simulation, one must either manually go through and delete each line of this data, or use the .dat.gz file I've attached in this directory for convenience. 

In order to simulate the storm, there must be code added to your setrun.py file that extracts a .dat file from the given .dat.gz file. See below:

`clawutil.data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2002/bal152017.dat.gz")
atcf_path = os.path.join(scratch_dir, "bal152017.dat")`

<h2>Topography Data</h2>
After finding the storm data, the next step was to locate and download topography data for the Atlantic basin. There are several sites where this can be done, but topography for the Maria simulation was downloaded from the GEBCO site: https://download.gebco.net
To download the topography data, four coordinates encompassing the area that Hurricane Maria traversed in 2017 were input into the "Boundaries" section, "GEBCO 2021" was selected as the preferred map, and finally, Esri ASCII was chosen as the format for the data given. The format is up to one's personal preference; if using ASCII, a similar section of code to the one below should be in the setrun.py file:

From setrun.py:

lines 399-400:

`topo_path = os.path.join(scratch_dir, 'maria-atlantic17.asc')
 topo_data.topofiles.append([3, topo_path])`
 
 <h2>File Organization</h2>
 The unique files necessary to run the simulation are as follows: setrun.py, setplot.py, Makefile, name_of_storm_data_file, name_of_topography_file
 
 The setrun.py, setplot.py, and Makefile files should all be within the main directory for the storm (e.g. "/Maria"), while the storm and topography data files should be in a separate file for data (e.g. "/Maria/data"). Modify the code within setrun.py to reflect the proper path to your data files. In this case, the storm and topography files were placed in the pre-existing directory "/scratch", and a short-cut to the path of this directory was written into setrun.py as the variable "scratch_dir". One could use a similar method to reproduce this example or others. 
 
 
