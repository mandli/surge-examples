from __future__ import absolute_import
from __future__ import print_function

import os

import numpy
import matplotlib.pyplot as plt
import datetime

import clawpack.visclaw.colormaps as colormap
import clawpack.visclaw.gaugetools as gaugetools
import clawpack.clawutil.data as clawutil
import clawpack.amrclaw.data as amrclaw
import clawpack.geoclaw.data as geodata

import clawpack.geoclaw.surge.plot as surgeplot

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

def setplot(plotdata):
    r"""Setplot function for surge plotting"""
    

    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'binary'

    # Load data from output
    clawdata = clawutil.ClawInputData(2)
    clawdata.read(os.path.join(plotdata.outdir, 'claw.data'))
    physics = geodata.GeoClawData()
    physics.read(os.path.join(plotdata.outdir, 'geoclaw.data'))
    surge_data = geodata.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir, 'surge.data'))
    friction_data = geodata.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir, 'friction.data'))

    # Load storm track
    track = surgeplot.track_data(os.path.join(plotdata.outdir,'fort.track'))

    # Set afteraxes function
    surge_afteraxes = lambda cd: surgeplot.surge_afteraxes(cd, track, 
                                                           plot_direction=False)

    # Color limits
    surface_range = 1.5
    speed_range = 1.0
    # speed_range = 1.e-2

    eta = physics.sea_level
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    speed_limits = [0.0,speed_range]
    
    wind_limits = [0, 55]
    pressure_limits = [966, 1013]
    friction_bounds = [0.01, 0.04]
    vorticity_limits = [-1.e-2, 1.e-2]
    land_bounds = [-10, 50]
    
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # Limits for plots
    regions = {'Full Domain': {"xlimits": [clawdata.lower[0], clawdata.upper[0]],
                               "ylimits": [clawdata.lower[1], clawdata.upper[1]],
                               "shrink": 1.0, 
                               "figsize": [6.4, 4.8]},
               'Tri-State Region': {"xlimits": [-74.5,-71.0], 
                                    "ylimits": [40.0,41.5], 
                                    "shrink": 1.0,
                                    "figsize": [6.4, 4.8]},
                'NYC': {"xlimits": [-74.2,-73.8], 
                        "ylimits": [40.55,40.85], 
                        "shrink": 1.0, 
                        "figsize": [6.4, 4.8]}
               }
    
    for (name, region_dict) in regions.items():
        # ========================================================================
        #  Surface Elevations
        # ========================================================================
        plotfigure = plotdata.new_plotfigure(name='Surface - %s' % name)
        plotfigure.show = True

        # Set up for axes in this figure:
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = 'Surface'
        plotaxes.scaled = True
        plotaxes.xlimits = region_dict['xlimits']
        plotaxes.ylimits = region_dict['ylimits']
        plotaxes.afteraxes = surge_afteraxes
    
        surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits, 
                                    shrink=region_dict['shrink'])
        surgeplot.add_land(plotaxes, bounds=land_bounds)
        
        # plotaxes.plotitem_dict['land'].amr_patchedges_show = 
        # plotaxes.plotitem_dict['surface'].amr_patchedges_show = 


        # ========================================================================
        #  Water Speed
        # ========================================================================
        plotfigure = plotdata.new_plotfigure(name='Currents - %s' % name)
        plotfigure.show = True

        # Set up for axes in this figure:
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = 'Currents'
        plotaxes.scaled = True
        plotaxes.xlimits = region_dict['xlimits']
        plotaxes.ylimits = region_dict['ylimits']
        plotaxes.afteraxes = surge_afteraxes

        surgeplot.add_speed(plotaxes, bounds=speed_limits, 
                        shrink=region_dict['shrink'])
        surgeplot.add_land(plotaxes, bounds=land_bounds)


    # ========================================================================
    # Hurricane forcing - Entire Atlantic
    # ========================================================================
    # Friction field
    plotfigure = plotdata.new_plotfigure(name='Friction')
    plotfigure.show = False

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Manning's N Coefficients"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    surgeplot.add_friction(plotaxes,bounds=friction_bounds)

    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure')
    plotfigure.show = True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surgeplot.add_pressure(plotaxes,bounds=pressure_limits)
    surgeplot.add_land(plotaxes, bounds=[-10, 500])
    
    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = True
    
    plotaxes = plotfigure.new_plotaxes()

    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surgeplot.add_wind(plotaxes,bounds=wind_limits,plot_type='imshow')
    surgeplot.add_land(plotaxes, bounds=[-10, 500])

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface, Speeds',
                                         type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    # Surface and Topography
    plotaxes = plotfigure.new_plotaxes()
    # plotaxes.axescmd = 'subplot(121)'
    try:
        plotaxes.xlimits = [amrdata.t0, amrdata.tfinal]
    except:
        pass
    plotaxes.ylimits = surface_limits
    plotaxes.title = 'Surface'
    # plotaxes.afteraxes = surgeplot.gauge_afteraxes
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    # Speeds
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(122)'
    try:
        plotaxes.xlimits = [amrdata.t0, amrdata.tfinal]
    except:
        pass
    plotaxes.ylimits = surface_limits
    plotaxes.title = 'Momenta'
    # plotaxes.afteraxes = surge.gauge_afteraxes

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 1
    plotitem.plotstyle = 'r-'
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 2
    plotitem.plotstyle = 'b-'

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

