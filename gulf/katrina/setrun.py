# encoding: utf-8
"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

from __future__ import print_function
from __future__ import absolute_import

import os
import sys
import datetime

from gzip import GzipFile
from six.moves.urllib.request import urlopen
import numpy as np

import clawpack.clawutil.data as data
import clawpack.geoclaw.topotools as topotools
import clawpack.geoclaw.etopotools as etopotools

# Landfall of hurricane 1110 UTC (6:10 a.m. CDT) on Monday, August 29, 2005
katrina_landfall = datetime.datetime(2005, 8, 29, 11, 10) \
                    - datetime.datetime(2005, 1, 1, 0, 0)

#                           days   s/hour    hours/day
days2seconds = lambda days: days * 60.0**2 * 24.0
seconds2days = lambda seconds: seconds / (60.0**2 * 24.0)


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
    rundata = data.ClawRunData(claw_pkg, num_dim)

    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------

    #probdata = rundata.new_UserData(name='probdata',fname='setprob.data')

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------

    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

    # Lower and upper edge of computational domain:
    clawdata.lower[0] = -99.0
    clawdata.upper[0] = -75.0

    clawdata.lower[1] = 15.0
    clawdata.upper[1] = 32.0


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
    clawdata.num_aux = 4 + 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2



    # -------------
    # Initial time:
    # -------------

    # Katrina 2005082412 20260800.000000000
    clawdata.t0 = days2seconds(katrina_landfall.days - 3) + katrina_landfall.seconds

    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1

    if clawdata.output_style == 1:
        # Output nout frames at equally spaced times up to tfinal:
        #                 day     s/hour  hours/day
        # Katrina 2005083012
        clawdata.tfinal = days2seconds(katrina_landfall.days + 1) + katrina_landfall.seconds

        # Output files per day requested
        recurrence = 48
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
        
    clawdata.output_format = 'binary'      # 'ascii' or 'netcdf'

    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'all' # could be list
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
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'
    # clawdata.source_split = 'strang'

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
    # Resolution in degrees 0.25, 0.125, 0.0625, 0.015625, 0.00390625
    # Resolution in ~meters 27.5e3, 13.75e3, 6.875e3, 1.71875e3, 429.6875
    amrdata.refinement_ratios_x = [2, 2, 4, 4, 4, 4]
    amrdata.refinement_ratios_y = [2, 2, 4, 4, 4, 4]
    amrdata.refinement_ratios_t = [2, 2, 4, 4, 4, 4]


    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center', 'capacity', 'yleft', 'center', 'center',
                        'center', 'center', 'center', 'center']

    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 2

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

    # == setgauges.data values ==
    gauges = rundata.gaugedata.gauges
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]

    # Grand Isle, LA (Station ID: 8761724)
    gauges.append([1, -89.96, 29.26, rundata.clawdata.t0, rundata.clawdata.tfinal])

    # Pilots Station East, SW Pass, LA (Station ID: 8760922)
    gauges.append([2, -89.41, 28.93, rundata.clawdata.t0, rundata.clawdata.tfinal])

    # Dauphin Island, AL (Station ID: 8735180)
    gauges.append([3, -88.08, 30.25, rundata.clawdata.t0, rundata.clawdata.tfinal])

    # == setregions.data values ==
    regions = rundata.regiondata.regions
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]

    dx = 0.1
    dy = 0.1

    for gauge in gauges:
        regions.append([amrdata.amr_levels_max, amrdata.amr_levels_max,
                        rundata.clawdata.t0, rundata.clawdata.tfinal,
                        gauge[1] - dx, gauge[1] + dx,
                        gauge[2] - dy, gauge[2] + dy])

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------

    rundata = setgeo(rundata)   # Defined below
    
    # Set storm
    set_storm(rundata)

    # Set variable friction
    set_friction(rundata)

    return rundata
    # end of function setrun
    # ----------------------


def setgeo(rundata):
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print("*** Error, this rundata has no geodata attribute")
        raise AttributeError("Missing geodata attribute")
       
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
    geo_data.manning_coefficient = 0.025 # Overridden below
    geo_data.friction_depth = 1e10

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.125  # Due to seasonal swelling of gulf
    geo_data.dry_tolerance = 1.e-2

    # Refinement Criteria
    refine_data = rundata.refinement_data
    refine_data.wave_tolerance = 1.0
    # refine_data.wave_tolerance = 0.5
    # refine_data.speed_tolerance = [0.25,0.5,1.0,2.0,3.0,4.0]
    # refine_data.speed_tolerance = [0.5,1.0,1.5,2.0,2.5,3.0]
    refine_data.speed_tolerance = [1.0,2.0,3.0,4.0]
    refine_data.deep_depth = 1e6
    refine_data.max_level_deep = 5
    refine_data.variable_dt_refinement_ratios = True

    # == settopo.data values ==
    topo_data = rundata.topo_data
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]

    # Fetch topography if needed
    topo_files = get_topo()

    for topo_file in topo_files:
        topo_data.topofiles.append([4, 1, 5,
                                    rundata.clawdata.t0, rundata.clawdata.tfinal,
                                    topo_file])
    topo_data.topofiles.append([3, 1, 5,
                                rundata.clawdata.t0, rundata.clawdata.tfinal,
                                os.path.join(os.environ['CLAW'], 'geoclaw', 'scratch', 'NewOrleans_3s.tt3')])

    # == setqinit.data values ==
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]
    # geodata.qinitfiles.append([1, 5, 'hump.xyz'])

    # == setfixedgrids.data values ==
    rundata.fixed_grid_data.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]
    # geodata.fixedgrids.append([1e3,3.24e4,10,-90,-80,-30,-15,100,100,0,1])

    return rundata
    # end of function setgeo
    # ----------------------


