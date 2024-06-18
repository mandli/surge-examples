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

import clawpack.clawutil.data as data
from clawpack.geoclaw.surge.storm import Storm
import clawpack.clawutil as clawutil


# Time Conversions
def days2seconds(days):
    return days * 60.0**2 * 24.0


# Scratch directory for storing topo and storm files:
scratch_dir = os.path.join(os.environ["CLAW"], 'geoclaw', 'scratch')


class BCTestData(data.ClawData):

    def __init__(self):
        super(BCTestData, self).__init__()

        # Incoming wave momentum flux modification
        # alpha \in [0, 1]
        #   alpha = 0:      Incoming momentum is zero
        #   0 < alpha < 1:  Incoming momentum is decayed from zero-order extrapolated value
        #   alpha = 1:      Incoming momentum is zero-order extrapolated
        self.add_attribute('alpha_bc', 1.0)

    def write(self, data_source='setrun.py', out_file='bc_test.data'):

        self.open_data_file(out_file, data_source)
        self.data_write('alpha_bc',
                        description="(Incoming momentum flux modification)")

        self.close_data_file()

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
    clawdata.lower[0] = -500e3      # west longitude
    clawdata.upper[0] = 500e3      # east longitude

    clawdata.lower[1] = -500e3     # south latitude
    clawdata.upper[1] = 500e3     # north latitude

    # Number of grid cells:
    clawdata.num_cells[0] = 200
    clawdata.num_cells[1] = 200

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    # First three are from shallow GeoClaw, fourth is friction and last 3 are
    # storm fields
    clawdata.num_aux = 1 + 1 + 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 0

    # -------------
    # Initial time:
    # -------------
    clawdata.t0 = days2seconds(-1)

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
    clawdata.tfinal = days2seconds(3)

    if clawdata.output_style == 1:
        # Output nout frames at equally spaced times up to tfinal:
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
        clawdata.total_steps = 10
        clawdata.output_t0 = True

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
    clawdata.steps_max = 2**16

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

    clawdata.checkpt_style = 1

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
        clawdata.checkpt_interval = 100

    # ---------------
    # AMR parameters:
    # ---------------
    amrdata = rundata.amrdata

    # max number of refinement levels:
    amrdata.amr_levels_max = 1

    # List of refinement ratios at each level (length at least mxnest-1)
    amrdata.refinement_ratios_x = [2, 2, 2, 6, 16]
    amrdata.refinement_ratios_y = [2, 2, 2, 6, 16]
    amrdata.refinement_ratios_t = [2, 2, 2, 6, 16]

    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center', 'center', 'center', 'center', 'center']

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
    rundata.gaugedata.gauges.append([0, rundata.clawdata.lower[0], 0.0,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([1, 0.0, 0.0,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([2, rundata.clawdata.upper[0], 0.0,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal])

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
    geo_data.coordinate_system = 1
    geo_data.earth_radius = 6367.5e3
    geo_data.rho = 1025.0
    geo_data.rho_air = 1.15
    geo_data.ambient_pressure = 101.3e3

    # == Forcing Options
    geo_data.coriolis_forcing = False
    geo_data.friction_forcing = False

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
    topo_data.test_topography = 2

    topo_data.x0 = rundata.clawdata.lower[0] + 1e8
    topo_data.x1 = rundata.clawdata.lower[0] + 2e8
    topo_data.x2 = rundata.clawdata.lower[0] + 3e8

    topo_data.basin_depth = -3e3
    topo_data.shelf_depth = -200.0
    topo_data.beach_slope = 0.05

    # Indexing
    rundata.friction_data.friction_index = 1
    rundata.surge_data.wind_index = 2
    rundata.surge_data.pressure_index = 4

    # ================
    #  Set Surge Data
    # ================
    data = rundata.surge_data

    # Source term controls
    data.wind_forcing = True
    data.drag_law = 1
    data.pressure_forcing = True
    data.rotation_override = "N"

    data.display_landfall_time = True

    # AMR parameters, m/s and m respectively
    data.wind_refine = [20.0, 40.0, 60.0]
    data.R_refine = [60.0e3, 40e3, 20e3]

    # Storm parameters - Parameterized storm (Holland 1980)
    data.storm_specification_type = 'holland80'  # (type 1)
    data.storm_file = os.path.join(os.getcwd(), 'synthetic.storm')

    # Construct synthetic storm
    storm = Storm()
    storm.time_offset = 0.0
    num_forecasts = 24
    storm.t = np.linspace(rundata.clawdata.t0, rundata.clawdata.tfinal,
                             num_forecasts)

    def ramp_function(t):
        c = days2seconds(1)
        return np.where(t < 0.0,
                           -2 / c**3 * t**3 - 3 / c**2 * t**2 + 1,
                           np.ones(t.shape))

    def storm_x(t):
        # 15 km/h storm speed
        storm_v = 15 / 3.6
        x0 = 0.0
        return x0 + storm_v * t

    storm.eye_location = np.array([[storm_x(t), 0.0] for t in storm.t])
    storm.max_wind_speed = np.array([64.0 for t in storm.t])

    # Max Wind Radius
    C0 = 218.3784
    storm.max_wind_radius = np.empty(num_forecasts)
    for (n, t) in enumerate(storm.t):
        storm.max_wind_radius[n] = (C0 - 1.2014 * storm.max_wind_speed[n]
                                    + (storm.max_wind_speed[n] / 10.9884)**2
                                    - (storm.max_wind_speed[n] / 35.3052)**3
                                    - 145.5090 * np.cos(storm.eye_location[n, 1] * 0.0174533)) * 1e3

    # Add central pressure - From Kossin, J. P. WAF 2015
    # a = -0.0025
    # b = -0.36
    # c = 1021.36
    # storm.central_pressure = np.empty(num_forecasts)
    # for (n, t) in enumerate(storm.t):
    #     storm.central_pressure[n] = ( a * storm.max_wind_speed[n]**2
    #             + b * storm.max_wind_speed[n] + c) * ramp_function(t)

    storm.central_pressure = geo_data.ambient_pressure - \
        (geo_data.ambient_pressure - 940e2) * ramp_function(storm.t)

    # Extent of storm set to 300 km
    storm.storm_radius = 300e3 * np.ones(num_forecasts)

    # Write out storm
    storm.write(data.storm_file, file_format='geoclaw')

    # BC Test source term splitting
    #  0 = no momentum flux
    #  1 = zero-extrapolation
    rundata.add_data(BCTestData(), 'bc_test_data')
    rundata.bc_test_data.alpha_bc = 1.0

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
