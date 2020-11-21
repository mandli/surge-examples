from __future__ import absolute_import
from __future__ import print_function

import os

import numpy as np
import matplotlib.pyplot as plt
import datetime

import clawpack.visclaw.colormaps as colormap
import clawpack.visclaw.gaugetools as gaugetools
import clawpack.clawutil.data as clawdata
import clawpack.amrclaw.data as amrclaw
import clawpack.geoclaw.data as geodata
import clawpack.geoclaw.topotools as topotools

import clawpack.geoclaw.util as geoutil
import clawpack.geoclaw.surge.plot as surgeplot
# to compare actual gauge data plot:
import csv
from clawpack.geoclaw.util import fetch_noaa_tide_data

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

def days2seconds(days):
    return days * 60.0**2 * 24.0

def setplot(plotdata):
    r"""Setplot function for surge plotting"""


    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'ascii'

    # Load data from output
    claw_data = clawdata.ClawInputData(2)
    claw_data.read(os.path.join(plotdata.outdir, 'claw.data'))
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
    surface_range = 4.5
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
    regions = {'Full Domain': {"xlimits": [claw_data.lower[0], claw_data.upper[0]],
                               "ylimits": [claw_data.lower[1], claw_data.upper[1]],
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
    def gauge_location_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos='all',
                                        format_string='ko', add_labels=True)

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
        plotaxes.afteraxes = plot_coastline
        # plotaxes.afteraxes = surge_afteraxes
        # plotaxes.afteraxes = gauge_location_afteraxes

        surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits,
                                    shrink=region_dict['shrink'])
        surgeplot.add_land(plotaxes, bounds=land_bounds)

        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0,0,0]
        plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0,0,0]


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
        plotaxes.afteraxes = plot_coastline
        
        surgeplot.add_speed(plotaxes, bounds=speed_limits,
                        shrink=region_dict['shrink'])
        surgeplot.add_land(plotaxes, bounds=land_bounds)

        plotaxes.plotitem_dict['land'].amr_patchedges_show = [0,0,0]
        plotaxes.plotitem_dict['speed'].amr_patchedges_show = [0,0,0]



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
    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    stations = [('8518750', 'The Battery, NY'),
                ('8516945', 'Kings Point, NY'),
                ('8519483', 'Bergen Point West Reach, NY')]
                #('8531680','Sandy Hook, NY'),
                #('n03020','Narrows,NY')]

    landfall_time = np.datetime64('2012-10-29T23:30')
    begin_date = datetime.datetime(2012, 10, 28)
    end_date = datetime.datetime(2012, 10, 31,)

    def get_actual_water_levels(station_id):
        # Fetch water levels and tide predictions for given station
        date_time, water_level, tide = fetch_noaa_tide_data(station_id,
                begin_date, end_date)

        # Calculate times relative to landfall
        seconds_rel_landfall = (date_time - landfall_time) / np.timedelta64(1, 's')
        # Subtract tide predictions from measured water levels
        water_level -= tide

        return seconds_rel_landfall, water_level

    def gauge_afteraxes(cd):
        station_id, station_name = stations[cd.gaugeno-1]
        seconds_rel_landfall, actual_level = get_actual_water_levels(station_id)

        axes = plt.gca()
        #surgeplot.plot_landfall_gauge(cd.gaugesoln, axes, landfall=landfall)
        axes.plot(seconds_rel_landfall, actual_level, 'g')

        # Fix up plot - in particular fix time labels
        axes.set_title(station_name)
        axes.set_xlabel('Seconds relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_xlim([days2seconds(-2), days2seconds(1)])
        axes.set_ylim([0, 4])
        axes.set_xticks([ days2seconds(-2), days2seconds(-1), 0, days2seconds(1)])
        #axes.set_xticklabels([r"$-3$", r"$-2$", r"$-1$", r"$0$", r"$1$"])
        #axes.grid(True)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.afteraxes = gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
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
