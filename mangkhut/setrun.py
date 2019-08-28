# encoding: utf-8
"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

from __future__ import absolute_import
from __future__ import print_function
from scipy.integrate import solve_ivp, odeint
from scipy.optimize import root,fsolve
from sympy import *

import os
import datetime
import shutil
import gzip

import numpy as np

import clawpack.clawutil as clawutil
import clawpack.geoclaw.units as units
from clawpack.geoclaw.surge.storm_Mangkhut import Storm

# Function solving the outer-region equation.
def solve_outer_region(r0, chi, f, v0=0, num=0):
    
    # Calculate initial value for outer-region equation
    def f0(x):
        M0 = 0.5 * f * r0**2 * 1000
        return (M0 - x[0]) / 0.1 - (x[0] - 0.5 * f * (r0-0.1)**2 * 1000)**2 / (r0**2 - (r0-0.1)**2)
    y0 = fsolve(f0, 0.5 * f * r0**2 * 1000)[0]
    def outer_region(y, t):
        return -chi * (y - 0.5 * f * t**2 * 1000)**2 / (r0**2 - t**2)
    n = int((r0 - 0.1 - 0.1) * 10 + 1)
    t = np.linspace(-r0+0.1, -0.1, n)
    
    # Solve outer-region equation to get absolute angular momentum
    M_solver = odeint(outer_region, y0=y0, t=t)
    v = np.empty(n)
    n1 = -1
    
    # Calculate velocity of every radius
    for i in range(n):
        v[n - i - 1] = -(M_solver[i] - 0.5 * f * t[i]**2 * 1000) / t[i]
        
        # Find the given velocity v0 and its radius r[n1]
        if np.abs(v[n - i - 1] - v0) < 1e-1:
            n1 = n - i - 1
    r = np.linspace(0.1, r0-0.1, n)
    
    # Absolute angular momentum at radius r[num]
    M = v[num] * r[num] + 0.5 * f * r[num]**2 * 1000
    return r[n1], M, v[num]
    
# Find r0, parameter of outer-region equation.
def Find_r0(r_r0, v_r0, chi, f):
    r0_find = np.linspace(r_r0 + 1, 5000, 5000)
    number = len(r0_find)
    
    # Giving specific v, v_r0, find r0 which make v_r0's radius equal to r_r0
    for m in range(number):
        r_test = solve_outer_region(r0_find[m], chi, f, v0=v_r0, num=0)[0]
        if np.abs(r_test - r_r0) < 5e-1:
            return(r0_find[m])
            break
            
