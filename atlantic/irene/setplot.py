
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""
import os

import numpy as np
import matplotlib

import matplotlib.pyplot as plt
import datetime

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
    plotdata.format = 'ascii'

    #fig_num_counter = surge.figure_counter()

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
    landfall_dt = datetime.datetime(2011,8,27,7,30) - datetime.datetime(2011,1,1,0)
    landfall = (landfall_dt.days) * 24.0 * 60**2 + landfall_dt.seconds

    # Set afteraxes function
    surge_afteraxes = lambda cd: surge.surge_afteraxes(cd, 
                                        track, landfall, plot_direction=False)
    # Limits for plots
    full_xlimits = [clawdata.lower[0],clawdata.upper[0]]
    full_ylimits = [clawdata.lower[1],clawdata.upper[1]]
    full_shrink = 0.8
    newyork_xlimits = [-74.2,-73.7]
    newyork_ylimits = [40.4,40.85]
    newyork_shrink = 1.0

    # Color limits
    surface_range = 1.5
    speed_range = 1.0
    # speed_range = 1.e-2

    xlimits = full_xlimits
    ylimits = full_ylimits
    eta = physics.sea_level
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    speed_limits = [0.0,speed_range]
    
    wind_limits = [0,55]
    pressure_limits = [966,1013]
    friction_bounds = [0.01,0.04]
    vorticity_limits = [-1.e-2,1.e-2]

    def pcolor_afteraxes(current_data):
        surge_afteraxes(current_data)
        surge.gauge_locations(current_data)
    
    def contour_afteraxes(current_data):
        surge_afteraxes(current_data)

    
    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================

    # ========================================================================
    #  Surface Elevations - Entire Atlantic
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface - Atlantic',  
                                         figno=100)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes
    
    surge.add_surface_elevation(plotaxes,bounds=surface_limits,shrink=full_shrink)
    surge.add_land(plotaxes)


    # ========================================================================
    #  Water Speed - Entire Atlantic
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Currents - Atlantic',  
                                         figno=200)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes

    # Speed
    surge.add_speed(plotaxes,bounds=speed_limits,shrink=full_shrink)

    # Land
    surge.add_land(plotaxes)

    # ========================================================================
    #  Surface Elevations - New York Area
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface - New York',  
                                         figno=300)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = newyork_xlimits
    plotaxes.ylimits = newyork_ylimits
    def after_with_gauges(cd):
        surge_afteraxes(cd)
        surge.gauge_locations(cd)
    plotaxes.afteraxes = after_with_gauges
    
    surge.add_surface_elevation(plotaxes,bounds=surface_limits,shrink=newyork_shrink)
    surge.add_land(plotaxes)

    # ========================================================================
    #  Currents Elevations - New York Area
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Currents - New York',  
                                         figno=400)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = newyork_xlimits
    plotaxes.ylimits = newyork_ylimits
    def after_with_gauges(cd):
        surge_afteraxes(cd)
        surge.gauge_locations(cd)
    plotaxes.afteraxes = after_with_gauges
    
    surge.add_speed(plotaxes,bounds=speed_limits,shrink=newyork_shrink)
    surge.add_land(plotaxes)


    # ========================================================================
    # Hurricane forcing - Entire Atlantic
    # ========================================================================
    # Friction field
    plotfigure = plotdata.new_plotfigure(name='Friction',
                                         figno=500)
    plotfigure.show = friction_data.variable_friction and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Manning's N Coefficients"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    surge.add_friction(plotaxes,bounds=friction_bounds)

    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure',  
                                         figno=600)
    plotfigure.show = surge_data.pressure_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.add_pressure(plotaxes,bounds=pressure_limits)
    # add_pressure(plotaxes)
    surge.add_land(plotaxes)
    
    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed', 
                                         figno=700)
    plotfigure.show = surge_data.wind_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.add_wind(plotaxes,bounds=wind_limits,plot_type='imshow')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='contour')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='quiver')
    surge.add_land(plotaxes)
    
    # Surge field
    plotfigure = plotdata.new_plotfigure(name='Surge Field', 
                                         figno=800)
    plotfigure.show = ((surge_data.wind_forcing or surge_data.pressure_forcing) 
                        and False)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Storm Surge Source Term S"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.pressure_field + 1
    plotitem.pcolor_cmap = plt.get_cmap('PuBu')
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1e-3
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.colorbar_label = "Source Strength"
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,0,0]
    
    surge.add_land(plotaxes)

    plotfigure = plotdata.new_plotfigure(name='Friction/Coriolis Source', 
                                         figno=900)
    plotfigure.show = False
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Friction/Coriolis Source"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.pressure_field + 2
    plotitem.pcolor_cmap = plt.get_cmap('PuBu')
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1e-3
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.colorbar_label = "Source Strength"
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,0,0]
    
    surge.add_land(plotaxes)

    # ==========================================================================
    #  Depth
    # ==========================================================================
    plotfigure = plotdata.new_plotfigure(name='Depth - Entire Domain', 
                                         figno=1000)
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Topography'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
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
    plotfigure = plotdata.new_plotfigure(name='Surface',   
                                         figno=250,type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True
 
    stations = [('8518750', 'The Battery, NY'),
                ('8516945', 'Kings Point, NY'),
                ('8519483', 'Bergen Point West Reach, NY')]
                #('8531680','Sandy Hook, NY'),
                #('n03020','Narrows,NY')]
  
    landfall_time = np.datetime64('2011-08-27T11:30')
    begin_date = datetime.datetime(2011, 8, 24 )
    end_date = datetime.datetime(2011, 8, 28)

#    def get_actual_water_levels(station_id):
#        # Fetch water levels and tide predictions for given station
#        date_time, water_level, tide = fetch_noaa_tide_data(station_id,
#                begin_date, end_date)

        # Calculate times relative to landfall
#        seconds_rel_landfall = (date_time - landfall_time) / np.timedelta64(1, 's')
        # Subtract tide predictions from measured water levels
#        water_level -= tide

 #       return seconds_rel_landfall, water_level

 
    def gauge_afteraxes(cd):
        station_id, station_name = stations[cd.gaugeno-1]
#        seconds_rel_landfall, actual_level = get_actual_water_levels(station_id)

        axes = plt.gca()
        #surgeplot.plot_landfall_gauge(cd.gaugesoln, axes, landfall=landfall)
 #       axes.plot(seconds_rel_landfall, actual_level, 'g')

        # Fix up plot - in particular fix time labels
        axes.set_title(station_name)
        axes.set_xlabel('Seconds relative to landfall')
        axes.set_ylabel('Surface (m)')
 #       axes.set_xlim([days2seconds(-2), days2seconds(1)])
        axes.set_ylim([0, 4])
#        axes.set_xticks([ days2seconds(-2), days2seconds(-1), 0, days2seconds(1)])
        #axes.set_xticklabels([r"$-3$", r"$-2$", r"$-1$", r"$0$", r"$1$"])
        #axes.grid(True)
 

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    try:
        plotaxes.xlimits = [amrdata.t0,amrdata.tfinal]
    except:
        pass
    plotaxes.ylimits = surface_limits
    plotaxes.title = 'Surface'
    plotaxes.afteraxes = gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

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

