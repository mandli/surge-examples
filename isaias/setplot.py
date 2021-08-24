
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
from clawpack.geoclaw.util import fetch_noaa_tide_data


import clawpack.geoclaw.surge.plot as surgeplot

try:
    from setplotfg import setplotfg
except:
    setplotfg = None


def setplot(plotdata=None):
    """"""

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    # clear any old figures,axes,items data
    plotdata.clearfigures()
    plotdata.format = 'ascii'

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
    track = surgeplot.track_data(os.path.join(plotdata.outdir, 'fort.track'))

    # Set afteraxes function
    def surge_afteraxes(cd):
        surgeplot.surge_afteraxes(cd, track, plot_direction=False,
                                             kwargs={"markersize": 4})

#HAS EXCESS CODE HERE THAT IKE NOR OPHELIA HAVE.
    # Color limits
    surface_limits = [physics.sea_level - 5.0, physics.sea_level + 5.0]
    surface_ticks = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    surface_labels = [str(value) for value in surface_ticks]
    speed_limits = [0.0, 3.0]
    speed_ticks = [0, 1, 2, 3]
    speed_labels = [str(value) for value in speed_ticks]
    wind_limits = [0, 64]
    pressure_limits = [935, 1013]
    friction_bounds = [0.01, 0.04]

    def add_custom_colorbar_ticks_to_axes(axes, item_name, ticks,
                                          tick_labels=None):
        """Adjust colorbar ticks and labels"""
        axes.plotitem_dict[item_name].colorbar_ticks = ticks
        axes.plotitem_dict[item_name].colorbar_tick_labels = tick_labels

    def gulf_after_axes(cd):
        # plt.subplots_adjust(left=0.08, bottom=0.04, right=0.97, top=0.96)
        surge_afteraxes(cd)

    def latex_after_axes(cd):
        # plt.subplot_adjust()
        surge_afteraxes(cd)
