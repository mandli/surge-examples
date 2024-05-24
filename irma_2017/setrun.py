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
import numpy as np

from clawpack.geoclaw.surge.storm import Storm
import clawpack.clawutil as clawutil


# Time Conversions
def days2seconds(days):
    return days * 60.0**2 * 24.0

# Scratch directory for storing topo and dtopo files:
data_dir = os.path.join(os.environ.get('datadir', os.getcwd()))


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
    clawdata.lower[0] = -90.0      # west longitude
    clawdata.upper[0] = -60.0       # east longitude

    clawdata.lower[1] = 15.0       # south latitude
    clawdata.upper[1] = 35.0       # north latitude

    # Number of grid cells:
    degree_factor = 4 # (0.25º,0.25º) ~ (25237.5 m, 27693.2 m) resolution
    clawdata.num_cells[0] = int(clawdata.upper[0] - clawdata.lower[0]) * degree_factor
    clawdata.num_cells[1] = int(clawdata.upper[1] - clawdata.lower[1]) * degree_factor

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
        clawdata.tfinal = days2seconds(2)
        recurrence = 4
        clawdata.num_output_times = int((clawdata.tfinal - clawdata.t0) * recurrence / (60**2 * 24))
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
    clawdata.order = 1

    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'

    # For unsplit method, transverse_waves can be
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 1

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
    amrdata.amr_levels_max = 7                

    # List of refinement ratios at each level (length at least mxnest-1)
    amrdata.refinement_ratios_x = [2, 2, 2, 2, 6, 4]
    amrdata.refinement_ratios_y = [2, 2, 2, 2, 6, 4]
    amrdata.refinement_ratios_t = [2, 2, 2, 2, 6, 4]

    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center', 'capacity', 'yleft', 'center', 'center', 'center', 'center']

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

    # region for entire domain
    regions.append([1, 2, rundata.clawdata.t0, rundata.clawdata.tfinal, -90.0, -60.0, 15.0, 35.0])

    # regions of higher refinement around gauges
    regions.append([5, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, -81.2, -80.9, 24.6, 24.8])
    regions.append([6, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, -81.9, -81.65, 24.4, 24.7])
    regions.append([3, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, -81.9, -81.5, 25.75, 26.25])
    regions.append([4, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, -83.0, -82.0, 27.0, 28.0])
    regions.append([2, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, -83.5, -82.5, 27.5, 28.5])
    regions.append([5, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, -66.5, -65.5, 18.0, 19.0])

    # regions of lower refinement
    regions.append([1, 1, rundata.clawdata.t0, rundata.clawdata.tfinal, -75.0, -60.0, 25.0, 35.0])
    regions.append([1, 1, rundata.clawdata.t0, rundata.clawdata.tfinal, -90.0, -85.0, 17.5, 25.0])
    regions.append([1, 1, rundata.clawdata.t0, rundata.clawdata.tfinal, -90.0, -60.0, 15.0, 17.5])
    regions.append([1, 1, rundata.clawdata.t0, rundata.clawdata.tfinal, -90.0, -75.0, 32.5, 35.0])
    
    # ------------------------------------------ Gauges for Irma ----------------------------------------
    # Vaca Key, Florida Bay, FL (ID: 8723970) (Marathon)
    # https://tidesandcurrents.noaa.gov/waterlevels.html?id=8723970&units=standard&bdate=20170907&edate=20170913&timezone=GMT&datum=MLLW&interval=6&action=
    rundata.gaugedata.gauges.append([1, -81.1057, 24.7119, rundata.clawdata.t0, rundata.clawdata.tfinal])
    
    # Key West, FL (ID: 8724580)
    # https://tidesandcurrents.noaa.gov/waterlevels.html?id=8724580&units=standard&bdate=20170907&edate=20170913&timezone=GMT&datum=MLLW&interval=6&action=
    rundata.gaugedata.gauges.append([2, -81.7885, 24.5763, rundata.clawdata.t0, rundata.clawdata.tfinal])
    
    # Naples, Gulf of Mexico, FL (ID: 8725110)
    # https://tidesandcurrents.noaa.gov/waterlevels.html?id=8725110&units=standard&bdate=20170907&edate=20170913&timezone=GMT&datum=MLLW&interval=6&action=
    rundata.gaugedata.gauges.append([3, -81.8211, 26.1316, rundata.clawdata.t0, rundata.clawdata.tfinal])

    # Port Manatee, FL (ID: 8726384)
    # https://tidesandcurrents.noaa.gov/waterlevels.html?id=8726384&units=standard&bdate=20170907&edate=20170913&timezone=GMT&datum=MLLW&interval=6&action=
    rundata.gaugedata.gauges.append([4, -82.5678, 27.6382, rundata.clawdata.t0, rundata.clawdata.tfinal])

    # Clearwater Beach, FL (ID: 8726724)
    # https://tidesandcurrents.noaa.gov/waterlevels.html?id=8726724&units=standard&bdate=20170907&edate=20170913&timezone=GMT&datum=MLLW&interval=6&action=
    rundata.gaugedata.gauges.append([5, -82.8341, 27.9778, rundata.clawdata.t0, rundata.clawdata.tfinal])

    # San Juan, PR (ID: 9755371)
    # https://tidesandcurrents.noaa.gov/waterlevels.html?id=9755371&units=standard&bdate=20170907&edate=20170913&timezone=GMT&datum=MLLW&interval=6&action=
    rundata.gaugedata.gauges.append([6, -66.1165, 18.4570, rundata.clawdata.t0, rundata.clawdata.tfinal])

    # ----------------------------------------------------------------------------------------------------

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
    # Due to seasonal swelling of gulf we set sea level higher
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 1.e-2

    # Refinement Criteria
    refine_data = rundata.refinement_data
    refine_data.wave_tolerance = 1.0
    refine_data.speed_tolerance = [1.0, 2.0, 3.0, 4.0]
    refine_data.deep_depth = 300.0
    refine_data.max_level_deep = 4
    refine_data.variable_dt_refinement_ratios = True

    # == settopo.data values ==
    topo_data = rundata.topo_data
    topo_data.topofiles = []
    # for topography, append lines of the form:[topotype, minlevel, maxlevel, t1, t2, fname]
    # See regions for control over these regions, need better bathy data for the smaller domains
    # !!!!!!!!!!!!!!!!NEED TO MODIFY PATH HERE IF TESTING EXAMPLE!!!!!!!!!!!!!
    topo_path = os.path.join(data_dir, "gebco_irma_topo.asc")
    topo_data.topofiles.append([3, 1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, topo_path])

    # == setfixedgrids.data values ==
    rundata.fixed_grid_data.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,ioutarrivaltimes,ioutsurfacemax]

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
    data.storm_file = os.path.expandvars(os.path.join(os.getcwd(),'irma.storm'))

    # Convert ATCF data to GeoClaw format
    clawutil.data.get_remote_file("https://ftp.nhc.noaa.gov/atcf/archive/2017/bal112017.dat.gz")
    atcf_path = os.path.join(data_dir, "bal112017.dat")
    
    # Note that the get_remote_file function does not support gzip files which
    # are not also tar files.  The following code handles this
    with gzip.open(".".join((atcf_path, 'gz')), 'rb') as atcf_file, open(atcf_path, 'w') as atcf_unzipped_file:
        atcf_unzipped_file.write(atcf_file.read().decode('ascii'))

    # irma = Storm(path="old_irma.storm", file_format="ATCF")
    irma = Storm(path=atcf_path, file_format="ATCF")

    # Calculate landfall time - Need to specify as the file above does not
    # Irma landfall in Cudjoe Key: 9/10/2017 ~ 09:10 EDT, 13:10 UTC
    irma.time_offset = datetime.datetime(2017, 9, 10, 13)

    irma.write(data.storm_file, file_format='geoclaw')

    # =======================
    #  Set Variable Friction
    # =======================
    data = rundata.friction_data

    # Variable friction
    data.variable_friction = True

    # Region based friction
    # Entire domain
    data.friction_regions.append([rundata.clawdata.lower, rundata.clawdata.upper, [np.infty, 0.0, -np.infty], [0.030, 0.022]])

    # La-Tex Shelf
    data.friction_regions.append([(-98, 25.25), (-90, 30), [np.infty, -10.0, -200.0, -np.infty], [0.030, 0.012, 0.022]])

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
