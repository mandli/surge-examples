from __future__ import absolute_import
from __future__ import print_function

import os

import numpy as np
import matplotlib.pyplot as plt
import datetime
from collections import deque

import clawpack.visclaw.gaugetools as gaugetools
import clawpack.visclaw.frametools as frametools
import clawpack.clawutil.data as clawutil
import clawpack.geoclaw.data as geodata
import clawpack.geoclaw.util as geoutil

import clawpack.geoclaw.surge.plot as surgeplot

try:
    from setplotfg import setplotfg
except ModuleNotFoundError:
    setplotfg = None


# Time Conversions
def days2seconds(days):
    return days * 60.0 ** 2 * 24.0


# Scratch directory for caching observed water levels at gauges
scratch_dir = os.path.join(os.getcwd(), 'scratch')


def setplot(plotdata=None):
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

    # Color limits
    surface_limits = [-5.0, 5.0]
    speed_limits = [0.0, 3.0]
    wind_limits = [0, 64]
    pressure_limits = [935, 1013]
    friction_bounds = [0.01, 0.04]
    color_limits = [0, 50]

    # Set afteraxes function
    def surge_afteraxes(current_data):
        surgeplot.surge_afteraxes(current_data, track, plot_direction=False,
                                  kwargs={"markersize": 4})

    # Standard set-up settings for plots
    def standard_setup(title, xlimits, ylimits, axes_type):
        plotaxes.title = title
        plotaxes.xlimits = xlimits
        plotaxes.ylimits = ylimits
        plotaxes.afteraxes = axes_type
        plotaxes.scaled = True

    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    regions = {"Full Domain": {"xlimits": (clawdata.lower[0],
                                           clawdata.upper[0]),
                               "ylimits": (clawdata.lower[1],
                                           clawdata.upper[1])},
               "Carolinas": {"xlimits": (-80.5, -77.0),
                             "ylimits": (31.5, 35)}}

    for (name, region_dict) in regions.items():
        # Surface Figure
        plotfigure = plotdata.new_plotfigure(name="Surface - %s" % name)
        plotaxes = plotfigure.new_plotaxes()
        standard_setup("Surface", region_dict["xlimits"], region_dict["ylimits"], surge_afteraxes)

        surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
        surgeplot.add_land(plotaxes)
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

        # Speed Figure
        plotfigure = plotdata.new_plotfigure(name="Currents - %s" % name)
        plotaxes = plotfigure.new_plotaxes()
        standard_setup("Currents", region_dict["xlimits"], region_dict["ylimits"], surge_afteraxes)

        surgeplot.add_speed(plotaxes, bounds=speed_limits)
        surgeplot.add_land(plotaxes, bounds=color_limits)
        plotaxes.plotitem_dict['speed'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10
    #
    # Friction field
    #
    plotfigure = plotdata.new_plotfigure(name='Friction')
    plotfigure.show = friction_data.variable_friction and True
    plotaxes = plotfigure.new_plotaxes()
    standard_setup(None, regions['Full Domain']['xlimits'], regions['Full Domain']['ylimits'],
                   """plt.title(r"Manning\'s $n$ Coefficient")""")

    surgeplot.add_friction(plotaxes, bounds=friction_bounds)
    plotaxes.plotitem_dict['friction'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['friction'].colorbar_label = "$n$"

    #
    #  Hurricane Forcing fields
    #
    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure')
    plotfigure.show = surge_data.pressure_forcing and True
    plotaxes = plotfigure.new_plotaxes()
    standard_setup("Pressure Field", regions['Full Domain']['xlimits'], regions['Full Domain']['ylimits'],
                   surge_afteraxes)

    surgeplot.add_pressure(plotaxes, bounds=pressure_limits)
    surgeplot.add_land(plotaxes)

    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = surge_data.wind_forcing and True
    plotaxes = plotfigure.new_plotaxes()
    standard_setup("Wind Field", regions['Full Domain']['xlimits'], regions['Full Domain']['ylimits'], surge_afteraxes)

    surgeplot.add_wind(plotaxes, bounds=wind_limits)
    surgeplot.add_land(plotaxes)

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=300,
                                         type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    stations = [('8720218', 'Mayport (Bar Pilots Dock), FL'),
                ('8670870', 'Fort Pulaski, GA'),
                ('8665530', 'Charleston, Cooper River Entrance, SC'),
                ('8658163', 'Wrightsville Beach, NC'),
                ('8658120', 'Wilmington, NC')]

    landfall_time = np.datetime64('2016-10-08T12:00')
    begin_date = datetime.datetime(2016, 10, 6, 12)
    end_date = datetime.datetime(2016, 10, 9, 12)

    def gauge_afteraxes(current_data):
        axes = plt.gca()

        surgeplot.plot_landfall_gauge(current_data.gaugesoln, axes)
        station_id, station_name = stations[current_data.gaugeno - 1]

        date_time, water_level, prediction = geoutil.fetch_noaa_tide_data(station_id, begin_date, end_date,
                                                                          cache_dir=scratch_dir)

        # Subtract tide predictions from measured water levels
        water_level -= prediction
        # Calculate times relative to landfall
        seconds_rel_landfall = (date_time - landfall_time) / np.timedelta64(1, 's')

        axes.plot(seconds_rel_landfall, water_level, 'g', label='Observed')

        # Fix up plot
        axes.set_title(station_name + " - Station ID: " + station_id)
        axes.set_xlabel('Days relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_xlim([days2seconds(-2), days2seconds(1)])
        axes.set_ylim([-1, 3])
        axes.set_xticks([days2seconds(-2), days2seconds(-1), 0, days2seconds(1)])
        axes.set_xticklabels([r"$-2$", r"$-1$", r"$0$", r"$1$"])
        axes.grid(True)
        plt.legend(loc="upper left")

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
    gauge_regions = {"Mayport": {"xlimits": (-81.435, -81.39),
                                 "ylimits": (30.39, 30.41),
                                 "gaugenos": [1]},
                     "Fort Pulaski": {"xlimits": (-80.94, -80.84),
                                      "ylimits": (32.005, 32.058),
                                      "gaugenos": [2]},
                     "Charleston, Cooper River Entrance": {"xlimits": (-79.951, -79.836),
                                                           "ylimits": (32.731, 32.805),
                                                           "gaugenos": [3]},
                     "Wrightsville Beach": {"xlimits": (-77.7953, -77.7834),
                                            "ylimits": (34.2106, 34.2176),
                                            "gaugenos": [4]},
                     "Wilmington": {"xlimits": (-78.03, -77.87),
                                    "ylimits": (33.82, 34.25),
                                    "gaugenos": [5]},
                     "Carolinas": {"xlimits": (-80.5, -77.0),
                                   "ylimits": (31.5, 35),
                                   "gaugenos": [3, 4, 5, 6]},
                     "All": {"xlimits": (-82.0, -77.0),
                             "ylimits": (30.0, 35.0),
                             "gaugenos": "all"}}

    # Need queue since gauge_location_afteraxes will use the gaugenos specified for all plots that call it (because
    # it is executed after creating all plot items)
    num_frames = len(frametools.only_most_recent(plotdata.print_framenos, plotdata.outdir))
    queue = deque(list(gauge_regions.keys()) * num_frames)

    def which_gauges():
        # Returns gaugenos from current region_dict - used by gauge_location_afteraxes
        gaugenos = (gauge_regions[queue[0]])["gaugenos"]
        queue.popleft()
        return gaugenos

    def gauge_location_afteraxes(current_data):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(current_data)
        gaugetools.plot_gauge_locations(current_data.plotdata, gaugenos=which_gauges(),
                                        format_string='ko', add_labels=True)

    for (name, region_dict) in gauge_regions.items():
        plotfigure = plotdata.new_plotfigure(name="Gauge Locations - %s" % name)
        plotaxes = plotfigure.new_plotaxes()
        standard_setup("Gauge Locations", region_dict["xlimits"], region_dict["ylimits"], gauge_location_afteraxes)

        surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
        surgeplot.add_land(plotaxes)
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # -----------------------------------------
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True  # print figures
    plotdata.print_format = 'png'  # file format
    plotdata.print_framenos = 'all'  # list of frames to print
    plotdata.print_gaugenos = 'all'  # list of gauges to print
    plotdata.print_fignos = 'all'  # list of figures to print
    plotdata.html = True  # create html files of plots?
    plotdata.latex = True  # create latex file of plots?
    plotdata.latex_figsperline = 2  # layout of plots
    plotdata.latex_framesperline = 1  # layout of plots
    plotdata.latex_makepdf = False  # also run pdflatex?
    plotdata.parallel = True  # parallel plotting

    return plotdata