#EXCESS CODE ENDS HERE, BACK TO ORIGINAL PROGRAMMING!
    def friction_after_axes(cd):
        # plt.subplots_adjust(left=0.08, bottom=0.04, right=0.97, top=0.96)
        plt.title(r"Manning's $n$ Coefficient")
        # surge_afteraxes(cd)

    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    regions = {"Atlantic": {"xlimits": (clawdata.lower[0], clawdata.upper[0]),
                        "ylimits": (clawdata.lower[1], clawdata.upper[1]),
                        "figsize": (6.4, 4.8)},
                "Savannah": {"xlimits": (-82, -76),
                               "ylimits": (29.5, 34.5),
                               "figsize": (8, 2.7)}}
    #changing this up! selected the DR, should select savannah prolly.
    for (name, region_dict) in regions.items():

        # Surface Figure
        plotfigure = plotdata.new_plotfigure(name="Surface - %s" % name)
        plotfigure.kwargs = {"figsize": region_dict['figsize']}
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = "Surface"
        plotaxes.xlimits = region_dict["xlimits"]
        plotaxes.ylimits = region_dict["ylimits"]
        plotaxes.afteraxes = surge_afteraxes
        plotaxes.scaled = True #OPTIONAL - CAN KEEP AS A SQUARE.

        surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
        surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10
        add_custom_colorbar_ticks_to_axes(plotaxes, 'surface', surface_ticks,
                                          surface_labels)

        # Speed Figure
        plotfigure = plotdata.new_plotfigure(name="Currents - %s" % name)
        plotfigure.kwargs = {"figsize": region_dict['figsize']}
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = "Currents"
        plotaxes.xlimits = region_dict["xlimits"]
        plotaxes.ylimits = region_dict["ylimits"]
        plotaxes.afteraxes = surge_afteraxes
        plotaxes.scaled = True #OPTIONAL - CAN KEEP AS A SQUARE.

        surgeplot.add_speed(plotaxes, bounds=speed_limits)
        surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
        plotaxes.plotitem_dict['speed'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10
        add_custom_colorbar_ticks_to_axes(plotaxes, 'speed', speed_ticks,
                                          speed_labels)

    #
    # Friction field
    #
    plotfigure = plotdata.new_plotfigure(name='Friction')
    plotfigure.show = friction_data.variable_friction and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Atlantic']['xlimits']
    plotaxes.ylimits = regions['Atlantic']['ylimits']
    # plotaxes.title = "Manning's N Coefficient"
    plotaxes.afteraxes = friction_after_axes
    plotaxes.scaled = True

    surgeplot.add_friction(plotaxes, bounds=friction_bounds, shrink=0.9)
    plotaxes.plotitem_dict['friction'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['friction'].colorbar_label = "$n$"

    #
    #  Hurricane Forcing fields
    #
    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure')
    plotfigure.show = surge_data.pressure_forcing and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Atlantic']['xlimits']
    plotaxes.ylimits = regions['Atlantic']['ylimits']
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_pressure(plotaxes, bounds=pressure_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = surge_data.wind_forcing and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Atlantic']['xlimits']
    plotaxes.ylimits = regions['Atlantic']['ylimits']
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_wind(plotaxes, bounds=wind_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Gauge Surfaces', figno=300,
                                         type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True


    plotaxes = plotfigure.new_plotaxes()
    #Time Conversions
    def days2seconds(days):
      return days * 60.0**2 * 24.0

    #Getting the data for each gauge from NOAA's API
    stations = [('9759110', 'Magueyes Island, PR'),
                ('8722670', 'Lake Worth Pier, FL'),
                ('8670870', 'Fort Pulaski, GA'),
                ('8661070', 'Springmaid Pier, SC'),
                ('8658120', 'Wilmington, NC'),
                ('8540433', 'Marcus Hook, PA')]

    landfall_time = numpy.datetime64('2020-07-31T00:00')
    begin_date = datetime.datetime(2020, 7, 30)
    end_date = datetime.datetime(2020, 8, 5)

    def get_actual_water_levels(station_id):
        # Fetch water levels and tide predictions for given station
        date_time, water_level, tide = fetch_noaa_tide_data(station_id,
                begin_date, end_date)

        # Calculate times relative to landfall
        seconds_rel_landfall = (date_time - landfall_time) / numpy.timedelta64(1, 's')
        # Subtract tide predictions from measured water levels
        water_level -= tide

        return seconds_rel_landfall, water_level

    def gauge_afteraxes(cd):
        station_id, station_name = stations[cd.gaugeno-1]
        seconds_rel_landfall, actual_level = get_actual_water_levels(station_id)

        axes = plt.gca()
        surgeplot.plot_landfall_gauge(cd.gaugesoln, axes)
        axes.plot(seconds_rel_landfall, actual_level, 'g')

        # Fix up plot - in particular fix time labels
        axes.set_title(station_name)
        axes.set_xlabel('Days relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_xlim([days2seconds(-1), days2seconds(5)])
        #axes.set_xlim([-1, 5])
        axes.set_ylim([-1, 2])
        axes.set_xticks([days2seconds(-1), days2seconds(0), days2seconds(1),
                        days2seconds(2), days2seconds(3), days2seconds(4), days2seconds(5)])
        #axes.set_xticks([-1, 0, 1, 2, 3, 4, 5])
        axes.set_xticklabels([r"$-1$", r"$0$", r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"])
        axes.grid(True)


    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    #plotaxes.xlimits = [-1, 5]
    # plotaxes.xlabel = "Days from landfall"
    # plotaxes.ylabel = "Surface (m)"
    #plotaxes.ylimits = [-1, 2]
    #plotaxes.title = 'Surface'
    plotaxes.afteraxes = gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    #Gauge Locations
    def gauge_1_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[1], format_string='ko', add_labels=True)

    def gauge_2_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[2], format_string='ko', add_labels=True)

    def gauge_3_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[3], format_string='ko', add_labels=True)

    def gauge_4_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[4], format_string='ko', add_labels=True)

    def gauge_5_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[5], format_string='ko', add_labels=True)

    def gauge_6_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[6], format_string='ko', add_labels=True)

    plotfigure = plotdata.new_plotfigure(name="1. Magueyes Island, PR")
    plotfigure.show = True
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = '1. Magueyes Island, PR'
    plotaxes.scaled = True
    #0.5x0.5
    plotaxes.xlimits = [-67.25, -66.75]
    plotaxes.ylimits = [17.75, 18.25]
    plotaxes.afteraxes = gauge_1_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    plotfigure = plotdata.new_plotfigure(name="2. Lake Worth Pier, FL")
    plotfigure.show = True
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = '2. Lake Worth Pier, FL'
    plotaxes.scaled = True
    #0.5x0.5
    plotaxes.xlimits = [-80.25, -79.75]
    plotaxes.ylimits = [26.35, 26.85]
    plotaxes.afteraxes = gauge_2_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    plotfigure = plotdata.new_plotfigure(name="3. Fort Pulaski, GA")
    plotfigure.show = True
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = '3. Fort Pulaski, GA'
    plotaxes.scaled = True
    #0.6x0.6
    plotaxes.xlimits = [-81.2, -80.6]
    plotaxes.ylimits = [31.7, 32.3]
    plotaxes.afteraxes = gauge_3_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    plotfigure = plotdata.new_plotfigure(name="4. Springmaid Pier, SC")
    plotfigure.show = True
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = '4. Springmaid Pier, SC'
    plotaxes.scaled = True
    #0.5x0.5
    plotaxes.xlimits = [-79.15, -78.65]
    plotaxes.ylimits = [33.4, 33.9]
    plotaxes.afteraxes = gauge_4_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    plotfigure = plotdata.new_plotfigure(name="5. Wilmington, NC")
    plotfigure.show = True
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = '5. Wilmington, NC'
    plotaxes.scaled = True
    #0.5x0.5
    plotaxes.xlimits = [-78.2, -77.7]
    plotaxes.ylimits = [33.95, 34.45]
    plotaxes.afteraxes = gauge_5_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    plotfigure = plotdata.new_plotfigure(name="6. Marcus Hook, PA")
    plotfigure.show = True
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = '6. Marcus Hook, PA'
    plotaxes.scaled = True
    plotaxes.xlimits = [-75.65, -75.15]
    plotaxes.ylimits = [39.55, 40.05]
    plotaxes.afteraxes = gauge_6_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # -----------------------------------------
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = [1, 2, 3, 4, 5, 6]   # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # parallel plotting

    return plotdata
