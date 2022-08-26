
from __future__ import absolute_import
from __future__ import print_function

import os

import numpy as np
import matplotlib.pyplot as plt
import datetime

import clawpack.visclaw.colormaps as colormap
import clawpack.visclaw.gaugetools as gaugetools
import clawpack.clawutil.data as clawutil
import clawpack.amrclaw.data as amrclaw
import clawpack.geoclaw.data as geodata
import clawpack.geoclaw.surge.plot as surgeplot
import csv
from clawpack.geoclaw.util import fetch_noaa_tide_data


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
        surgeplot.surge_afteraxes(cd, track, plot_direction=True,
                                             kwargs={"markersize": 4})
    def plot_coastline(cd):
        """Load fine coastline for plotting around NYC"""
        try:
            # Assumes that at path theres a fine topography file in NetCDF file format
            path = "/Users/mandli/Dropbox/research/data/topography/atlantic/sandy_bathy/ny_area.nc"
            topo_file = topotools.Topography(path, topo_type=4)
            topo_file.read(nc_params={"x_var":"lon", 
                                      "y_var":"lat", 
                                      "z_var": "Band1"})

            axes = plt.gca()
            axes.contour(topo_file.X, topo_file.Y, topo_file.Z, 
                         levels=[-0.001, 0.001], 
                         colors='k', linestyles='-')
        except:
            pass

        surge_afteraxes(cd)

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
    regions = {'Full Domain': {"xlimits": [clawdata.lower[0], clawdata.upper[0]],
                               "ylimits": [clawdata.lower[1], clawdata.upper[1]],
                               "shrink": 1.0,
                               "figsize": [6.4, 4.8]},
               'Tri-State Region': {"xlimits": [-74.5,-71.0],
                                    "ylimits": [40.0,41.5],
                                    "shrink": 1.0,
                                    "figsize": [6.4, 4.8]},
                'NYC': {"xlimits": [-74.2,-73.7],
                        "ylimits": [40.4,40.85],
                        "shrink": 1.0,
                        "figsize": [6.4, 4.8]}
               }
    for (name, region_dict) in regions.items():

        # Surface Figure
        plotfigure = plotdata.new_plotfigure(name="Surface - %s" % name)
        plotfigure.kwargs = {"figsize": region_dict['figsize']}
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.title = "Surface"
        plotaxes.xlimits = region_dict["xlimits"]
        plotaxes.ylimits = region_dict["ylimits"]
        plotaxes.afteraxes = plot_coastline
        # plotaxes.afteraxes = surge_afteraxes

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
        plotaxes.afteraxes = plot_coastline
        # plotaxes.afteraxes = surge_afteraxes

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
    plotaxes.title = "Manning's N Coefficient"
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
    plotfigure = plotdata.new_plotfigure(name='Gauge Surfaces', figno=300,
                                         type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    stations = [ ('8518750', 'The Battery, NY'),
            ('8516945', 'Kings Point, NY'),
            ('8510560', 'Montauk, NY'),
            ('8467150', 'Bridgeport, CT'),
            ('8465705', 'New Haven, CT'),
            ('8461490','New London, CT')]

    # landfall_time = datetime.datetime(2012, 10, 29, 23, 30)
    
    landfall_time = np.datetime64("2012-10-29T23:30")
    begin_date = datetime.datetime(2012, 10, 28, 23, 30)
    end_date = datetime.datetime(2012, 10, 30, 23, 30)

    def get_actual_water_levels(station_id):
        # Fetch water levels and tide predictions for given station
        date_time, water_level, tide = fetch_noaa_tide_data(station_id,
                begin_date, end_date)

        # Calculate times relative to landfall
        days_rel_landfall = (date_time - landfall_time) / np.timedelta64(1,'s')  / 86400
        
        # Subtract tide predictions from measured water levels
        water_level -= tide
        
        # Find the mean values
        # Data imported every 6 minutes (i.e. 360 seconds)
        num_data_pts = (end_date - begin_date).total_seconds() / 360
        mean_value = np.sum(water_level) / num_data_pts
        water_level -= mean_value

        return days_rel_landfall, water_level
    
    #############################################
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-1, 1]
    # plotaxes.xlabel = "Days from landfall"
    # plotaxes.ylabel = "Surface (m)"
    plotaxes.ylimits = [-1, 4]
    plotaxes.title = 'Surface'

    def gauge_afteraxes(cd):
        station_id, station_name = stations[cd.gaugeno-1]
        days_rel_landfall, actual_level = get_actual_water_levels(station_id)
        
        axes = plt.gca()
        surgeplot.plot_landfall_gauge(cd.gaugesoln, axes)
        axes.plot(days_rel_landfall, actual_level, 'g')

        # Fix up plot - in particular fix time labels
        axes.set_title(station_name)
        axes.set_xlabel('Days relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_xlim([-1,1])
        axes.set_ylim([-1.5,3])
        axes.set_xticks([-1,-0.5,0,0.5,1])
        axes.set_yticks([-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3])
        axes.grid(True)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = gauge_afteraxes
    
    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
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
    plotaxes.xlimits = [-74.5, -71.6]
    plotaxes.ylimits = [40.5, 41.5]
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
    plotdata.print_gaugenos = 'all'   # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # parallel plotting

    return plotdata