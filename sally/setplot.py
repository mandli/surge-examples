
from __future__ import absolute_import
from __future__ import print_function

import os

import numpy
import matplotlib.pyplot as plt
import datetime

import pandas as pd

import clawpack.visclaw.colormaps as colormap
import clawpack.visclaw.gaugetools as gaugetools
import clawpack.clawutil.data as clawutil
import clawpack.amrclaw.data as amrclaw
import clawpack.geoclaw.data as geodata
import clawpack.geoclaw.util

import clawpack.geoclaw.surge.plot as surgeplot

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

i = 0 # Used as global variable to iterate through gauges and plot each one's location 

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
    surface_limits = [-2, 2]
    speed_limits = [0.0, 3.0]
    wind_limits = [0, 64]
    pressure_limits = [935, 1013]
    friction_bounds = [0.01, 0.04]

    def friction_after_axes(cd):
        plt.title(r"Manning's $n$ Coefficient")

    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    regions = {"Gulf": {"xlimits": (clawdata.lower[0], clawdata.upper[0]),
                        "ylimits": (clawdata.lower[1], clawdata.upper[1]),
                        "figsize": (6.4, 4.8)},
               "Coast": {"xlimits": (-90, -86),
                               "ylimits": (28, 31.5),
                               "figsize": (8, 4)}}

    
    import gzip
    from clawpack.geoclaw.surge.storm import Storm
    from clawpack.clawutil import data

    # Scratch directory for storing topo and storm files:
    scratch_dir = os.path.join(os.environ["CLAW"], 'geoclaw', 'scratch')

    # Convert ATCF data to GeoClaw format
    data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2020/bal192020.dat.gz")
    atcf_path = os.path.join(scratch_dir, "bal192020.dat")
    # Note that the get_remote_file function does not support gzip files which
    # are not also tar files.  The following code handles this
    with gzip.open(".".join((atcf_path, 'gz')), 'rb') as atcf_file,    \
            open(atcf_path, 'w') as atcf_unzipped_file:
        atcf_unzipped_file.write(atcf_file.read().decode('ascii'))


    sally = Storm(path=atcf_path, file_format="ATCF")

    # Time of landfall - Need to specify as the file above does not
    # include this info (9/16/2020 ~9am UTC)
    sally.time_offset = datetime.datetime(2020, 9, 16, 9)


    def category_afteraxes(cd):
        axes = plt.gca()
        surgeplot.add_track(sally, axes, intensity=True)
        surge_afteraxes(cd)


    plotfigure = plotdata.new_plotfigure(name="Path with Category")
    plotfigure.show = True
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Gulf']['xlimits']
    plotaxes.ylimits = regions['Gulf']['ylimits']

    plotaxes.afteraxes = surge_afteraxes
    
    plotaxes.title = "Path with Category"
    plotaxes.afteraxes = category_afteraxes
    plotaxes.scaled = False

    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10    
    
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
    plotaxes.xlimits = regions['Gulf']['xlimits']
    plotaxes.ylimits = regions['Gulf']['ylimits']
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
    plotaxes.xlimits = regions['Gulf']['xlimits']
    plotaxes.ylimits = regions['Gulf']['ylimits']
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_pressure(plotaxes, bounds=pressure_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = surge_data.wind_forcing and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = regions['Gulf']['xlimits']
    plotaxes.ylimits = regions['Gulf']['ylimits']
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

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-4.5, 2] # Days from landfall
    plotaxes.ylimits = [-3, 2] # Surface (m)
    plotaxes.title = 'Surface'


    # Reading in gauges from CSV file

    scratch_dir = os.path.join(os.environ["CLAW"], 'geoclaw', 'scratch')
    all_gauges_path = os.path.join(scratch_dir, "gauges.csv")

    all_gauges = pd.read_csv(all_gauges_path)
    gauge_IDs = all_gauges.iloc[:,1]
    my_dict = {i+1: str(gauge_IDs[i]) for i in range(gauge_IDs.size)} # append gauges

    num_gauges = len(all_gauges.iloc[:,5]) # number of gauges

    # To manually append gauges (without .csv file), use:
    # my_dict = {1: 'gauge_ID', 2: 'gauge_ID', etc.}

    def gauge_afteraxes(cd):
        t0 = datetime.datetime(2020, 9, 11, 21) # initial time
        t_offset = datetime.datetime(2020, 9, 16, 9) # landfall
        tf = datetime.datetime(2020, 9, 18, 9) # final time
        date_time, water_level, prediction = clawpack.geoclaw.util.fetch_noaa_tide_data(my_dict[cd.gaugeno], t0, tf)
        axes = plt.gca()

        surgeplot.plot_landfall_gauge(cd.gaugesoln, axes) # simulation

        date_time = date_time.astype('O')
        t = numpy.empty(date_time.shape[0]) # time array
        for j, dt in enumerate(date_time):
            t[j] = (dt - t_offset).total_seconds() / 86400
        initial_water_level = water_level[0] - prediction[0] # used to offset graph so it starts at 0 m
        axes.plot(t, water_level - prediction - initial_water_level) # plot data from noaa
       
        # Fix up plot - in particular fix time labels
        axes.set_title('Station %s' % cd.gaugeno)
        axes.set_xlabel('Days relative to landfall')
        axes.set_ylabel('Surface (m)')

        axes.set_xlim([-4.5, 2]) # t0 and tf
        axes.set_ylim([-3, 2])
        axes.set_xticks([-4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]) # adjust x_ticks
        axes.set_xticklabels([r"$-4$", r"", r"$-3$", r"", r"$-2$", r"", r"$-1$", r"", r"$-0$", r"", r"$1$", r"", r"$2$"])
        axes.set_yticks([-3, -2.75, -2.5, -2.25, -2, -1.75, -1.5, -1.25, -1, -.75, -.5, -.25, 0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2]) # adjust y_ticks
        axes.set_yticklabels([r"$-3$", r"$-2.75$", r"$-2.5$", r"$-2.25$", r"$-2$", r"$-1.75$", r"$-1.5$", r"$-1.25$", r"$-1$", r"$-.75$", r"$-.5$", r"$-.25$", r"$0$", r"$.25$", r"$.5$", r"$.75$", r"$1$", r"$1.25$", r"$1.5$", r"$1.75$", r"$2$"])

        axes.grid(True)
    
    plotaxes.afteraxes = gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'b-'

    # Loops across all gauges to print individual gauge location plots
    def loop():
        global i
        i += 1
        return (i - 1) % num_gauges


    # Gauge Locations
    # Picks bounds for individual gauge location plots
    # n is the gauge number (1, 2, 3, ...)

    def pickXlimits(n): # longitude
        long = all_gauges.iloc[n,8]
        return [long-0.5, long+0.5]

    def pickYlimits(n): # latitude
        lat = all_gauges.iloc[n,5]
        return [lat-0.5, lat+0.5] 

    

    # Plots all gauge locations on one figure

    def gauge_location_afteraxes_all(cd):
        
        surge_afteraxes(cd)

        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos='all',
                                        format_string='ko', add_labels=True, 
                                        markersize=3, fontsize=10)

    plotfigure = plotdata.new_plotfigure(name="Gauge Locations (All)")
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Gauge Locations (All)'
    plotaxes.scaled = True
    plotaxes.xlimits = [-90, -86.5]
    plotaxes.ylimits = [29, 31.5]

    plotaxes.afteraxes = gauge_location_afteraxes_all
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    
    # Hides edges of refinement regions
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10
    

    # Plot individual gauge locations

    def gauge_location_afteraxes(cd):
        
        surge_afteraxes(cd)

        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[loop()+1],
                                        format_string='ko', add_labels=True) 


    # Array to store gauge location figures
    figures = [] 

    for i in range(num_gauges):

        xLims = pickXlimits(i)
        yLims = pickYlimits(i)

        figures.append(plotdata.new_plotfigure(name="Gauge " + str(i+1)))

        figures[i].show = True

        plotaxes = figures[i].new_plotaxes(name=str(i+1))
        plotaxes.title = 'Gauge Locations'
        plotaxes.scaled = False
        plotaxes.xlimits = xLims
        plotaxes.ylimits = yLims

        plotfigure.clf_each_gauge = True
        
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

    print(type(plotdata))
    return plotdata
