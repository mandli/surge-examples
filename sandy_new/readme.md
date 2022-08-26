# Hurricane Sandy Storm Report (AL182012)
The folder contains an updated version of the code that simulates Hurricane Sandy in late October 2012.

## General Information About Hurricane Sandy
Hurricane Sandy was a Category 3 hurricane that started out in the southwestern Carribean Sea. The origin of this hurricane is associated with a tropical wave from the west coast of Africa on October 11, 2012. As it traveled north from the Carribean Sea, it made several landfalls on locations like Jamaica and Cuba, where it weakened to a Category 1 hurricane. As it traveled further north, however, it significantly grew in size as it traveled across the Bahamas. It made landfall on 29th of October 2012 at about 23:30 UTC. At the time of landfall, the intensity and the minimum pressure were measured to be 70 kt and 945 mb, respectively. The hurricane gradually weakened as it made its way through New Jersey, Delaware, and Pennsylvania before it finally merged with a low pressure area over eastern Canada. 

*Source: National Hurricane Center Tropical Cyclone Report* (https://www.nhc.noaa.gov/data/tcr/AL182012_Sandy.pdf)

## Storm Data
The storm data file can be found in the NOAA storm data archive website (http://ftp.nhc.noaa.gov/atcf/archive/2012/bal182012.dat.gz)
The following code from ```setrun.py``` will automatically retrieve the file:
``` python
# Convert ATCF data to GeoClaw format
clawutil.data.get_remote_file("http://ftp.nhc.noaa.gov/atcf/archive/2012/bal182012.dat.gz")
atcf_path = os.path.join(scratch_dir, "bal182012.dat")
```
As it is implemented now, the storm data file will be placed in the scratch directory ```$CLAW/geoclaw/scrach```

## Topography & Bathymetry Data
The two topography data files of interest are ```atlantic_1min.tt3``` and ```newyork_3s.tt3```. The files should be placed in the scratch directory ```$CLAW/geoclaw/scrach```

## Geoclaw Parameters
Landfall time: 29 October 2012 23:30 UTC

Gauges:
  1. Battery, NY (8518750)
  2. Kings Point, NY (8516945)
  3. Montauk, NY (8510560)
  4. Bridgeport, CT (8467150)
  5. New Haven, CT (8465705)
  6. New London, CT (8461490)
  
 *All gauge locations are based on NOAA Tides and Currents Dashboard* (https://tidesandcurrents.noaa.gov/map/index.html)
