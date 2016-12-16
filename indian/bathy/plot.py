#!/usr/bin/env python

import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import clawpack.geoclaw.topotools as topotools
import clawpack.visclaw.colormaps as colormaps

# Read topography
indian_ocean_topo = topotools.Topography("indian_ocean.nc", topo_type=4)
indian_ocean_topo.read(nc_params={"x_var":"lon", "y_var":"lat", "z_var":"Band1"})
# indian_ocean_topo.Z = numpy.ma.MaskedArray(indian_ocean_topo.Z)

mumbai_topo = topotools.Topography("mumbai.tt3")
# mumbai_topo.Z = numpy.ma.MaskedArray(mumbai_topo.Z)

# region_extent = indian_ocean_topo.extent
# depth_extent = (numpy.min(indian_ocean_topo.Z), numpy.max(indian_ocean_topo.Z))
# depth_extent = (-1000, 200)

# Plot topography
fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)

# indian_ocean_topo.plot(axes=axes)
topo_extent = (numpy.min(indian_ocean_topo.Z), numpy.max(indian_ocean_topo.Z))

# axes.pcolor(indian_ocean_topo.X, indian_ocean_topo.Y, indian_ocean_topo.Z)
indian_ocean_topo.plot(axes=axes)
mumbai_topo.plot(axes=axes, add_colorbar=False)

# mumbai_topo.plot(axes=axes, limits=topo_extent, plot_box=True)

# land_cmap = colormaps.make_colormap({ 0.0:[0.1,0.4,0.0],
#                                      0.25:[0.0,1.0,0.0],
#                                       0.5:[0.8,1.0,0.5],
#                                       1.0:[0.8,0.5,0.2]})
# sea_cmap = plt.get_cmap('Blues_r')
# if region_extent[0] >= 0.0:
#     cmap = land_cmap
#     norm = colors.Normalize(vmin=0.0, vmax=region_extent[1])
# elif region_extent[1] <= 0.0:
#     cmap = sea_cmap
#     norm = colors.Normalize(vmin=region_extent[0], vmax=0.0)
# else:
#     cmap, norm = colormaps.add_colormaps((land_cmap, sea_cmap),
#                                          data_limits=region_extent,
#                                          data_break=0.0)

# axes.imshow(indian_ocean_topo.Z, vmin=depth_extent[0], vmax=depth_extent[1],
#                          extent=region_extent, cmap=cmap, origin='lower',
#                                        interpolation='nearest')
# axes.imshow(mumbai_topo.Z, vmin=depth_extent[0], vmax=depth_extent[1],
#                          extent=region_extent)
# axes.set_xlim(region_extent[0:2])
# axes.set_ylim(region_extent[2:])

plt.show()