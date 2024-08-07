
from __future__ import absolute_import
from __future__ import print_function

import os
import datetime

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import clawpack.visclaw.colormaps as colormap
import clawpack.visclaw.gaugetools as gaugetools
import clawpack.clawutil.data as clawutil
import clawpack.amrclaw.data as amrclaw
import clawpack.geoclaw.data as geodata
import clawpack.geoclaw.util as geoutil


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

    # Color limits
    surface_limits = [-5.0, 5.0]
    speed_limits = [0.0, 3.0]
    wind_limits = [0, 64]
    pressure_limits = [935, 1013]
    friction_bounds = [0.01, 0.04]

    def friction_after_axes(cd):
        plt.title(r"Manning's $n$ Coefficient")

    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    regions = {"Full Domain": {"xlimits": (clawdata.lower[0], clawdata.upper[0]),
                        "ylimits": (clawdata.lower[1], clawdata.upper[1]),
                        "figsize": (6.4, 4.8)},
               "South Carolina": {"xlimits": (-85, -75),
                               "ylimits": (30, 35),
                               "figsize": (8, 2.7)}}

    for (name, region_dict) in regions.items():

        # Surface Figure
        plotfigure = plotdata.new_plotfigure(name="Surface - %s" % name)
        plotfigure.kwargs = {"figsize": region_dict['figsize']}
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = "Surface"
        plotaxes.xlimits = region_dict["xlimits"]
        plotaxes.ylimits = region_dict["ylimits"]
        plotaxes.afteraxes = surge_afteraxes

        surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
        surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

        # Speed Figure
        plotfigure = plotdata.new_plotfigure(name="Currents - %s" % name)
        plotfigure.kwargs = {"figsize": region_dict['figsize']}
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = "Currents"
        plotaxes.xlimits = region_dict["xlimits"]
        plotaxes.ylimits = region_dict["ylimits"]
        plotaxes.afteraxes = surge_afteraxes

        surgeplot.add_speed(plotaxes, bounds=speed_limits)
        surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
        plotaxes.plotitem_dict['speed'].amr_patchedges_show = [0] * 10
        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10
    #
    # Friction field
    #
    plotfigure = plotdata.new_plotfigure(name='Friction')
    plotfigure.show = friction_data.variable_friction and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
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
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_pressure(plotaxes, bounds=pressure_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = surge_data.wind_forcing and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Full Domain']['xlimits']
    plotaxes.ylimits = regions['Full Domain']['ylimits']
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_wind(plotaxes, bounds=wind_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    def plot_observed(current_data):
        """Fetch and plot gauge data for gauges used."""

        # Map GeoClaw gauge number to NOAA gauge number and location/name
        gauge_mapping = {1: [8665530, "Charleston, SC"],
                         2: [8658120, 'Wilmington, NC'],
                         3: [8656483, 'Duke Marine Lab, NC']}

        station_id, station_name = gauge_mapping[current_data.gaugesoln.id]
        landfall_time = np.datetime64(datetime.datetime(2012, 8, 29, 0))
        begin_date = datetime.datetime(2012, 8, 27)
        end_date = datetime.datetime(2012, 8, 31)

        landfall_time = np.datetime64('1989-09-22T04:00')
        begin_date = datetime.datetime(1989, 9, 20)
        end_date = datetime.datetime(1989, 9, 23)

        # Load in local data
        path = os.path.abspath(os.path.join(current_data.plotdata.rundir, 
                                            "gauges", 
                                            "{}_data.csv".format(station_id)))

        data = pd.read_csv(path, engine="python", sep=",+", header=0, names=[
            "Date", "Time(GMT)", "Predicted(m)", "Verified(m)",
            "Preliminary(m)",
            "Forecast Guidance(m)", ],
                           converters={
                               "Date": lambda d: datetime.datetime(
                                   int(d[0:4]), int(d[5:7]), int(d[8:10])),
                               "Time(GMT)": lambda d: datetime.timedelta(
                                   hours=int(d[0:2])),
                           },
                           dtype={
                               "Predicted(m)": float,
                               "Verified(m)": float,
                           })

        data['DATE'] = data["Date"] + data["Time(GMT)"]
        date_time = data['DATE']
        water_level = data['Verified(m)']
        predicted_level = data['Predicted(m)']

        # Convert to seconds relative to landfall
        t = (date_time - landfall_time) / np.timedelta64(1, 's')
        t /= (24 * 60**2)

        # Detide
        water_level -= predicted_level

        # Plot data
        ax = plt.gca()
        ax.plot(t, water_level, color='lightgray', marker='x')
        ax.set_title(station_name)
        ax.legend(['Computed', "Dry", "Observed"])


    plotfigure = plotdata.new_plotfigure(name='Gauge Surfaces', figno=300,
                                         type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.time_scale = 1 / (24 * 60**2)
    plotaxes.grid = True
    plotaxes.xlimits = [-2, 1]
    plotaxes.ylimits = [-1, 7]
    plotaxes.title = "Surface"
    plotaxes.ylabel = "Surface (m)"
    plotaxes.time_label = "Days relative to landfall"
    plotaxes.afteraxes = plot_observed
    
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = surgeplot.gauge_surface
    # Plot red area if gauge is dry
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = surgeplot.gauge_dry_regions
    plotitem.kwargs = {"color":'lightcoral', "linewidth":5}
    
    #  Gauge Location Plot
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
    plotaxes.xlimits = [-81, -76]
    plotaxes.ylimits = [32, 35]
    plotaxes.afteraxes = gauge_location_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # -----------------------------------------
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # parallel plotting

    return plotdata
