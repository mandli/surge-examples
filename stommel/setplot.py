
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""

import os

import matplotlib.pyplot as plt

import clawpack.geoclaw.surge as surge
import clawpack.visclaw.colormaps as colormaps
import clawpack.clawutil.clawdata as clawdata

try:
    from setplotfg import setplotfg
except:
    setplotfg = None

def setplot(plotdata):
    r"""Setplot function for surge plotting"""
    

    plotdata.clearfigures()  # clear any old figures,axes,items data

    # Load data from output
    amrdata = clawdata.AmrclawInputData(2)
    amrdata.read(os.path.join(plotdata.outdir,'amrclaw.data'))
    physics = clawdata.GeoclawInputData(2)
    physics.read(os.path.join(plotdata.outdir,'geoclaw.data'))
    surge_data = surge.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir,'surge.data'))

    # Limits for plots
    full_xlimits = [amrdata.lower[0],amrdata.upper[0]]
    full_ylimits = [amrdata.lower[1],amrdata.upper[1]]

    # Color limits
    surface_range = 1.0
    speed_range = 1.0e-3

    xlimits = full_xlimits
    ylimits = full_ylimits
    eta = physics.sea_level
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    speed_limits = [0.0,speed_range]
    # surface_limits = None
    # speed_limits = None
    
    wind_limits = [0,1]

    # ==========================================================================
    #  Generic helper functions
    # ==========================================================================
    def pcolor_afteraxes(current_data):
        surge_afteraxes(current_data)
        
    def contour_afteraxes(current_data):
        surge_afteraxes(current_data)


    # ========================================================================
    #  Surge related helper functions
    # ========================================================================
    def surge_afteraxes(current_data):
        surge.plot.days_figure_title(current_data)
        m_to_km_labels(current_data)


    def m_to_km_labels(current_data=None):
        plt.xlabel('km')
        plt.ylabel('km')
        locs,labels = plt.xticks()
        labels = locs/1.e3
        plt.xticks(locs,labels)
        locs,labels = plt.yticks()
        labels = locs/1.e3
        plt.yticks(locs,labels)

    
    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================

    # ========================================================================
    #  Surface Elevations
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=0)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes
    
    surge.plot.add_surface_elevation(plotaxes,bounds=surface_limits)
    surge.plot.add_land(plotaxes)


    # ========================================================================
    #  Water Speed
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='speed', figno=1)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes

    # Speed
    surge.plot.add_speed(plotaxes,bounds=speed_limits)

    # Land
    surge.plot.add_land(plotaxes)


    # ========================================================================
    # Wind field
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Wind Speed',figno=4)
    plotfigure.show = surge_data.wind_forcing
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.plot.add_wind(plotaxes,bounds=wind_limits,plot_type='imshow')
    surge.plot.add_land(plotaxes)
    
    # Wind field components
    plotfigure = plotdata.new_plotfigure(name='Wind Components',figno=5)
    plotfigure.show = surge_data.wind_forcing
    plotfigure.kwargs = {'figsize':(16,6)}
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(121)"
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "X-Component of Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surge.plot.wind_x
    plotitem.imshow_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.imshow_cmin = -wind_limits[1]
    plotitem.imshow_cmax = wind_limits[1]
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = "subplot(122)"
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Y-Component of Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = surge.plot.wind_y
    plotitem.imshow_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.imshow_cmin = -wind_limits[1]
    plotitem.imshow_cmax = wind_limits[1]
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]

    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    # plotdata.print_framenos = [45,46,47,48]
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

