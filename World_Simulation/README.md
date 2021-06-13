# World Simulation


Purpose: see if GeoClaw could handle a storm with the topography of world.


Topography was selected from NOAA Grid Extract. Coastal Relief Model was selected as dataset.


https://maps.ngdc.noaa.gov/viewers/grid-extract/index.html

12 topography files were extracted with latitude from -180 to 180 and longitude from -60 to 60. Each topography file had interval of 30 for latitude and maintained the same longitude of -60 to 60. (Ex. First topography file had latitude of -180 to -150 and longitude of -60 to 60; Second has latitude of -150 to -120 and longitude of -60 to 60). Files were downloaded and uploaded to current working directory. 


Files were adjusted to have latitude from 0 to 360. Code for Adjusting Topography Files.


    import os
    import matplotlib as plt
    import clawpack.geoclaw.topotools as topo
    from clawpack.geoclaw import topotools


    topofiles = []
    for n in range(7,13):
        topo=topotools.Topography()
        topo.read('./world_' + str(n) + '.tt3' , topo_type=3)
        topofiles.append(topo)

        for k, x in enumerate(topo.x):
            x+=180;
            topo.x[k]=x
        print(topo.x)
        topo.plot()

Sotrm file was uploaded in directory named 'Storm'. Ran multiple storms using the topography of the entire world.


Storms we ran so far were near Australia and New Zealand.


Created a script that automatically placed gauges near the storm. 
