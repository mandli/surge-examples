#!/usr/bin/env python

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

# Set indices

surgeplot.wind_field = 2
surgeplot.pressure_field = 4

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

    # def storm_radius(cd):
    #     # Plot 300 km circle around eye to indicate outer edge of storm radius
    #     track_data = track.get_track(cd.frameno)
    #     return np.sqrt((cd.x - track_data[0])**2 + (cd.y - track_data[1])**2)

    # def add_storm_radius(ax, radius=[100e3]):
    #     plotitem = plotaxes.new_plotitem(name="storm radius", plot_type="2d_contour")
    #     plotitem.plot_var = storm_radius
    #     plotitem.contour_levels = radius
    #     plotitem.contour_colors = 'r'

    # Color limits
    surface_limits = [-1.0, 1.0]
    H = 3e3
    speed_limits = [0.0, 1.0]
    wind_limits = [0, 64]
    pressure_limits = [935, 1013]
    storm_radii = [100e3, 300e3]

    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # Surface Figure
    plotfigure = plotdata.new_plotfigure(name="Surface")
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Surface"
    plotaxes.xlimits = (clawdata.lower[0], clawdata.upper[0])
    plotaxes.ylimits = (clawdata.lower[1], clawdata.upper[1])
    plotaxes.scaled = True
    plotaxes.afteraxes = surge_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_storm_radii(plotaxes, track, radii=storm_radii)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # Speed Figure
    plotfigure = plotdata.new_plotfigure(name="Currents")
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Currents"
    plotaxes.xlimits = (clawdata.lower[0], clawdata.upper[0])
    plotaxes.ylimits = (clawdata.lower[1], clawdata.upper[1])
    plotaxes.scaled = True
    plotaxes.afteraxes = surge_afteraxes
    surgeplot.add_speed(plotaxes, bounds=speed_limits)
    surgeplot.add_storm_radii(plotaxes, track, radii=storm_radii)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    plotaxes.plotitem_dict['speed'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # ==========================
    #  Hurricane Forcing Fields
    # ==========================
    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure')
    plotfigure.show = surge_data.pressure_forcing and True
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = (clawdata.lower[0], clawdata.upper[0])
    plotaxes.ylimits = (clawdata.lower[1], clawdata.upper[1])
    plotaxes.scaled = True
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_pressure(plotaxes, bounds=pressure_limits)
    surgeplot.add_storm_radii(plotaxes, track, radii=storm_radii)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed')
    plotfigure.show = surge_data.wind_forcing and True
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = (clawdata.lower[0], clawdata.upper[0])
    plotaxes.ylimits = (clawdata.lower[1], clawdata.upper[1])
    plotaxes.scaled = True
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    surgeplot.add_wind(plotaxes, bounds=wind_limits)
    surgeplot.add_storm_radii(plotaxes, track, radii=storm_radii)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.plot_var = surgeplot.wind_speed
    plotitem.contour_levels = [10, 20, 30, 40, 50, 60]
    plotitem.contour_colors = ['blue']

    # plotfigure = plotdata.new_plotfigure(name='Wind Speed X')
    # plotfigure.show = surge_data.wind_forcing and True
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.xlimits = (clawdata.lower[0], clawdata.upper[0])
    # plotaxes.ylimits = (clawdata.lower[1], clawdata.upper[1])
    # plotaxes.title = "Wind Field X"
    # plotaxes.afteraxes = surge_afteraxes
    # plotaxes.scaled = True    
    # plotitem = plotaxes.new_plotitem(name='wind', plot_type='2d_pcolor')
    # plotitem.plot_var = surgeplot.wind_x
    # plotitem.pcolor_cmap = surgeplot.velocity_cmap    
    # plotitem.pcolor_cmin = -wind_limits[1]
    # plotitem.pcolor_cmax = wind_limits[1]
    # plotitem.add_colorbar = True
    # plotitem.colorbar_label = "Wind Speed (m/s)"
    # surgeplot.add_storm_radii(plotaxes, track, radii=storm_radii)
    # surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # plotfigure = plotdata.new_plotfigure(name='Wind Speed Y')
    # plotfigure.show = surge_data.wind_forcing and True
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.xlimits = (clawdata.lower[0], clawdata.upper[0])
    # plotaxes.ylimits = (clawdata.lower[1], clawdata.upper[1])
    # plotaxes.title = "Wind Field Y"
    # plotaxes.afteraxes = surge_afteraxes
    # plotaxes.scaled = True    
    # plotitem = plotaxes.new_plotitem(name='wind', plot_type='2d_pcolor')
    # plotitem.plot_var = surgeplot.wind_y
    # plotitem.pcolor_cmap = surgeplot.velocity_cmap    
    # plotitem.pcolor_cmin = -wind_limits[1]
    # plotitem.pcolor_cmax = wind_limits[1]
    # plotitem.add_colorbar = True
    # plotitem.colorbar_label = "Wind Speed (m/s)"
    # surgeplot.add_storm_radii(plotaxes, track, radii=storm_radii)
    # surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])

    # ===========
    #  Transects
    # ===========
    def compute_max(current_data, field=3, title=r"Field {} - $\max = {}$"):
        ax = plt.gca()
        max_value = np.max(np.abs(current_data.q[field, :, :]))
        ax.set_title(title.format(field, max_value))

    def transect(current_data, field=3, y0=0.0):
        y = current_data.y
        dy = current_data.dy
        index = np.where(abs(y - y0) <= dy / 2.0)[1][0]
        if field < 0:
            # Extract velocity
            h = current_data.q[0, :, index]
            hu = current_data.q[abs(field), :, index]
            u = np.where(h > 1e-3, hu / h, np.zeros(h.shape))
            return current_data.x[:, index], u
        elif field == 4:
            # Plot topography
            h = current_data.q[0, :, index]
            eta = current_data.q[3, :, index]
            return current_data.x[:, index], eta - h
        else:
            return current_data.x[:, index], current_data.q[field, :, index]

    # === Surface/Topography ===
    plotfigure = plotdata.new_plotfigure(name="Surface Transect")
    plotfigure.show = True
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Surface Transect"
    plotaxes.xlabel = "x (m)"
    plotaxes.ylabel = r"$\eta$"
    plotaxes.xlimits = [clawdata.lower[0], clawdata.upper[0]]
    plotaxes.ylimits = surface_limits
    plotaxes.grid = True
    plotaxes.afteraxes = lambda cd: compute_max(cd)

    plotitem = plotaxes.new_plotitem(plot_type="1d_from_2d_data")
    plotitem.map_2d_to_1d = transect
    plotitem.plotstyle = "ko-"
    plotitem.kwargs = {"markersize": 3}

    plotitem = plotaxes.new_plotitem(plot_type="1d_from_2d_data")
    plotitem.map_2d_to_1d = lambda cd: transect(cd, field=4)
    plotitem.plotstyle = "g"
    plotitem.kwargs = {"markersize": 3}

    # === Depth ===
    plotfigure = plotdata.new_plotfigure(name="Depth Transect")
    plotfigure.show = False
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Depth Transect"
    plotaxes.xlabel = "x (m)"
    plotaxes.ylabel = r"$h$"
    plotaxes.xlimits = [clawdata.lower[0], clawdata.upper[0]]
    plotaxes.ylimits = [H + surface_limits[0], H + surface_limits[1]]
    plotaxes.grid = True
    plotaxes.afteraxes = lambda cd: compute_max(cd, field=0)

    plotitem = plotaxes.new_plotitem(plot_type="1d_from_2d_data")
    plotitem.map_2d_to_1d = lambda cd: transect(cd, field=0)
    plotitem.plotstyle = "ko-"
    plotitem.kwargs = {"markersize": 3}

    # === Momentum/Velocity ===
    plotfigure = plotdata.new_plotfigure(name="Momentum Transect")
    plotfigure.show = True
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = r"Momentum Transect - $\max |hu|$"
    plotaxes.xlabel = "x (m)"
    plotaxes.ylabel = r"$hu$"
    plotaxes.xlimits = [clawdata.lower[0], clawdata.upper[0]]
    plotaxes.ylimits = [-speed_limits[1], speed_limits[1]]
    plotaxes.grid = True
    plotaxes.afteraxes = lambda cd: compute_max(cd, field=1)

    # plotitem = plotaxes.new_plotitem(plot_type="1d_from_2d_data")
    # plotitem.map_2d_to_1d = lambda cd: transect(cd, field=1)
    # plotitem.plotstyle = "ko-"
    # plotitem.kwargs = {"markersize": 3}

    plotitem = plotaxes.new_plotitem(plot_type="1d_from_2d_data")
    plotitem.map_2d_to_1d = lambda cd: transect(cd, field=-1)
    plotitem.plotstyle = "bx-"
    plotitem.kwargs = {"markersize": 3}

    # ========
    #  Gauges
    # ========
    plotfigure = plotdata.new_plotfigure(name='Gauge Surface and Velocity', 
                                         type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True

    plotfigure = plotdata.new_plotfigure(name="Gauge Surfaces", figno=300, 
                                         type="each_gauge")
    plotfigure.show = True
    plotfigure.clf_each_gauge = True
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.time_scale = 1 / (24 * 60**2)
    plotaxes.grid = True
    plotaxes.xlimits = "auto"
    plotaxes.ylimits = "auto"
    plotaxes.title = "Surface"
    plotaxes.ylabel = "Surface (m)"
    plotaxes.time_label = "t (s)"
    plotitem = plotaxes.new_plotitem(plot_type="1d_plot")
    plotitem.plot_var = surgeplot.gauge_surface

    # Gauge Location Plot
    def gauge_location_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos='all',
                                        format_string='ko', add_labels=False)

    plotfigure = plotdata.new_plotfigure(name="Gauge Locations")
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Gauge Locations'
    plotaxes.scaled = True
    plotaxes.xlimits = (clawdata.lower[0], clawdata.upper[0])
    plotaxes.ylimits = (clawdata.lower[1], clawdata.upper[1])
    plotaxes.afteraxes = gauge_location_afteraxes
    surgeplot.add_surface_elevation(plotaxes, bounds=surface_limits)
    surgeplot.add_storm_radii(plotaxes, track, radii=storm_radii)
    surgeplot.add_land(plotaxes, bounds=[0.0, 20.0])
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # -----------------------------------------
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'        # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # parallel plotting

    return plotdata
