#Hurricane Frederic:
Soon to be a category 4 hurricane, hurricane Frederic formed as a tropical depression on August 29, 1979, in the Caribbean. It traveled northwards over the Caribbean islands, making landfall on the Gulf coast. On September 12, 1979, Frederic made landfall on Dauphin Island, AL near Mobile, AL. The storm brought sustained winds of 215 km/h and a minimum pressure of 943 mbar. After landfall, Frederic continued on a northeastern path but weakened and merged with an extratropical cyclone. It lightly affected the Mid-Atlantic and New England states before finally ending in Quebec, Canada. Over the course of its lifespan, Frederic caused over $2.3 billion in damages and lead to the evacuation of over 500,000 people making it the costliest storm and the largest evacuation the US had experienced up to that point. Fortunately, only 5 deaths were caused as a direct result of the storm.
Sources:
https://www.weather.gov/mob/frederic
https://www.al.com/hurricane/2019/09/remembering-hurricane-frederic-40-years-ago-today.html
https://en.wikipedia.org/wiki/Hurricane_Frederic

#Storm data:
Storm data was acquired from the Atlantic Ocean & Meteorological Laboratory's HURDAT database: https://www.aoml.noaa.gov/hrd/hurdat/Data_Storm.html
The file was then put in the scratch directory.
Data was loaded by the following code in setrun.py:
atcf_path = os.path.join(scratch_dir, "HurdatData.txt")#"bal111979.dat")
frederic = Storm(path=atcf_path, file_format="HURDAT")

#Topography/Bathymetry data:
The topography from the Hurricane Ike example was reused for Frederic since both storms took place primarily in the Gulf Coast region.

Source: http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2

An additional topography file was used to supplement regions surrounding the simulated gauge locations.
The topography data was downloaded from the GEBCO Gridded Bathymetry Data Download website: https://download.gebco.net/

The file's format is Esri ASCII and was placed in the scratch directory.
File was loaded into geoclaw with the following code in setrun.py:
topo_path2 = os.path.join(scratch_dir, 'mobile_bay.asc')
topo_data.topofiles.append([3, topo_path2])

It is included in the GitHub directory as 'mobile_bay.asc'.

#GeoClaw setup:
As a storm from 1979, the ATCF and HURDAT data files for Frederic lack some information that is present for more recent storms. Thus, the max wind radius and storm radius had to be set manually within the storm.py file.
The code is below:
self.max_wind_radius[i] = 26500
self.storm_radius[i] = 500000

storm radius was set to 500,000 m to make sure to cover the entire storm domain. max_wind_radius was set to 26,500 m in as per data from the paper "The Transition of the Hurricane Frederic Boundary-Layer Wind Field from the Open Gulf of Mexico to Landfall"

Source: https://journals.ametsoc.org/view/journals/mwre/110/12/1520-0493_1982_110_1912_ttothf_2_0_co_2.xml?tab_body=pdf

#Comparison to Historical Data
To validate the results of the simulation, historical data of water levels around the landfall area were sought out. Only one gauge with accessible data was active at the time of Hurricane Frederic: The Pensacola, FL station. Other observations were acquired from the United States Geological Survey (USGS) report on Hurricane Frederic (Can be found here: https://pubs.er.usgs.gov/browse/Report/USGS%20Numbered%20Series/Hydrologic%20Atlas/). Data from USFS were reported with respect to the National Geodetic Vertical Datum of 1929 (NGVD 29) whereas the Geoclaw simulation uses the North American Vertical Datum of 1988 (NAVD 88). Thus, USGS data were converted to NAVD 88 according to the following Vertcon Map: https://www.ngs.noaa.gov/TOOLS/Vertcon/Vertcon_Map.html. The values were then converted from feet to meters to make them comparable to results from the simulation.

Pensacola, FL
- Latitude: 30° 24.3 N = 30.405°
- Longitude: 87° 12.7 W = -87.21°
- Max flooding: 1.297 m
Source: https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8729840&units=metric&bdate=19790911&edate=19790914&timezone=GMT&datum=MHHW&interval=h&action=

Mobile, AL
- Latitude: 30.60°
- Longitude: -88.0399°
- Max flooding: 3.466 m
Source: https://pubs.usgs.gov/ha/624/plate-1.pdf

Dauphin Island, AL
- Latitude: 30.243971°
- Longitude: -88.130710°
- Max flooding: 3.8929 m
Source: https://pubs.usgs.gov/ha/627/plate-1.pdf

Gulf Shores, AL
- Latitude: 30.225729°
- Longitude: -87.686317°
- Max flooding: 3.375 m
Source: https://pubs.usgs.gov/ha/635/plate-1.pdf

Bayou La Batre, AL
- Latitude: 30.398325°
- Longitude: -88.329254°
- Max flooding: 2.918 m
Source: https://pubs.usgs.gov/ha/622/plate-1.pdf

#Analysis
Simulated results for the Mobile gauge came in at 4 m, ~0.5 m higher than the maximum observed value. However, results from Pensacola, Dauphin Island, Gulf Shores, and Bayou La Batre were lower than the observed amounts by ~0.5 m, ~2.3 m, ~1.0 m, ~1.4 m respectively. Although there were significant deviations from the observed data, the simulation predicted the correct general trend of the storm surge. 
Possible sources of error may include:
- Change in topography: topography files are based on the current shoreline/water level which may be different from that in 1979
- Lack of storm/wind radius data: These were set as a constant value throughout the simulation, so information about their variation is lost
- Variation in observed data: Although the maximum observed value was used, the USGS maps show that Storm Surge observations can vary widely across even small distances.

#Future Work
Topography data circa 1979 may be found at the USGS Topoview website (https://ngmdb.usgs.gov/topoview/viewer/#9/30.6438/-88.0815), downloaded in GeoTIFF format, converted to NetCDF via the MyGeodata converter (https://mygeodata.cloud/converter/geotiff-to-netcdf), and processed into .tt3 by Clawpack. Using historical topography could lead to more accurate results.

----------------------------------------------------------------------------------------

Contact Aniv Ray (ar4180@columbia.edu) with any questions.