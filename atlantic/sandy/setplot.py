
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""
import os

# import numpy as np
# import matplotlib

import matplotlib.pyplot as plt
import datetime

from clawpack.visclaw import colormaps
import clawpack.clawutil.data
import clawpack.amrclaw.data
import clawpack.geoclaw.data

import clawpack.geoclaw.surge.plot as surge

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

def setplot(plotdata):
    r"""Setplot function for surge plotting"""
    

    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'binary'

    # Load data from output
    clawdata = clawpack.clawutil.data.ClawInputData(2)
    clawdata.read('claw.data')
    physics = clawpack.geoclaw.data.GeoClawData()
    physics.read(os.path.join(plotdata.outdir,'geoclaw.data'))
    surge_data = clawpack.geoclaw.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir,'surge.data'))
    friction_data = clawpack.geoclaw.data.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir,'friction.data'))

    # Load storm track
    track = surge.track_data(os.path.join(plotdata.outdir,'fort.track'))

    # Calculate landfall time, off by a day, maybe leap year issue?
    landfall_dt = datetime.datetime(2012,10,30,8,0) - datetime.datetime(2012,1,1,0)
    landfall = (landfall_dt.days) * 24.0 * 60**2 + landfall_dt.seconds

    # Set afteraxes function
    surge_afteraxes = lambda cd: surge.surge_afteraxes(cd, 
                                        track, landfall, plot_direction=False)


    # Color limits
    surface_range = 1.5
    speed_range = 1.0
    # speed_range = 1.e-2

    eta = physics.sea_level
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    speed_limits = [0.0,speed_range]
    
    wind_limits = [0,55]
    pressure_limits = [966,1013]
    friction_bounds = [0.01,0.04]
    vorticity_limits = [-1.e-2,1.e-2]
    land_bounds = [-10, 50]

    def pcolor_afteraxes(current_data):
        surge_afteraxes(current_data)
        # surge.gauge_locations(current_data)
    
    def contour_afteraxes(current_data):
        surge_afteraxes(current_data)

    
    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================
    # Limits for plots
    regions = {'full': ([[clawdata.lower[0],clawdata.upper[0]],
                         [clawdata.lower[1],clawdata.upper[1]]],
                         0.8, [1] * 10),
               'Region': ([[-74.5,-71.0], [40.0,41.5]], 
                          0.5, [0] * 10),
                   'NYC':([[-74.2,-73.8], [40.55,40.85]], 0.5, [0] * 10)
                  }
    
    for (name, region_data) in regions.items():
        # ========================================================================
        #  Surface Elevations
        # ========================================================================
        plotfigure = plotdata.new_plotfigure(name='Surface - %s' % name)
        plotfigure.show = True

        # Set up for axes in this figure:
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = 'Surface'
        plotaxes.scaled = True
        plotaxes.xlimits = region_data[0][0]
        plotaxes.ylimits = region_data[0][1]
        plotaxes.afteraxes = pcolor_afteraxes
    
        surge.add_surface_elevation(plotaxes, bounds=surface_limits, shrink=region_data[1])
        surge.add_land(plotaxes, bounds=land_bounds)
        plotaxes.plotitem_dict['land'].amr_patchedges_show = region_data[2]
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = region_data[2]


        # ========================================================================
        #  Water Speed
        # ========================================================================
        plotfigure = plotdata.new_plotfigure(name='Currents - %s' % name)
        plotfigure.show = True

        # Set up for axes in this figure:
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = 'Currents'
        plotaxes.scaled = True
        plotaxes.xlimits = region_data[0][0]
        plotaxes.ylimits = region_data[0][1]
        plotaxes.afteraxes = pcolor_afteraxes

        # Speed
        surge.add_speed(plotaxes,bounds=speed_limits,shrink=region_data[1])

        # Land
        surge.add_land(plotaxes, bounds=land_bounds)
        plotaxes.plotitem_dict['land'].amr_patchedges_show = region_data[2]
        plotaxes.plotitem_dict['speed'].amr_patchedges_show = region_data[2]


    # ========================================================================
    # Hurricane forcing - Entire Atlantic
    # ========================================================================
    # Friction field
    plotfigure = plotdata.new_plotfigure(name='Friction')
    plotfigure.show = friction_data.variable_friction and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['full'][0][0]
    plotaxes.ylimits = regions['full'][0][1]
    plotaxes.title = "Manning's N Coefficients"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    surge.add_friction(plotaxes,bounds=friction_bounds)

    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure')
    plotfigure.show = surge_data.pressure_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['full'][0][0]
    plotaxes.ylimits = regions['full'][0][1]
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.add_pressure(plotaxes,bounds=pressure_limits)
    # add_pressure(plotaxes)
    surge.add_land(plotaxes, bounds=[-10, 500])
    
    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = surge_data.wind_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()

    plotaxes.xlimits = regions['full'][0][0]
    plotaxes.ylimits = regions['full'][0][1]
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.add_wind(plotaxes,bounds=wind_limits,plot_type='imshow')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='contour')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='quiver')
    surge.add_land(plotaxes, bounds=[-10, 500])

    # ==========================================================================
    #  Depth
    # ==========================================================================
    plotfigure = plotdata.new_plotfigure(name='Depth - Entire Domain')
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Topography'
    plotaxes.scaled = True
    plotaxes.xlimits = regions['full'][0][0]
    plotaxes.ylimits = regions['full'][0][1]
    plotaxes.afteraxes = surge_afteraxes

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = 0
    plotitem.imshow_cmin = 0
    plotitem.imshow_cmax = 200
    plotitem.imshow_cmap = plt.get_cmap("terrain")
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,1,1,1,1]

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='Surface, Speeds',   
    #                                      figno=fig_counter + 7,
    #                                      type='each_gauge')
    # plotfigure.show = True
    # plotfigure.clf_each_gauge = True

    # # Surface and Topography
    # plotaxes = plotfigure.new_plotaxes()
    # # plotaxes.axescmd = 'subplot(121)'
    # try:
    #     plotaxes.xlimits = [amrdata.t0,amrdata.tfinal]
    # except:
    #     pass
    # plotaxes.ylimits = surface_limits
    # plotaxes.title = 'Surface'
    # plotaxes.afteraxes = surge.gauge_afteraxes
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 3
    # plotitem.plotstyle = 'b-'

    # # Speeds
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.axescmd = 'subplot(122)'
    # try:
    #     plotaxes.xlimits = [amrdata.t0,amrdata.tfinal]
    # except:
    #     pass
    # plotaxes.ylimits = surface_limits
    # plotaxes.title = 'Momenta'
    # plotaxes.afteraxes = surge.gauge_afteraxes

    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 1
    # plotitem.plotstyle = 'r-'
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 2
    # plotitem.plotstyle = 'b-'




    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