def set_storm(rundata):

    data = rundata.surge_data

    # Source term controls - These are currently not respected
    data.wind_forcing = True
    data.pressure_forcing = True
    data.drag_law = 2

    # AMR parameters - m/s for wind refinement and (m) for radius
    data.wind_refine = [20.0, 40.0, 60.0]
    data.R_refine = [60.0e3, 40e3, 20e3]

    # Storm parameters - Storm Type 1 is Holland parameterized
    data.storm_type = 1
    data.landfall = days2seconds(katrina_landfall.days)         \
                    + katrina_landfall.seconds
    data.display_landfall_time = True

    # Fetch storm track if needed
    storm_file = get_storm_track()

    # Storm type 1 - Idealized storm track
    data.storm_file = storm_file

    return data


def set_friction(rundata):

    data = rundata.friction_data

    # Variable friction
    data.variable_friction = True

    # Region based friction
    # Entire domain
    data.friction_regions.append([rundata.clawdata.lower,
                                  rundata.clawdata.upper,
                                  [np.infty, 0.0, -np.infty],
                                  [0.030, 0.022]])

    # # La-Tex Shelf
    # data.friction_regions.append([(-98, 25.25), (-90, 30),
    #                               [np.infty, -10.0, -200.0, -np.infty],
    #                               [0.030, 0.012, 0.022]])

    return data


def get_topo():
    """
    Retrieve the topo files from NOAA.
    """
    base_url = 'https://gis.ngdc.noaa.gov/mapviewer-support/wcs-proxy/wcs.groovy'

    claw_dir = os.environ['CLAW']
    scratch_dir = os.path.join(claw_dir, 'geoclaw', 'scratch')

    # Specify topo parameters as tuples of the form
    #   (res_mins, lat_min, lat_max, lon_min, lon_max)
    topo_params = [(10, 5, 35, -100, -70),     # Gulf
                   (1, 28, 31, -92.5, -87.5)]  # New Orleans

    topo_files = []

    for (res_mins, lat_min, lat_max, lon_min, lon_max) in topo_params:
        # Construct output file name
        lat_lon = '{}{}_{}{}_{}{}_{}{}'.format(abs(lat_min),
                                               'N' if lat_min >= 0 else 'S',
                                               abs(lat_max),
                                               'N' if lat_max >= 0 else 'S',
                                               abs(lon_min),
                                               'E' if lon_min >= 0 else 'W',
                                               abs(lon_max),
                                               'E' if lon_max >= 0 else 'W')
        topo_fname = 'etopo1_{}m_{}.nc'.format(res_mins, lat_lon)
        topo_files.append(os.path.join(scratch_dir, topo_fname))

        # Fetch topography
        #   Note: We manually create the query string because using 'urlencode'
        #   causes an internal server error.
        res_hrs = res_mins / 60.0
        url_params = {
            'filename': 'etopo1.nc',
            'request': 'getcoverage',
            'version': '1.0.0',
            'service': 'wcs',
            'coverage': 'etopo1',
            'CRS': 'EPSG:4326',
            'format': 'netcdf',
            'resx': '{:.18f}'.format(res_hrs),
            'resy': '{:.18f}'.format(res_hrs),
            'bbox': '{:.14f},{:.14f},{:.14f},{:.14f}'.format(lon_min, lat_min,
                                                             lon_max, lat_max)
        }
        query_str = '&'.join('{}={}'.format(k, v) for k, v in url_params.items())
        full_url = '{}?{}'.format(base_url, query_str)
        data.get_remote_file(full_url, file_name=topo_fname, verbose=True)

    return topo_files


def get_storm_track(verbose=True):
    """
    Retrieve the storm track file from NOAA.
    """
    url = 'http://ftp.nhc.noaa.gov/atcf/archive/2005/bal122005.dat.gz'

    claw_dir = os.environ['CLAW']
    scratch_dir = os.path.join(claw_dir, 'geoclaw', 'scratch')
    output_path = os.path.join(scratch_dir, 'bal122005.dat')

    # Download and decompress storm track file if it does not already exist
    if not os.path.exists(output_path):
        if verbose:
            print('Downloading storm track file')
        with urlopen(url) as response:
            with GzipFile(fileobj=response) as fin:
                with open(output_path, 'wb') as fout:
                    fout.write(fin.read())
    elif verbose:
        print('Using previously downloaded storm track file')

    return output_path


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.

    rundata = data.ClawRunData("geoclaw", 2)
    if len(sys.argv) == 2:
        rundata = setrun(sys.argv[1])
    else:
        rundata = setrun()

    rundata.write()
