# encoding: utf-8
"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

from __future__ import absolute_import
from __future__ import print_function

import os
import datetime
import shutil
import gzip
from pylab import *
import numpy as np

from clawpack.geoclaw.surge.storm import Storm
import clawpack.clawutil as clawutil


# Time Conversions
def days2seconds(days):
    return days * 60.0**2 * 24.0


# Scratch directory for storing topo and storm files:
scratch_dir = os.path.join(os.environ["CLAW"], 'geoclaw', 'scratch')


# ------------------------------
def setrun(claw_pkg='geoclaw'):

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    from clawpack.clawutil import data

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)

    # ------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    # ------------------------------------------------------------------
    clawdata = rundata.clawdata  # initialized when rundata instantiated

    # Set single grid parameters first.
    # See below for AMR parameters.

    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

    # Lower and upper edge of computational domain:
    clawdata.lower[0] = -99.0      # west longitude
    clawdata.upper[0] = -70.0      # east longitude

    clawdata.lower[1] = 8.0       # south latitude
    clawdata.upper[1] = 32.0      # north latitude


    # Number of grid cells:
    degree_factor = 4  # (0.25º,0.25º) ~ (25237.5 m, 27693.2 m) resolution
    clawdata.num_cells[0] = int(clawdata.upper[0] - clawdata.lower[0]) \
        * degree_factor
    clawdata.num_cells[1] = int(clawdata.upper[1] - clawdata.lower[1]) \
        * degree_factor

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    # First three are from shallow GeoClaw, fourth is friction and last 3 are
    # storm fields
    clawdata.num_aux = 3 + 1 + 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2

    # -------------
    # Initial time:
    # -------------
    clawdata.t0 = -days2seconds(4)

    # Restart from checkpoint file of a previous run?
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False               # True to restart from prior results
    clawdata.restart_file = 'fort.chk00006'  # File to use for restart data

    # -------------
    # Output times:
    # --------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1

    if clawdata.output_style == 1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.tfinal = days2seconds(5)
        recurrence = 4
        clawdata.num_output_times = int((clawdata.tfinal - clawdata.t0) *
                                        recurrence / (60**2 * 24))

        clawdata.output_t0 = True  # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = [0.5, 1.0]

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 1
        clawdata.output_t0 = True

    clawdata.output_format = 'ascii'      # 'ascii' or 'binary'
    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'all'
    clawdata.output_aux_onlyonce = False    # output aux arrays only at t0

    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 0

    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = True

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 0.016

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 10000

    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2

    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'

    # For unsplit method, transverse_waves can be
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 2

    # Number of waves in the Riemann solution:
    clawdata.num_waves = 3

    # List of limiters to use for each wave family:
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc', 'mc', 'mc']

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms

    # Source terms splitting:
    #   src_split == 0 or 'none'
    #      ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov'
    #      ==> Godunov (1st order) splitting used,
    #   src_split == 2 or 'strang'
    #      ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'

    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.bc_lower[0] = 'extrap'
    clawdata.bc_upper[0] = 'extrap'

    clawdata.bc_lower[1] = 'extrap'
    clawdata.bc_upper[1] = 'extrap'

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 0

    if clawdata.checkpt_style == 0:
        # Do not checkpoint at all
        pass

    elif np.abs(clawdata.checkpt_style) == 1:
        # Checkpoint only at tfinal.
        pass

    elif np.abs(clawdata.checkpt_style) == 2:
        # Specify a list of checkpoint times.
        clawdata.checkpt_times = [0.1, 0.15]

    elif np.abs(clawdata.checkpt_style) == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5

    # ---------------
    # AMR parameters:
    # ---------------
    amrdata = rundata.amrdata

    # max number of refinement levels:
    amrdata.amr_levels_max = 5

    # List of refinement ratios at each level (length at least mxnest-1)
    amrdata.refinement_ratios_x = [2, 2, 2, 6, 16]
    amrdata.refinement_ratios_y = [2, 2, 2, 6, 16]
    amrdata.refinement_ratios_t = [2, 2, 2, 6, 16]

    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center', 'capacity', 'yleft', 'center', 'center',
                        'center', 'center']

    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0

    #  ----- For developers -----
    # Toggle debugging print statements:
    amrdata.dprint = False      # print domain flags
    amrdata.eprint = False      # print err est flags
    amrdata.edebug = False      # even more err est flags
    amrdata.gprint = False      # grid bisection/clustering
    amrdata.nprint = False      # proper nesting output
    amrdata.pprint = False      # proj. of tagged points
    amrdata.rprint = False      # print regridding summary
    amrdata.sprint = False      # space/memory output
    amrdata.tprint = False      # time step reporting each level
    amrdata.uprint = False      # update/upbnd reporting

    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    # == setregions.data values ==
    regions = rundata.regiondata.regions

    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    regions.append([1, 3, clawdata.t0, clawdata.tfinal, clawdata.lower[0], clawdata.upper[0], clawdata.lower[1], clawdata.upper[1]])
    regions.append([1, 5, clawdata.t0, clawdata.tfinal, -99, -91, 26.5, 32]) # More specific domain f/ LaTex domain, minlevel = 1, maxlevel > 3, e.g. Can custommize based on time domain



	# Ruled rectangles -allows more custom definition of refinement regions
    from clawpack.amrclaw.data import FlagRegion
    flagregion = FlagRegion(num_dim=2)
    flagregion.name = 'Region_LatexShelf'
    flagregion.minlevel = 2
    flagregion.maxlevel = 5
    flagregion.t1 = 0.
    flagregion.t2 = 1e9
    flagregion.spatial_region_type = 2 # Ruled Rectangle
    

    from numpy import ma # masked arrays
    from clawpack.visclaw import colormaps, plottools
    from clawpack.geoclaw import topotools, marching_front
    from clawpack.amrclaw import region_tools
    import clawpack.geoclaw.topotools as topo

    zmin = -60.
    zmax = 40.

    land_cmap = colormaps.make_colormap({ 0.0:[0.1,0.4,0.0],
                                        0.25:[0.0,1.0,0.0],
                                        0.5:[0.8,1.0,0.5],
                                        1.0:[0.8,0.5,0.2]})

    sea_cmap = colormaps.make_colormap({ 0.0:[0,0,1], 1.:[.8,.8,1]})

    cmap, norm = colormaps.add_colormaps((land_cmap, sea_cmap),
                                        data_limits=(zmin,zmax),
                                        data_break=0.)
                                        
    sea_cmap_dry = colormaps.make_colormap({ 0.0:[1.0,0.7,0.7], 1.:[1.0,0.7,0.7]})
    cmap_dry, norm_dry = colormaps.add_colormaps((land_cmap, sea_cmap_dry),
                                        data_limits=(zmin,zmax),
                                        data_break=0.)

    topo_file = topo.Topography()
    topo_file.read('../../../scratch/gulf_caribbean.tt3', topo_type=3)
    topo_file = topo_file.crop((-98, -90, 26.5, 32.5))

    pts_chosen = marching_front.select_by_flooding(topo_file.Z, Z1=0, Z2=1e6, max_iters=20)
    pts_chosen = marching_front.select_by_flooding(topo_file.Z, Z1=0, Z2=15., prev_pts_chosen=pts_chosen,
    max_iters=None)

    pts_chosen_shallow = marching_front.select_by_flooding(topo_file.Z, Z1=0, Z2=-25., max_iters=None)
    Zshallow = ma.masked_array(topo_file.Z, logical_not(pts_chosen_shallow))

    pts_chosen_nearshore = logical_and(pts_chosen, pts_chosen_shallow)
    Znearshore = ma.masked_array(topo_file.Z, logical_not(pts_chosen_nearshore))

    rr = region_tools.ruledrectangle_covering_selected_points(topo_file.X, topo_file.Y, pts_chosen_nearshore, 
                                                            ixy='x', method=0,
                                                            padding=0, verbose=True)

    rr_name = 'RuledRectangle_LatexShelf.data'
    
    rr.write(rr_name)

    flagregion.spatial_region_file = \
        os.path.abspath('RuledRectangle_LatexShelf.data')


    rundata.flagregiondata.flagregions.append(flagregion)

    # Gauges from NOAA website - Houston and Cameron LA

    rundata.gaugedata.gauges.append([1, -95.294, 28.936, 
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # Freeport Harbor, wet, 8772471
    rundata.gaugedata.gauges.append([2, -95.113, 29.095,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # San Luis Pass, wet (unable to locate on Google Maps), 8771972
    rundata.gaugedata.gauges.append([3, -94.897, 29.302, 
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # Galveston Railroad, sometimes dry, 8771486
    rundata.gaugedata.gauges.append([4, -94.792, 29.311,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # Galveston Pier 21, wet, 8771450
    rundata.gaugedata.gauges.append([5, -94.725, 29.357,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # Galveston Bay Entrance, wet, 8771341
    rundata.gaugedata.gauges.append([6, -94.511, 29.516,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # Rollover Pass, sometimes dry, 8770971
    rundata.gaugedata.gauges.append([7, -94.390, 29.595,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # High Island, sometimes dry, 8770808
    rundata.gaugedata.gauges.append([8, -94.985, 29.682, 
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # Morgans Point, wet, 8770613
    rundata.gaugedata.gauges.append([9, -95.266, 29.726,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal]) # Manchester, always dry, 8770777
    rundata.gaugedata.gauges.append([10, -93.343, 29.768,
 				     rundata.clawdata.t0,
				     rundata.clawdata.tfinal]) # Calcasieu Lake, Louisiana, sometimes dry, 8768094
    rundata.gaugedata.gauges.append([11, -93.842, 29.689, 
				     rundata.clawdata.t0,
				     rundata.clawdata.tfinal]) #  Sabine Pass, Louisiana, wet, 8770822

    # Force the gauges to also record the wind and pressure fields
    rundata.gaugedata.aux_out_fields = [4, 5, 6]

    # ------------------------------------------------------------------
    # GeoClaw specific parameters:
    # ------------------------------------------------------------------
    rundata = setgeo(rundata)

    return rundata
    # end of function setrun
    # ----------------------


# -------------------
def setgeo(rundata):
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    geo_data = rundata.geo_data

    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2
    geo_data.earth_radius = 6367.5e3
    geo_data.rho = 1025.0
    geo_data.rho_air = 1.15
    geo_data.ambient_pressure = 101.3e3

    # == Forcing Options
    geo_data.coriolis_forcing = True
    geo_data.friction_forcing = True
    geo_data.friction_depth = 1e10

    # == Algorithm and Initial Conditions ==
    # Note that in the original paper due to gulf summer swelling this was set
    # to 0.28
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 1.e-2

    # Refinement Criteria
    refine_data = rundata.refinement_data
    refine_data.wave_tolerance = 1.0
    refine_data.speed_tolerance = [1.0, 2.0, 3.0, 4.0]
    refine_data.variable_dt_refinement_ratios = True

    # == settopo.data values ==
    topo_data = rundata.topo_data
    topo_data.topofiles = []
    # for topography, append lines of the form
    #   [topotype, fname]
    # See regions for control over these regions, need better bathy data for
    # the smaller domains
    clawutil.data.get_remote_file(
           "http://www.columbia.edu/~ktm2132/bathy/gulf_caribbean.tt3.tar.bz2")
    topo_path = os.path.join(scratch_dir, 'gulf_caribbean.tt3')
    topo_data.topofiles.append([3, topo_path])

    # == setfixedgrids.data values ==
    rundata.fixed_grid_data.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    # ================
    #  Set Surge Data
    # ================
    data = rundata.surge_data

    # Source term controls
    data.wind_forcing = True
    data.drag_law = 1
    data.pressure_forcing = True

    data.display_landfall_time = True

    # AMR parameters, m/s and m respectively
    data.wind_refine = [20.0, 40.0, 60.0]
    data.R_refine = [60.0e3, 40e3, 20e3]

    # Storm parameters - Parameterized storm (Holland 1980)
    data.storm_specification_type = 'holland80'  # (type 1)
    data.storm_file = os.path.expandvars(os.path.join(os.getcwd(),
                                         'harvey.storm'))

    # Convert ATCF data to GeoClaw format
    clawutil.data.get_remote_file(
                   "http://ftp.nhc.noaa.gov/atcf/archive/2017/bal092017.dat.gz")
    atcf_path = os.path.join(scratch_dir, "bal092017.dat")
    # Note that the get_remote_file function does not support gzip files which
    # are not also tar files.  The following code handles this
    with gzip.open(".".join((atcf_path, 'gz')), 'rb') as atcf_file,    \
            open(atcf_path, 'w') as atcf_unzipped_file:
        atcf_unzipped_file.write(atcf_file.read().decode('ascii'))

    # Uncomment/comment out to use the old version of the Ike storm file
    # ike = Storm(path="old_ike.storm", file_format="ATCF")
    harvey = Storm(path=atcf_path, file_format="ATCF")

    # Calculate landfall time - Need to specify as the file above does not
    # include this info (8/26/2017 ~4am UTC)
    harvey.time_offset = datetime.datetime(2017, 8, 26, 4)

    harvey.write(data.storm_file, file_format='geoclaw')

    # =======================
    #  Set Variable Friction
    # =======================
    data = rundata.friction_data

    # Variable friction
    data.variable_friction = True

    # Region based friction
    # Entire domain
    data.friction_regions.append([rundata.clawdata.lower,
                                  rundata.clawdata.upper,
                                  [np.infty, 0.0, -np.infty],
                                  [0.030, 0.022]])

    # La-Tex Shelf
    data.friction_regions.append([(-98, 25.25), (-90, 30),
                                  [np.infty, -10.0, -200.0, -np.infty],
                                  [0.030, 0.012, 0.022]])

    return rundata
    # end of function setgeo
    # ----------------------


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    if len(sys.argv) == 2:
        rundata = setrun(sys.argv[1])
    else:
        rundata = setrun()

    rundata.write()