# Calculate radius of maximum wind
def max_wind_radius_calculation(storm):
    r"""
    Use the approach: Complete Radial Structure in the paper [1] to calculate 
    radius of maximum wind.
    
    :Input:
    - *storm* (object) Storm
    
    1. Chavas, D. R., N. Lin, and K. Emanuel, A model for the complete radial 
    structure of the tropical cyclone wind field. Part I: Comparison with 
    observed structure. J. Atmos. Sci., 72, 3647–3662 (2015).
    """
    
    rm, ra, va = symbols('rm ra va')
    A = np.mat(zeros(3,3))
    B = np.matrix(np.arange(9).reshape((3,3)), dtype = 'float')

    
    # Number of data lines in storm object
    num = len(storm.t)

    # w - the average angular velocity of Earth’s rotation
    w = 7.292e-5
    
    v30 = units.convert(30.0, 'knots', 'm/s')
    
    # Calculate radius of maximum wind with Newton Method
    for i in range(num):
        if (i != 0) & (storm.t[i] == storm.t[i-1]):
            storm.max_wind_radius[i] = storm.max_wind_radius[i-1]
            continue
        
        # Radius of 30kts wind
        r30 = -1
        for j in range(max(i-2, 0), min(i+3, num)):
            if (storm.wind_speeds[i, 1] != -1) & (np.abs(storm.wind_speeds[i, 0] - v30) < 1e-5) & (storm.t[j] == storm.t[i]):
                r30 = units.convert(storm.wind_speeds[i, 1], 'm', 'nmi')
                break
            else:
                r30 = -1
                 
        # Find radius of maximum defined wind speed (such as 30kt, 50kt in atcf
        # file) in every record.        
        max_record_wind_radius = -1
        a = storm.wind_speeds[i, 0]
        b = i
        for k in range(max(i-2, 0), min(i+3, num)):
            if (storm.t[k] == storm.t[i]) & (storm.wind_speeds[k, 0] > a) & (storm.wind_speeds[k, 1] != -1):
                b = k
                a = storm.wind_speeds[k, 0]
        max_record_wind_radius = units.convert(storm.wind_speeds[b, 1], 'm', 'nmi')
            
        # Latitude
        phi = storm.eye_location[i, 1] * np.pi / 180.0
        
        # Coriolis parameter
        f = 2 * np.sin(phi) * w
                
        # Speed of maximum wind
        vm = units.convert(storm.max_wind_speed[i], 'm/s', 'knots')
        chi_30 = 1.0
        if (np.abs(r30) < 1e-5) | (np.abs(r30 + 1) < 1e-5):
            storm.max_wind_radius[i] = -1
            continue
        
        # Parameter of the equationn set
        r0 = Find_r0(r30, v30, chi_30, f)
        chi = 1.0
        CkCd = 1.0
        
        # The equation set
        f1 = ((ra * va + 0.5 * f * ra**2 * 1000) / (rm * vm + 0.5 * f * rm**2 * 1000))**(CkCd) - 2 * (ra / rm)**2 / (2 - CkCd + CkCd * (ra / rm)**2)
        f2 = 2 * (ra * va + 0.5 * f * ra**2 * 1000) / (ra * ((ra / rm)**2 + 1)) - chi * (ra * va)**2 / (r0**2 - ra**2)
        f32 = lambda ra, v, va: chi * (ra * v)**2 / (r0**2 - ra**2) - va - f * ra * 1000
        
        # Initial Guess for Newton Method
        x0 = [1.0, 1.0, 1.0]
        xk = [0, 0, 0]
        step = 0
        if (max_record_wind_radius == -1) | (np.abs(max_record_wind_radius) < 1e-5):
            storm.max_wind_radius[i] = -1
            continue
        x0[0] = max_record_wind_radius / 2.0
        x0[1] = max_record_wind_radius
        num_1 = int((x0[1] - 0.1) * 10)
        M1 = solve_outer_region(r0, chi, f, v0=0, num=num_1)
        x0[2] = M1[2]
        Fx0 = [-1, -1, -1]
        max_wind_radius = 0
        
        # Newton Method
        while((abs(Fx0[0]) > 1.e-3) | (abs(Fx0[1]) > 1.e-3) | (abs(Fx0[2]) > 1.e-3)):
            F = [f1, f2]
            x = [rm, ra, va]
            for m in range(2):
                for n in range(3):
                    A[m, n] = diff(F[m], x[n])
            xk = x0
            for m in range(2):
                for n in range(3):
                    B[m, n] = A[m, n].evalf(subs={rm:xk[0], ra:xk[1], va:xk[2]})
                    
            # Check whether va is negative or whether ra is larger than outer radius r0
            num_2 = int((xk[1] - 0.1) * 10)
            if (num_2 < 0) | (xk[1] > r0):
                max_wind_radius = -1
                break
            M2 = solve_outer_region(r0, chi, f, v0=0, num=num_2)
            B[2, 0] = 0
            B[2, 1] = f32(xk[1], M2[2], xk[2])
            B[2, 2] = -xk[1]
            Fx1 = f1.evalf(subs={rm:xk[0], ra:xk[1], va:xk[2]})
            Fx2 = f2.evalf(subs={rm:xk[0], ra:xk[1], va:xk[2]})
            Fx3 = M2[1] - (xk[1] * xk[2] + 0.5 * f * xk[1]**2 * 1000)
            Fx0 = [Fx1, Fx2, Fx3]
            Fx = np.array(Fx0).reshape(-1,1)
            
            # Check whether inv(B) exists
            if np.linalg.matrix_rank(B) != 3:
                break
            B1 = np.linalg.inv(B)
            B2 = B1 * Fx
            for l in range(3):
                x0[l] = xk[l] - B2.sum(axis=1)[l, 0]
            step = step + 1
            if step > 1.e3:
                max_wind_radius = -1
                break
        if (max_wind_radius != -1) & (x0[0] > 0) & (x0[0] < r0):
            max_wind_radius = x0[0]
            storm.max_wind_radius[i] = units.convert(float(max_wind_radius), 'km', 'm')
        else:
            storm.max_wind_radius[i] = -1
    return None

