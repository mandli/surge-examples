
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""

import os

import numpy as np
import matplotlib.pyplot as plt
import datetime

from clawpack.geoclaw.util import fetch_noaa_tide_data
from clawpack.visclaw import colormaps, gaugetools
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

    # Load data from output
    clawdata = clawpack.clawutil.data.ClawInputData(2)
    clawdata.read(os.path.join(plotdata.outdir,'claw.data'))
    physics = clawpack.geoclaw.data.GeoClawData()
    physics.read(os.path.join(plotdata.outdir,'geoclaw.data'))
    surge_data = clawpack.geoclaw.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir,'surge.data'))
    friction_data = clawpack.geoclaw.data.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir,'friction.data'))

    # Load storm track32
    track = surge.track_data(os.path.join(plotdata.outdir,'fort.track'))

    # Set afteraxes function
    def surge_afteraxes(cd):
        return surge.surge_afteraxes(cd, track, plot_direction=False)

    # Limits for plots
    dx = 0.5
    dy = 0.5
    regions = [{"name": "Full Domain",
                "limits": [[clawdata.lower[0], clawdata.upper[0]],
                           [clawdata.lower[1], clawdata.upper[1]]]},
               {"name": "New Orleans",
                "limits": [[-90.5, -85.5], [27.5, 32]]}]


    # Color limits
    surface_limits = [physics.sea_level - 5.0, physics.sea_level + 5.0]
    surface_ticks = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    surface_labels = [str(value) for value in surface_ticks]
    speed_limits = [0.0, 3.0]
    speed_ticks = [0, 1, 2, 3]
    speed_labels = [str(value) for value in speed_ticks]
    wind_limits = [15, 40]
    pressure_limits = [966,1013]
    friction_bounds = [0.01,0.04]

    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================

    # Loop over region specifications ploting both surface and speeds
    for region in regions:
        name = region['name']
        xlimits = region['limits'][0]
        ylimits = region['limits'][1]
        # ======================================================================
        #  Surface Elevations
        # ======================================================================
        plotfigure = plotdata.new_plotfigure(name='Surface - %s' % name)
        plotfigure.show = True

        # Set up for axes in this figure:
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = 'Surface'
        plotaxes.scaled = True
        plotaxes.xlimits = xlimits
        plotaxes.ylimits = ylimits
        plotaxes.afteraxes = surge_afteraxes

        surge.add_surface_elevation(plotaxes, bounds=surface_limits)
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
        surge.add_land(plotaxes)
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

        # ======================================================================
        #  Water Speed
        # ======================================================================
        plotfigure = plotdata.new_plotfigure(name='Currents - %s' % name)
        plotfigure.show = True

        # Set up for axes in this figure:
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = 'Currents'
        plotaxes.scaled = True
        plotaxes.xlimits = xlimits
        plotaxes.ylimits = ylimits
        plotaxes.afteraxes = surge_afteraxes

        surge.add_speed(plotaxes, bounds=speed_limits)
        plotaxes.plotitem_dict['speed'].amr_patchedges_show = [0] * 10
        surge.add_land(plotaxes)
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10


    # Only plot hurricane forcing in the full domain
    region = regions[0]
    name = region['name']
    xlimits = region['limits'][0]
    ylimits = region['limits'][1]
    # ======================================================================
    #  Wind Field
    # ======================================================================
    plotfigure = plotdata.new_plotfigure(name='Wind Speed - %s' % name)
    plotfigure.show = surge_data.wind_forcing

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Wind Field"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = surge_afteraxes

    surge.add_wind(plotaxes, bounds=wind_limits)
    plotaxes.plotitem_dict['wind'].amr_patchedges_show = [0] * 10
    surge.add_land(plotaxes)
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10


    # ========================================================================
    # Hurricane forcing
    # ========================================================================

    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure - %s' % name)
    plotfigure.show = surge_data.pressure_forcing

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Pressure Field"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = surge_afteraxes

    surge.add_pressure(plotaxes, bounds=pressure_limits)
    plotaxes.plotitem_dict['pressure'].amr_patchedges_show = [0] * 10
    surge.add_land(plotaxes)
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10


    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface & Topo', figno=300, \
                    type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    stations = [('8728690', 'Apalachicola, FL'),
                ('8729210', 'Panama City, FL'),
                ('8729840', 'Pensacola'),
                ('8735180', 'Dauphin Island, AL')]


    landfall_time = np.datetime64('2005-07-10T11:00')
    begin_date = datetime.datetime(2005, 7, 8)
    end_date = datetime.datetime(2005, 7, 12)

    def get_actual_water_levels(station_id):
        # Fetch water levels and tide predictions for given station
        date_time, water_level, tide = fetch_noaa_tide_data(station_id,
                begin_date, end_date)

        # Calculate times relative to landfall
        secs_rel_landfall = (date_time - landfall_time) / np.timedelta64(1, 's')

        # Subtract tide predictions from measured water levels
        water_level -= tide

        return secs_rel_landfall, water_level

    def gauge_afteraxes(cd):

        station_id, station_name = stations[cd.gaugeno - 1]
        secs_rel_landfall, actual_level = get_actual_water_levels(station_id)

        axes = plt.gca()
        axes.plot(secs_rel_landfall, actual_level, 'g')

        # Fix up plot - in particular fix time labels
        axes.set_title(station_name)
        axes.set_xlabel('Days relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_xlim(np.array([-2, 1]) * 86400)
        axes.set_ylim([-0.5, 2.5])
        axes.set_xticks(np.linspace(-2, 1, 4) * 86400)
        axes.set_xticklabels([r"$-2$", r"$-1$", r"$0$", r"$1$"])
        axes.grid(True)

        # Plot wind speed using second scale
        # wind_speed = np.linalg.norm(cd.gaugesoln.q[7:10, :], axis=0)
        # axes2 = axes.twinx()
        # axes2.plot(cd.gaugesoln.t, wind_speed, 'r.', markersize=0.3)
        # axes2.set_ylabel('Wind Speed (m/s)')
        # axes2.set_ylim([-2.5, 52.5])

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    #
    #  Gauge Location Plot
    #
    def gauge_location_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos='all',
                                        format_string='ko', add_labels=True)

    plotfigure = plotdata.new_plotfigure(name="Gauge Locations")
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Gauge Locations'
    plotaxes.scaled = True
    plotaxes.xlimits = [-90, -84]
    plotaxes.ylimits = [27.0, 32.0]
    plotaxes.afteraxes = gauge_location_afteraxes

    surge.add_surface_elevation(plotaxes, bounds=surface_limits)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    surge.add_land(plotaxes)
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10


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
