# Hurricane Irene Storm Report
A Category 1 storm made landfall on August 27, 2011 near Cape Lookout, North Carolina. Irene left flood and wind damage along the path.
Precipitation levels ranged from 5 inches near the Northern Outer Banks to 15 inches in Beaufort County, South Carolina. 

This example contains the data and setup for running a storm surge forecast for Hurricane Irene.


Topography data was accessed using Grid Extract NOAA website. 
Coastal Relief Model was selected as the dataset.
Latitude was specified to be -90 to -30 and longitude of 10 to 65. 
Data was downloaded. 
An online converter was used to convert the file from TIF to NETCDF. 
Topography file was uploaded to a folder in GeoClaw directory.

A separate folder was created to hold setrun.py, setplot.py, and MAKE files. 
Data directory was changed to path containing topography file.
Location of gauges was edited to see storm surge in Cape Lookout, NC(landfall area), Chesapeake Bay, Atlantic City, Sandy Hook, Connecticut, and Boston.
Initial time and final time were edited to three days before and after landfall date.

# Comparison Data
Gauges were selected in NOAA Inundations dashboard and matched locations specified in setrun file.
Time frame was changed from Aug 24, 2011 to Aug 30, 2011. Data was taken in 6 minute intervals. Data downloaded as CSV file.
Calculated difference in storm surge in Excel by subtracted predicted storm surge from actual storm surge. Multiplied value by 0.3048 to convert from ft to m.
Calculated time in days in Excel.

Saved data as a text file and uploaded to Irene directory.

# Data Results:
Duke Marine Lab, NC experienced storm surge of approximately 0.9 m. However, GeoClaw predicts close to 0.5 m of storm surge.
Kiptopeke Beach, Va experienced 1.0 m of storm surge. GeoClaw predicted 0.5 m of storm surge.
Atlantic City, NJ experienced 1.0 m of storm surge. GeoClaw predicted 0.4 m of storm surge.
Sandy Hook, NJ experienced 1.4 m of storm surge. GeoClaw predicted 0.5 m of storm surge.
New London, CT experienced 1.1 m of storm surge. GeoClaw predicted less than 0.4 m of storm surge.
Boston, MA experienced 0.5 m of storm surge. GeoClaw predicted 0.2 m of storm surge.
In each case, GeoClaw data is lower than actual data at peak points.

# Sources
https://www.weather.gov/mhx/Aug272011EventReview
Topography data:
https://maps.ngdc.noaa.gov/viewers/grid-extract/index.html
Topography File Converter:
https://mygeodata.cloud/converter/tif-to-netcdf
Data from NOAA:
Duke Marine Lab, NC
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8656483&units=standard&bdate=20110824&edate=20110830&timezone=LST/LDT&datum=MHHW&interval=6&action=
Kiptopeke Beach, VA
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8632200&units=standard&bdate=20110824&edate=20110830&timezone=LST/LDT&datum=MHHW&interval=6&action=
Atlantic City, NJ
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8534720&units=standard&bdate=20110824&edate=20110830&timezone=LST/LDT&datum=MHHW&interval=6&action=
Sandy Hook, NJ
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8531680&units=standard&bdate=20110824&edate=20110830&timezone=LST/LDT&datum=MHHW&interval=6&action=
New London, CT
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8461490&units=standard&bdate=20110824&edate=20110830&timezone=LST/LDT&datum=MHHW&interval=6&action=
Boston, MA
https://tidesandcurrents.noaa.gov/inundationdb/inundation.html?id=8443970&units=standard&bdate=20110824&edate=20110830&timezone=LST/LDT&datum=MHHW&interval=6&action=
