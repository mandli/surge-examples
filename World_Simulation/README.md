# World Simulation


Purpose: see if GeoClaw could handle a storm with the topography of world.


Topography was selected from NOAA Grid Extract. 12 topography files were extracted with latitude from -180 to 180 and longitude from -60 to 60. Files were adjusted to have latitude from 0 to 360. 


Code for Adjusting Topography Files.


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

Ran multiple storms using the topography of the entire world.


Storms we ran so far were near Australia and New Zealand.


Created a script that automatically placed gauges near the storm. 
