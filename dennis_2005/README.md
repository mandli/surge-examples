## Hurricane Dennis Storm Surge Example


# Hurricane Dennis:
Hurricane Dennis was an early-forming major hurricane in the Caribbean and Gulf of Mexico during the record-breaking 2005 Atlantic hurricane season. It was the fourth storm, second hurricane, and first major hurricane. The tropical wave that became hurricane Dennis was identified on June 26, 2005, inland over Africa. It emerged over the Atlantic Ocean on June 29 and moved quickly to the west. The storm achieved tropical storm status on July 5 and hurricane status the following day from where it intensified into a major hurricane on July 7. Dennis first struck Granma Province, Cuba as a Category 4 hurricane on July 8 and attained its peek wind speed paralleling the southwestern coast of cuba at 150 miles per hour (240 km/h) later that day before making its second landfall in Matanzas Province. Dennis emerged over the Gulf of Mexico on July 9 and reached Category 4 strength for the third time on July 10 as it approached the northern tail of Florida where it attained its lowest barometric pressure of 930 mbar (hPa; 27.46 inHg). Dennis was directly responsibel for 42 deaths and the American Insurance Services Group estimated the insured property da,mage in the United States at $1.115 billion.
Source: NOAA (National Oceanic and Atmospheric Administration) Tropical Cyclone Report: Hurricane Dennis (https://www.nhc.noaa.gov/data/tcr/AL042005_Dennis.pdf)


# Storm data:
The data from the storm was taken from NOAA’s storm data archive found here: https://ftp.nhc.noaa.gov/atcf/archive/2005/. Hurricane Noel Dennis is found in the file bal042005.dat.gz. 


# Topography/Bathymetry data:
Topography file is stored in http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2 and extracted using the setrun.py file

To get more precise data, you can download a three arc-second topography file of a similar area in NetCDF format from here: https://www.ngdc.noaa.gov/mgg/coastal/grddas03/grddas03.htm.

# GeoClaw results:
After importing the storm data and the bathymetry data into setrun.py, the simulation reported there was half a meter to one meter rise in water level over the southern tip of the Gulf of Mexico from Florida to Alibama. The simulation ran from 2 days before landfall (July 8) to 2 days after landfall (November 12).

# Comparison data:
To validate the storm surge from the simulation, water level data from NOAA Tides and Currents were taken from three locations in Florida and one locations in Alabama, from days July 8 to July 12.


# Conclusion:
The NOAA verified water levels often showed higher surges than the predicted data on low resolution and would likely be more accurate with a greater resolution simulation and the inclusion of topography data of greater resolution close to the gauges. 
