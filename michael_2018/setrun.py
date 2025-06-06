# encoding: utf-8
"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
import datetime
import shutil
import gzip

import numpy as np

from clawpack.geoclaw.surge.storm import Storm
import clawpack.clawutil as clawutil
import clawpack.geoclaw.topotools as topotools

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
    clawdata.lower[0] = -90      # west longitude
    clawdata.upper[0] = -65   # east longitude
    
    clawdata.lower[1] = 8      # south latitude
    clawdata.upper[1] = 33     # north latitude

    # Number of grid cells:
    num_deg = 4
    degree_factor = num_deg  # (0.25º,0.25º) ~ (25237.5 m, 27693.2 m) resolution
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
    clawdata.t0 = days2seconds(-2)

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
        t_final = 1
        num_recurrence = 12
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.tfinal = days2seconds(t_final)
        recurrence = num_recurrence
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
        clawdata.output_t0 = False

    clawdata.output_format = 'binary'      # 'ascii' or 'binary'
    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'all'
    clawdata.output_aux_onlyonce = False    # output aux arrays only at t0

    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 1

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
    clawdata.steps_max = 5000

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
    amrdata.refinement_ratios_x = [2,2,2,4,4]
    amrdata.refinement_ratios_y = [2,2,2,4,4]
    amrdata.refinement_ratios_t = [2,2,2,4,4]

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
    # full region
    regions.append([1,1,clawdata.t0,clawdata.tfinal, clawdata.lower[0],clawdata.upper[0],clawdata.lower[1],clawdata.upper[1]])
    # secondary region
    regions.append([2,3,clawdata.t0, clawdata.tfinal, -87.5,-82.5, 27.5, 31])

    # gauge = 1;-84.980;29.724;          8728690; APCF1, Apalachicola, FL, O
    # gauge = 2; -80.903;32.035;         9670870; FPKG1, Fort Pulaski. GA
    # gauge = 3; -82.8532264;27.9841164;  8726724; CWBF1, Clearwater Beach, FL, A2
    # gauge = 4; -85.6667;30.1517;        8729108; PACF1, Panama City, FL, O
    # gauge = 5; -87.21; 30.40; 8729840; PCLF1, Pensacola
    # gauge = 6;-85.8808554;30.2095418; 8729210; PCBF1, Panama City Beach, FL, A
    # gauge = 7;-82.5518544;27.8602907; 8726607; OPTF1, Old Port Tampa, FL, A
    # gauge = 8;-87.21;30.40;           8729840; PCLF1, Pensacola, FL, O
    # region
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-84.980-0.25,-84.980+0.25,29.724-0.25,29.724+0.25])
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-80.903-0.25,-80.903+0.25,32.035-0.25,32.035+0.25])
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-82.8532264-0.25,-82.8532264+0.25,27.9841164-0.25,27.9841164+0.25])
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-85.6667-0.25,-85.6667+0.25,30.1517-0.25,30.1517+0.25])
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-87.21-0.25,-87.21+0.25,30.40-0.25,30.40+0.25])
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-85.8808554-0.25,-85.8808554+0.25,30.2095418-0.25,30.2095418+0.25])
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-82.5518544-0.25,-82.5518544+0.25,27.8602907-0.25,27.8602907+0.25])
    regions.append([5,6,clawdata.t0, clawdata.tfinal,-87.21-0.25,-87.21+0.25,30.40-0.25,30.40+0.25])

    # == set gauges ==    
    rundata.gaugedata.gauges.append([1, -84.980, 29.724, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([2, -80.903, 32.035, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([3, -82.8532264, 27.9841164, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([4, -85.6667, 30.1517, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([5, -87.21, 30.40, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([6, -85.8808554, 30.2095418, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([7, -82.5518544, 27.8602907, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([8, -87.21, 30.40, rundata.clawdata.t0, rundata.clawdata.tfinal])


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
    # Note that inS the original paper due to gulf summer swelling this was set
    # to 0.28
    geo_data.sea_level = 0
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
    
    GEBCO_path = os.path.join(os.environ["DATA_PATH"], "topography", "GEBCO", "GEBCO_2023.nc")
    topo_path = os.path.join(scratch_dir, "gebco_2023_n45_s00_w-105_e-35.tt3")
    if not os.path.exists(topo_path):
        topo_file = topotools.Topography()
        topo_file.read(GEBCO_path, topo_type=4)
        topo_file = topo_file.crop((-105.5, -34.5, -0.5, 45.5))
        topo_file.write(path=topo_path, topo_type=3)
    topo_data.topofiles.append([3, topo_path])
    topo_data.topofiles.append([3, topo_path])


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
                                         "michael.storm"))

    # Convert ATCF data to GeoClaw format
    clawutil.data.get_remote_file(
                   "http://ftp.nhc.noaa.gov/atcf/archive/2018/bal142018.dat.gz")
    atcf_path = os.path.join(scratch_dir, "bal142018.dat")
    # Note that the get_remote_file function does not support gzip files which
    # are not also tar files.  The following code handles this
    # with gzip.open(".".join((atcf_path, 'gz')), 'rb') as atcf_file,    \
    #         open(atcf_path, 'w') as atcf_unzipped_file:
    #     atcf_unzipped_file.write(atcf_file.read().decode('ascii'))
    
    michael = Storm(path=atcf_path, file_format="ATCF")

    # Calculate landfall time - Need to specify as the file above does not

    michael.time_offset = datetime.datetime(2018, 10, 10, 17, 0)

    

    michael.write(data.storm_file, file_format='geoclaw')

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
                                  [np.inf, 0.0, -np.inf],
                                  [0.030, 0.022]])

    # La-Tex Shelf
    data.friction_regions.append([(-98, 25.25), (-90, 30),
                                  [np.inf, -10.0, -200.0, -np.inf],
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
    # quick_setup_parameters()