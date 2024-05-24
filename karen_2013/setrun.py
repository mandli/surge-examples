# encoding: utf-8
"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
import datetime

import numpy as np

import clawpack.geoclaw.surge as surge

# Need to adjust the date a bit due to weirdness with leap year (I think)
karen_landfall = datetime.datetime(2013,10,5,0) - datetime.datetime(2013,1,1,0)

#                           days   s/hour    hours/day            
days2seconds = lambda days: days * 60.0**2 * 24.0
seconds2days = lambda seconds: seconds / (60.0**2 * 24.0)

#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

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
    clawdata.lower[0] = -99.0      # west longitude
    clawdata.upper[0] = -70.0      # east longitude

    clawdata.lower[1] = 8.0       # south latitude
    clawdata.upper[1] = 32.0      # north latitude

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
    clawdata.t0 = days2seconds(karen_landfall.days - 3) + karen_landfall.seconds
    # clawdata.t0 = days2seconds(ike_landfall.days - 1) + ike_landfall.seconds

    # Restart from checkpoint file of a previous run?
    # Note: If restarting, you must also change the Makefile to set:
    #    RESTART = True
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False               # True to restart from prior results
    clawdata.restart_file = 'fort.chk00006'  # File to use for restart data

    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        # clawdata.tfinal = days2seconds(date2days('2008091400'))
        clawdata.tfinal = days2seconds(karen_landfall.days + 0.75) + karen_landfall.seconds
        recurrence = 24
        clawdata.num_output_times = int((clawdata.tfinal - clawdata.t0) 
                                            * recurrence / (60**2 * 24))

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
    # Output the bathymetry, the friction, and the computed storm fields
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
    # clawdata.cfl_desired = 0.25
    # clawdata.cfl_max = 0.5

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 5000




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
        clawdata.checkpt_times = [0.1,0.15]

    elif clawdata.checkpt_style == 3:
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
    amrdata.refinement_ratios_x = [2,2,3,4,4,4]
    amrdata.refinement_ratios_y = [2,2,3,4,4,4]
    amrdata.refinement_ratios_t = [2,2,3,4,4,4]


    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center','capacity','yleft','center','center','center',
                         'center', 'center', 'center']


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

    # == setregions.data values ==
    regions = rundata.regiondata.regions
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]
    # Latex shelf
    regions.append([1, 3, rundata.clawdata.t0, rundata.clawdata.tfinal,
                                            -97.5, -88.5, 27.5, 30.5])

    # Galveston Sub-Domains
    # regions.append([1, 5, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                         -95.8666, -93.4, 28.63333, 30.2])
    # regions.append([1, 6, rundata.clawdata.t0, rundata.clawdata.tfinal,
    #                                         -95.3723, -94.5939, 29.2467, 29.9837])
    # # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal,
    # #                                             -95.25, -94.3, 28.85, 29.8])

    # # Galveston Channel Entrance (galveston_channel)
    # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                             -94.84, -94.70, 29.30, 29.40])
    # # Galveston area (galveston)
    # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                 -94.922600000000003, -94.825786176806162, 
    #                                              29.352,  29.394523768822882])
    # # Lower Galveston Bay channel (lower_galveston_bay)
    # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                 -94.903199999999998, -94.775835119593594, 
    #                                  29.383199999999999, 29.530588208444357])
    # # Middle Galveston Bay Channel (upper_galveston_bay)
    # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                 -94.959199999999996, -94.859496211934697, 
    #                                  29.517700000000001,  29.617610214127549])
    # # Upper Galveston bay channel (houston_channel_2)
    # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                 -95.048400000000001, -94.903076052178108, 
    #                                  29.602699999999999,  29.688573241894751])
    # # Lower Houston channel (houston_channel_3)
    # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                 -95.094899999999996, -94.892808885060177,
    #                                             29.6769,  29.832958103058733])

    # # Upper Houston channel (houston_harbor)
    # regions.append([1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                                 -95.320999999999998, -95.074527281677078,
    #                                  29.699999999999999,  29.830461271340102])

    # == setgauges.data values ==
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    # rundata.gaugedata.gauges.append([121, -94.70895, 29.2812, rundata.clawdata.t0, rundata.clawdata.tfinal])  
    # rundata.gaugedata.gauges.append([122, -94.38840, 29.4964, rundata.clawdata.t0, rundata.clawdata.tfinal])    
    # rundata.gaugedata.gauges.append([123, -94.12530, 29.5846, rundata.clawdata.t0, rundata.clawdata.tfinal]) 

    # Gauges from Ike AWR paper (2011 Dawson et al)
    rundata.gaugedata.gauges.append([1, -95.04, 29.07, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([2, -94.71, 29.28, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([3, -94.39, 29.49, rundata.clawdata.t0, rundata.clawdata.tfinal])
    rundata.gaugedata.gauges.append([4, -94.13, 29.58, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # rundata.gaugedata.gauges.append([5, -95.00, 29.70, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # rundata.gaugedata.gauges.append([6, -95.14, 29.74, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # rundata.gaugedata.gauges.append([7, -95.08, 29.55, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # rundata.gaugedata.gauges.append([8, -94.75, 29.76, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # rundata.gaugedata.gauges.append([9, -95.27, 29.72, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # rundata.gaugedata.gauges.append([10, -94.51, 29.52, rundata.clawdata.t0, rundata.clawdata.tfinal])
    
    # Stations from Andrew Kennedy
    # Station R - 82
    rundata.gaugedata.gauges.append([ord('R'),-97.1176, 27.6289, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # Station S - 83
    rundata.gaugedata.gauges.append([ord('S'),-96.55036666666666, 28.207733333333334, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # Station U - 85
    rundata.gaugedata.gauges.append([ord('U'),-95.75235, 28.62505, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # Station V - 86
    rundata.gaugedata.gauges.append([ord('V'),-95.31511666666667, 28.8704, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # Station W: Same as gauge 1
    # rundata.gaugedata.gauges.append([ord('W'),-95.03958333333334, 29.0714, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # Station X: Same as gauge 2 above
    # rundata.gaugedata.gauges.append([ord('X'),-94.70895, 29.281266666666667, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # Station Y: Same as gauge 3 above
    # rundata.gaugedata.gauges.append([ord('Y'),-94.3884, 29.496433333333332, rundata.clawdata.t0, rundata.clawdata.tfinal])
    # Station Z: Same as gauge 4 above
    # rundata.gaugedata.gauges.append([ord('Z'),-94.12533333333333, 29.584683333333334, rundata.clawdata.t0, rundata.clawdata.tfinal])

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------
    rundata = setgeo(rundata)

    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print "*** Error, this rundata has no geo_data attribute"
        raise AttributeError("Missing geo_data attribute")
       
    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2
    geo_data.earth_radius = 6367.5e3

    # == Forcing Options
    geo_data.coriolis_forcing = True
    geo_data.friction_forcing = True
    geo_data.manning_coefficient = 0.025 # Overridden below
    geo_data.friction_depth = 1e10

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.27  # Due to seasonal swelling of gulf
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
    topo_data.topofiles = []
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]
    # See regions for control over these regions, need better bathy data for the
    # smaller domains
    topo_data.topofiles.append([3, 1, 5, rundata.clawdata.t0, rundata.clawdata.tfinal, 
                              '../bathy/gulf_caribbean.tt3'])
    topo_data.topofiles.append([3, 1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal,
                              '../bathy/NewOrleans_3s.tt3'])
    # topo_data.topofiles.append([3, 1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal,
    #                           '../bathy/NOAA_Galveston_Houston.tt3'])
    # topo_data.topofiles.append([3, 1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal,
    #                           '../bathy/Galveston_DEM_1072/galveston_tx.asc'])
    # geodata.topofiles.append([3, 1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                           '../bathy/galveston_channel.tt3'])
    # geodata.topofiles.append([3, 1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                           '../bathy/houston_harbor.tt3'])
    # geodata.topofiles.append([3, 1, 7, rundata.clawdata.t0, rundata.clawdata.tfinal, 
    #                           '../bathy/houston_channel_3.tt3'])
    # geodata.topofiles.append([3, 1, 7, 0., 1.e10, \
    #                           '../bathy/houston_channel_2.tt3'])
    # geodata.topofiles.append([3, 1, 7, 0., 1.e10, \
    #                           '../bathy/galveston.tt3'])
    # geodata.topofiles.append([3, 1, 7, 0., 1.e10, \
    #                           '../bathy/lower_galveston_bay.tt3'])
    # geodata.topofiles.append([3, 1, 7, 0., 1.e10, \
    #                           '../bathy/upper_galveston_bay.tt3'])

    # == setdtopo.data values ==
    dtopo_data = rundata.dtopo_data
    dtopo_data.dtopofiles = []
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #   [topotype, minlevel,maxlevel,fname]

    # == setqinit.data values ==
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]

    # == setfixedgrids.data values ==
    rundata.fixed_grid_data.fixedgrids = []
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    # Set storm
    set_storm(rundata)

    # Set variable friction
    set_friction(rundata)

    return rundata
    # end of function setgeo
    # ----------------------


def set_storm(rundata):

    data = rundata.surge_data

    # Physics parameters
    data.rho_air = 1.15
    data.ambient_pressure = 101.3e3 # Nominal atmos pressure

    # Source term controls - These are currently not respected
    data.wind_forcing = True
    data.drag_law = 1
    data.pressure_forcing = True
    
    # Source term algorithm parameters
    # data.wind_tolerance = 1e-4
    # data.pressure_tolerance = 1e-4 # Pressure source term tolerance

    # AMR parameters
    data.wind_refine = [20.0,40.0,60.0] # m/s
    data.R_refine = [60.0e3,40e3,20e3]  # m
    
    # Storm parameters
    data.storm_type = 1 # Type of storm
    data.landfall = days2seconds(karen_landfall.days) + karen_landfall.seconds
    data.display_landfall_time = True

    # Storm type 1 - Idealized storm track
    data.storm_file = os.path.expandvars(os.path.join(os.getcwd(),'karen.storm'))

    return data


def set_friction(rundata):

    data = rundata.friction_data

    # Variable friction
    data.variable_friction = True

    # Region based friction
    # Entire domain
    data.friction_regions.append([rundata.clawdata.lower, 
                                  rundata.clawdata.upper,
                                  [np.infty,0.0,-np.infty],
                                  [0.030, 0.022]])

    # La-Tex Shelf
    data.friction_regions.append([(-98, 25.25), (-90, 30),
                                  [np.infty,-10.0,-200.0,-np.infty],
                                  [0.030, 0.012, 0.022]])

    return data


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    if len(sys.argv) == 2:
        rundata = setrun(sys.argv[1])
    else:
        rundata = setrun()

    rundata.write()
