## Hurricane Noel GeoClaw Storm Surge Report


# Hurricane Noel:
The sixth storm of the 2007 hurricane season, Hurricane Noel, formed on October 27, 2007 and traveled from the Caribbean islands across the Atlantic to Newfoundland. On October 28th, it became a tropical storm and made landfall near Jacmel, Haiti on October 29th. It moved North towards the Dominican Republic, then Southwest into Cuba and made landfall again near Guardalavaca, Cuba. It turned North towards the Bahamas and became classified as a Hurricane on November 1st. It then became an extratropical cyclone and weakened as it went up to Newfoundland until it merged with another extratropical storm. This storm was the deadliest of the 2007 Hurricane season, with a total of 163 deaths and 59 missing, most of them from the Dominican Republic and Haiti. 
Source: NOAA (National Oceanic and Atmospheric Administration) Tropical Cyclone Report: Hurricane Noel (https://www.nhc.noaa.gov/data/tcr/AL162007_Noel.pdf). 

# Storm data:
The data from the storm was taken from NOAA’s storm data archive found here: https://ftp.nhc.noaa.gov/atcf/archive/2007/. Hurricane Noel data is found in the file bal162007.dat.gz. 

# Topography/Bathymetry data:
Topography/bathymetry data for the Atlantic ocean was taken from the NOAA Grid Extract website where you can extract Earth surface data (https://maps.ngdc.noaa.gov/viewers/grid-extract/index.html). An ETOPO1 (ice) area of  longitude around -89.83 W to -28.62 W, and latitude 12.96 N to 63.80 N was extracted, which is most of the Atlantic ocean, North America, and the Caribbean. The data from this website was of type .tif, so it was converted to NetCDF so it was compatible with GeoClaw through this website: https://mygeodata.cloud/converter/tif-to-netcdf. This topography data was imported into a separate directory and it was then called from setrun.py

# GeoClaw results:
After importing the storm data and the bathymetry data into setrun.py, the simulation reported there was no significant change in water level in Florida, the Bahamas, and Puerto Rico, indicating there was little to no storm surge. The simulation ran from 3 days before landfall (October 26) to 5 days after landfall (November 3).

# Comparison data:
To validate the storm surge from the simulation, water level data from NOAA Tides and Currents were taken from two locations in Florida and two locations in Puerto Rico, from days October 26th to November 3rd, and downloaded as csv files. The data was taken in 6 minutes intervals. The predicted water levels were subtracted from the observed water levels, and then graphed alongside the GeoClaw water level data for storm surge comparison. Below are the locations and the NOAA water level websites:
Virginia Key, Biscayne Bay, FL: https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8723214
Key West, FL:
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8724580
Magueyes Island, PR:
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=9759110
Mona Island, PR:
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=9759938 
The python file comparison_gauge_data.py was used to convert the csv files into data with dates relative to landfall and then converted into a text file.

For the Bahamas, there was no scientific water level data found, therefore the storm surge was compared to flooding heights taken from two different newspapers:
https://bahamaspress.com/rum-cay-have-its-share-of-heavy-rains/
https://ufdc.ufl.edu/UF00084249/03028/1x 

# Conclusion:
The NOAA water level data for Florida and Puerto Rico were mostly consistent with the storm surge from GeoClaw.
The flood height was extremely different from the storm surge in the Bahamas. This means the flooding was most likely not caused by storm surge. After looking at the NOAA report and NASA data (https://earthobservatory.nasa.gov/images/8185/rain-from-tropical-storm-noel), the amount of rain in the Bahamas was somewhere around 500 mm (20 in.), and in Long Island it was even recorded to be 29.43 in. Therefore, this explains the amount of flooding in the Bahamas.
The lack of storm surge is consistent with what it’s stated in the NOAA report. The storm was likely traveling too fast to create any significant storm surge.