# Time Conversions
def days2seconds(days):
    return days * 60.0**2 * 24.0

def seconds2days(seconds):
    return seconds / (60.0**2 * 24.0)

# Scratch directory for storing topo and dtopo files:
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

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = clawutil.data.ClawRunData(claw_pkg, num_dim)

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
    clawdata.lower[0] = 103.0      # west longitude
    clawdata.upper[0] = 135.0      # east longitude

    clawdata.lower[1] = 5.0       # south latitude
    clawdata.upper[1] = 35.0      # north latitude

    # Number of grid cells:
    degree_factor = 4 # (0.25º,0.25º) ~ (25237.5 m, 27693.2 m) resolution
    clawdata.num_cells[0] = int(clawdata.upper[0] - clawdata.lower[0]) *      \
                                degree_factor
    clawdata.num_cells[1] = int(clawdata.upper[1] - clawdata.lower[1]) *      \
                                degree_factor

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
    clawdata.t0 = -days2seconds(3.0)

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
        # clawdata.tfinal = days2seconds(date2days('2008091400'))
        clawdata.tfinal = days2seconds(0.75)
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
    clawdata.steps_max = 100000

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

    elif clawdata.checkpt_style == 1:
        # Checkpoint only at tfinal.
        pass

    elif clawdata.checkpt_style == 2:
        # Specify a list of checkpoint times.
        clawdata.checkpt_times = [0.1, 0.15]

    elif clawdata.checkpt_style == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5

    # ---------------
    # AMR parameters:
    # ---------------
    amrdata = rundata.amrdata

    # max number of refinement levels:
    amrdata.amr_levels_max = 6

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
    regions.append([1, 6, rundata.clawdata.t0, rundata.clawdata.tfinal,
                    111.71666667, 111.91666667, 21.48333333, 21.68333333])
    regions.append([1, 6, rundata.clawdata.t0, rundata.clawdata.tfinal,
                    112.26, 112.86, 21.3, 21.7])
    regions.append([1, 6, rundata.clawdata.t0, rundata.clawdata.tfinal,
                    114.11333333, 114.31333333, 22.19111111, 22.39111111])
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    
    # Gauge from Tide Prediction Table of Zhapo Station
    rundata.gaugedata.gauges.append([1, 111.81666667, 21.58333333,
                                     rundata.clawdata.t0,
                                     rundata.clawdata.tfinal])
    # Gauge from SatRef of Hong Kong Quarry Bay Station
    rundata.gaugedata.gauges.append([2, 114.21333333, 22.29111111,
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

    try:
        geo_data = rundata.geo_data
    except:
        print("*** Error, this rundata has no geo_data attribute")
        raise AttributeError("Missing geo_data attribute")

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
    geo_data.sea_level = 0
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
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]
    # See regions for control over these regions, need better bathy data for
    # the smaller domains
    topo_path = os.path.join(scratch_dir, 'etopo2.asc')
    topo_data.topofiles.append([3, 1, 4, rundata.clawdata.t0,
                                rundata.clawdata.tfinal,
                                topo_path])

    # == setfixedgrids.data values ==
    rundata.fixed_grid_data.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    # ================
    #  Set Surge Data
    # ================
    data = rundata.surge_data

    # Source term controls - These are currently not respected
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
                                         'mangkhut.storm'))

    # Convert ATCF data to GeoClaw format
    atcf_path = os.path.join(scratch_dir, "MangkhutATCF.dat")
    
    with open(atcf_path, 'rb') as atcf_file:
        atcf_file.read().decode('ascii')
    
    mangkhut = Storm(path=atcf_path, file_format="ATCF")

    # Calculate landfall time - Need to specify as the file above does not
    # include this info (~2345 UTC - 6:45 p.m. CDT - on August 28)
    mangkhut.time_offset = datetime.datetime(2018, 9, 16, 6)
    
    max_wind_radius_calculation(mangkhut)

    mangkhut.write(data.storm_file, file_format='geoclaw')


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
