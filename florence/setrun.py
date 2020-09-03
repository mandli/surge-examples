
"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
import datetime

import numpy as np
from clawpack.geoclaw.surge.storm import Storm

import clawpack.clawutil as clawutil

from clawpack.geoclaw import topotools, marching_front
from numpy import ma # masked array

from clawpack.amrclaw import region_tools
from clawpack.amrclaw.data import FlagRegion


# September 14, 2018 at 7:15 am EDT
florence_landfall = datetime.datetime(2018, 9, 14, 7, 15) - datetime.datetime(2018, 9, 14, 7, 15)

#                           days   s/hour    hours/day            
days2seconds = lambda days: days * 60.0**2 * 24.0
seconds2days = lambda seconds: seconds / (60.0**2 * 24.0)

scratch_dir = os.path.join(os.environ["CLAW"], 'geoclaw', 'scratch')

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
    
    from clawpack.clawutil import data as clawdata 
    
    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'classic'"
    
    num_dim = 2
    rundata = clawdata.ClawRunData(claw_pkg, num_dim)
    
    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------

    # probdata = rundata.new_UserData(name='probdata',fname='setprob.data')

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #------------------------------------------------------------------

    clawdata = rundata.clawdata  # initialized when rundata instantiated
    
    # ---------------
    # Spatial domain:
    # ---------------
    
    # Number of space dimensions:
    clawdata.num_dim = num_dim
    
    # Lower and upper edge of computational domain:
    clawdata.lower[0] = -85 # west longitude
    clawdata.upper[0] = -65 # east longitude
    
    clawdata.lower[1] = 25 # south longitude
    clawdata.upper[1] = 40 # north longitude
    
    # Number of grid cells:
    degree_factor = 4 
    clawdata.num_cells[0] = int(clawdata.upper[0] - clawdata.lower[0]) * degree_factor
    clawdata.num_cells[1] = int(clawdata.upper[1] - clawdata.lower[1]) * degree_factor 
    
    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 9

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = days2seconds(-2) #start 2 days before landfall

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
    # -------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        #                 day     s/hour  hours/day
        
        clawdata.tfinal = days2seconds(1.5)

        # Output occurrence per day, 24 = every hour, 4 = every 6 hours
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
        

    clawdata.output_format = 'binary'      # 'ascii' or 'binary' or 'netcdf' 

    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'all' # could be list
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
    amrdata.amr_levels_max = 6

    # List of refinement ratios at each level (length at least mxnest-1)
    amrdata.refinement_ratios_x = [2,2,2,6,8,10,8]
    amrdata.refinement_ratios_y = [2,2,2,6,8,10,8]
    amrdata.refinement_ratios_t = [2,2,2,6,8,10,8]


    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center','capacity','yleft','center','center','center',
                         'center', 'center', 'center']



    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 4

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
    # Wilmington gauge
    regions.append([5,6,days2seconds(-2), days2seconds(1.5),-78.1,-77.8,33.9,34.4])
    # Pamlico gauge
    regions.append([5,6,days2seconds(-2), days2seconds(1.5),-77.15,-76.6,35.2,35.6])
    # Trent gauge
    regions.append([5,6,days2seconds(-0.5), days2seconds(1),-77.2,-76.6,34.7,35.2])

    # append as many flagregions as desired to this list:
    flagregions = rundata.flagregiondata.flagregions 

    flagregion = FlagRegion(num_dim=2)
    flagregion.name = 'Region_Coast_NC'
    flagregion.minlevel = 3
    flagregion.maxlevel = 5
    flagregion.t1 = days2seconds(-2)
    flagregion.t2 = days2seconds(1.5)
    flagregion.spatial_region_type = 2  # Ruled Rectangle
    flagregion.spatial_region_file = os.path.abspath('RuledRectangle_Coast_NC.data')
    flagregions.append(flagregion) 

    flagregion = FlagRegion(num_dim=2)
    flagregion.name = 'Region_Coast_SC'
    flagregion.minlevel = 3
    flagregion.maxlevel = 5
    flagregion.t1 = days2seconds(-1)
    flagregion.t2 = days2seconds(1.5)
    flagregion.spatial_region_type = 2  # Ruled Rectangle
    flagregion.spatial_region_file = os.path.abspath('RuledRectangle_Coast_SC.data')
    flagregions.append(flagregion) 

    flagregion = FlagRegion(num_dim=2)
    flagregion.name = 'Islands_NC'
    flagregion.minlevel = 5
    flagregion.maxlevel = 7
    flagregion.t1 = days2seconds(-1)
    flagregion.t2 = days2seconds(1)
    flagregion.spatial_region_type = 2  # Ruled Rectangle
    flagregion.spatial_region_file = os.path.abspath('RuledRectangle_NCIslands.data')
    flagregions.append(flagregion)

    # make Ruled Rectangle flagregions
    topo_path = os.path.join(scratch_dir, 'atlantic_1min.tt3')
    topo = topotools.Topography()
    topo.read(topo_path)
    
    # make RuledRectangle_Coast_NC.data:
    filter_region = (-79, -75, 33.3, 37)
    topo = topo.crop(filter_region) 
    # specify a Ruled Rectangle the flagregion should lie in
    rrect = region_tools.RuledRectangle()
    rrect.ixy = 'x'
    rrect.s = np.array([-78.,-77,-76.5,-75.3])
    rrect.lower = -131*np.ones(rrect.s.shape)
    rrect.upper = np.array([34.3,35,35.5,35.7])
    rrect.method = 1 
    
    # Start with a mask defined by the ruled rectangle `rrect` defined above:
    mask_out = rrect.mask_outside(topo.X, topo.Y)
    # select onshore points within 2 grip points of shore:
    pts_chosen_Zabove0 = marching_front.select_by_flooding(topo.Z, mask=mask_out, 
                                                       prev_pts_chosen=None, 
                                                       Z1=0, Z2=1e6, max_iters=2)
    # select offshore points down to 700 m depth:
    pts_chosen_Zbelow0 = marching_front.select_by_flooding(topo.Z, mask=None, 
                                                       prev_pts_chosen=None, 
                                                       Z1=0, Z2=-700., max_iters=None)
    # buffer offshore points with another 10 grid cells:
    pts_chosen_Zbelow0 = marching_front.select_by_flooding(topo.Z, mask=None, 
                                                       prev_pts_chosen=pts_chosen_Zbelow0, 
                                                       Z1=0, Z2=-5000., max_iters=10)

    # Take the intersection of the two sets of points selected above:
    nearshore_pts = np.where(pts_chosen_Zabove0+pts_chosen_Zbelow0 == 2, 1, 0)
    print('Number of nearshore points: %i' % nearshore_pts.sum())

    rr = region_tools.ruledrectangle_covering_selected_points(topo.X, topo.Y,
                                                          nearshore_pts, ixy='y', method=0,
                                                          verbose=True)
    # make .data file to use as a flagregion
    rr_name = 'RuledRectangle_Coast_NC'
    rr.write(rr_name + '.data')
    
    # make RuledRectangle_Coast_SC.data:
    filter_region = (-82, -77.5, 32, 34.5)
    topo = topo.crop(filter_region)
    #Specify a RuledRectangle the flagregion should lie in:
    rrect = region_tools.RuledRectangle()
    rrect.ixy = 'x' 
    rrect.s = np.array([-79.5,-79,-78.9,-77.8])
    rrect.lower = -131*np.ones(rrect.s.shape)
    rrect.upper = np.array([33.2,33.8,34,34])
    rrect.method = 1

    # Start with a mask defined by the ruled rectangle `rrect` defined above:
    mask_out = rrect.mask_outside(topo.X, topo.Y)

    # select onshore points within 3 grip points of shore:
    pts_chosen_Zabove0 = marching_front.select_by_flooding(topo.Z, mask=mask_out, 
                                                       prev_pts_chosen=None, 
                                                       Z1=0, Z2=1e6, max_iters=3)
    # select offshore points within 40 grip points of shore:
    pts_chosen_Zbelow0 = marching_front.select_by_flooding(topo.Z, mask=None, 
                                                       prev_pts_chosen=None, 
                                                       Z1=0, Z2=-500., max_iters=40)
    # buffer offshore points with another 10 grid cells:
    pts_chosen_Zbelow0 = marching_front.select_by_flooding(topo.Z, mask=None, 
                                                       prev_pts_chosen=pts_chosen_Zbelow0, 
                                                       Z1=0, Z2=-5000., max_iters=10)

    # Take the intersection of the two sets of points selected above:
    nearshore_pts = np.where(pts_chosen_Zabove0+pts_chosen_Zbelow0 == 2, 1, 0)
    print('Number of nearshore points: %i' % nearshore_pts.sum())

    rr = region_tools.ruledrectangle_covering_selected_points(topo.X, topo.Y,
                                                          nearshore_pts, ixy='y', method=0,
                                                          verbose=True)
    # make .data file to use as a flagregion
    rr_name = 'RuledRectangle_Coast_SC'
    rr.write(rr_name + '.data')

    # make RuledRectangle_NCIslands.data:
    rr = region_tools.RuledRectangle()
    rr.ixy = 1  # so s refers to x, lower & upper are limits in y
    rr.s = np.array([-76.27,-75.7,-75.56,-75.55,-75.42])
    rr.lower = np.array([34.9,35.1,35.17,35.18,35.25])
    rr.upper = np.array([35.02,35.3,35.6,35.77,35.75])
    rr.method = 1
    # make .data file to use as a flagregion
    rr_name = 'RuledRectangle_NCIslands'
    rr.write(rr_name + '.data')
    
    # == setgauges.data values ==
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    # Springmaid Pier gauge
    rundata.gaugedata.gauges.append([1,-78.85,33.68,clawdata.t0,clawdata.tfinal])
    # Wilmington gauge
    rundata.gaugedata.gauges.append([2,-77.95,34.27,clawdata.t0,clawdata.tfinal])
    # Wrightsville Beach gauge
    rundata.gaugedata.gauges.append([3,-77.80,34.18,clawdata.t0,clawdata.tfinal])
    # Beaufort gauge
    rundata.gaugedata.gauges.append([4,-76.65,34.7,clawdata.t0,clawdata.tfinal])
    # Hatteras gauge
    rundata.gaugedata.gauges.append([5,-75.70,35.25,clawdata.t0,clawdata.tfinal])
    # Oregon Inlet Marina gauge
    rundata.gaugedata.gauges.append([6,-75.57,35.78,clawdata.t0,clawdata.tfinal])
    # Pamlico River gauge
    rundata.gaugedata.gauges.append([7,-77.04,35.525,clawdata.t0,clawdata.tfinal])
    # Trent River gauge
    rundata.gaugedata.gauges.append([8,-76.96,35.03,clawdata.t0,clawdata.tfinal])

    # Force the gauges to also record the wind and pressure fields
    #rundata.gaugedata.aux_out_fields = [4, 5, 6]
    
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
        print("*** Error, this rundata has no geodata attribute")
        raise AttributeError("Missing geodata attribute")
       
    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2
    geo_data.earth_radius = 6367.5e3
    geo_data.rho_air = 1.15
    geo_data.ambient_pressure = 101.3e3 # Nominal atmos pressure

    # == Forcing Options
    geo_data.coriolis_forcing = True
    geo_data.friction_forcing = True
    geo_data.manning_coefficient = 0.025 # Overridden below
    geo_data.friction_depth = 1e10

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.28  # Due to seasonal swelling of gulf
    geo_data.dry_tolerance = 1.e-2

    # Refinement Criteria
    refine_data = rundata.refinement_data
    # refine_data.wave_tolerance = 1.0
    refine_data.wave_tolerance = 0.5
    # refine_data.speed_tolerance = [0.25,0.5,1.0,2.0,3.0,4.0]
    # refine_data.speed_tolerance = [0.5,1.0,1.5,2.0,2.5,3.0]
    refine_data.speed_tolerance = [1.0,2.0,3.0,4.0]
    refine_data.deep_depth = 1e6
    refine_data.max_level_deep = 4
    refine_data.variable_dt_refinement_ratios = True
    
    # == settopo.data values ==
    topo_data = rundata.topo_data
    topo_data.topofiles = []
    # for topography, append lines of the form
    #   [topotype, minlevel, maxlevel, t1, t2, fname]
    topo_path = os.path.join('..', 'bathy')
    topo_data.topofiles.append([3, 1, 5, rundata.clawdata.t0, rundata.clawdata.tfinal, os.path.join(topo_path, 'atlantic_1min.tt3')])
    
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
    data.storm_specification_type = "holland80" # Type of storm
    data.display_landfall_time = True

    # Storm type 1 - Idealized storm track
    data.storm_file = os.path.expandvars(os.path.join(os.getcwd(), 'florence.storm'))
    # Convert ATCF data to GeoClaw format
    clawutil.data.get_remote_file('http://ftp.nhc.noaa.gov/atcf/archive/2018/bal062018.dat.gz')
    atcf_path = os.path.join(scratch_dir, 'bal062018.dat')
    florence = Storm(path=atcf_path, file_format="ATCF")
    
    florence.time_offset = datetime.datetime(2018,9,14,7,15)
    florence.write(data.storm_file, file_format="geoclaw")

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
                                  [0.050, 0.025]])

    return data



if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    if len(sys.argv) == 2:
        rundata = setrun(sys.argv[1])
    else:
        rundata = setrun()

    rundata.write()



