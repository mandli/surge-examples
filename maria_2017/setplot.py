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
    surface_limits = [-2.0, 2.0]
    speed_limits = [0.0, 2.0]
    wind_limits = [0, 64]
    pressure_limits = [935, 1013]
    friction_bounds = [0.01, 0.04]

    def friction_after_axes(cd):
        plt.title(r"Manning's $n$ Coefficient")

    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    regions = {"Atlantic": {"xlimits": (clawdata.lower[0], clawdata.upper[0]),
                        "ylimits": (clawdata.lower[1], clawdata.upper[1]),
                        "figsize": (6.4, 4.8)},
                "Puerto Rico": {"xlimits": (-69, -64),
                                "ylimits": (17, 19),
                                "figsize": (6.4, 2.56)}
              }
               
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

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-2, 1]
    # plotaxes.xlabel = "Days from landfall"
    # plotaxes.ylabel = "Surface (m)"
    plotaxes.ylimits = [-1, 5]
    plotaxes.title = 'Surface'
    
    #gauge data
    #may or may not keep this? see irene example
    #credit for below code to author of Irene example
    try: #add proper file names, and files themselves
        gauges = [np.loadtxt('gauge_data_1.txt'),
            np.loadtxt('gauge_data_2.txt'),
            np.loadtxt('gauge_data_3.txt'),
            np.loadtxt('gauge_data_4.txt'),
            np.loadtxt('gauge_data_5.txt')]
        #gauge locations
        data_names = ["St. Croix, VI, Data from NOAA",
                "Vieques Island, PR, Data from NOAA",
                "Fajardo, PR, just for corroboration",
                "San Juan, PR, Data from NOAA",
                "Arecibo, PR, Data from NOAA"]
    except:
        print("Add gauge files to directory")
    
    #May potentially need to change this function to place
    #multiple gauges ... refer to completed examples
    def gauge_afteraxes(cd):

        axes = plt.gca()
        surgeplot.plot_landfall_gauge(cd.gaugesoln, axes)

        # Fix up plot - in particular fix time labels
        axes.set_title('Station %s' % cd.gaugeno)
        axes.set_xlabel('Days relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_xlim([-2, 1]) #change this?
        axes.set_ylim([-1, 5]) #change this?
        axes.set_xticks([-2, -1, 0, 1]) #change this if line 204 changes
        axes.set_xticklabels([r"$-2$", r"$-1$", r"$0$", r"$1$"]) #same as 206
        axes.grid(True)
    
    
    #may or may not keep this? see irene example
    #credit for below code to author of Irene example
    # try:
    #     gauge_data=gaugea[cd.gaugeno-1]
    #     axes.plot(gauge_data[:,0], gauge_data[:,1], label=data_names[cd.gaugeno-1])
    #     axes.legend()
    # except:
    #         print('Gauge Data Unavailable')
    #irene code ends here
    plotaxes.afteraxes = gauge_afteraxes #originally line 209 - KEEP!!

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 3
    # plotitem.plotstyle = 'b-'

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
    plotaxes.xlimits = [-64, -69] # change depending on gauge axes
    plotaxes.ylimits = [17.0, 19.0] # same as line above
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
    plotdata.print_gaugenos = [1, 2, 3, 4, 5]   # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # parallel plotting

    return plotdata
