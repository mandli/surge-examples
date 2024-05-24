
""" 
Set up the plot figures, axes, and items to be done for each frame.
This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""
import os
import io
import urllib.request

import numpy as np
import matplotlib

import matplotlib.pyplot as plt
import datetime

#from clawpack.geoclaw.util import fetch_noaa_tide_data
import clawpack.clawutil.data
import clawpack.amrclaw.data
import clawpack.geoclaw.data

import clawpack.geoclaw.surge.plot as surge
import clawpack.visclaw.gaugetools as gaugetools
 
import requests
import xml.etree.ElementTree as ET 

import urllib.parse


try:
    from setplotfg import setplotfg
except:
    setplotfg = None

def setplot(plotdata):
    r"""Setplot function for surge plotting"""
    

    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'binary'

    #fig_num_counter = surge.figure_counter()

    # Load data from output
    clawdata = clawpack.clawutil.data.ClawInputData(2)
    clawdata.read(os.path.join(plotdata.outdir,'claw.data'))
    physics = clawpack.geoclaw.data.GeoClawData()
    physics.read(os.path.join(plotdata.outdir,'geoclaw.data'))
    surge_data = clawpack.geoclaw.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir,'surge.data'))
    friction_data = clawpack.geoclaw.data.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir,'friction.data'))

    # Load storm track
    track = surge.track_data(os.path.join(plotdata.outdir,'fort.track'))

    # Calculate landfall time, off by a day, maybe leap year issue?
    landfall_dt = datetime.datetime(2011,8,27,7,30) - datetime.datetime(2011,1,1,0)
    landfall = (landfall_dt.days) * 24.0 * 60**2 + landfall_dt.seconds

    # Set afteraxes function
    surge_afteraxes = lambda cd: surge.surge_afteraxes(cd, 
                                        track, landfall, plot_direction=False)
    # Limits for plots
    full_xlimits = [clawdata.lower[0],clawdata.upper[0]]
    full_ylimits = [clawdata.lower[1],clawdata.upper[1]]
    full_shrink = 0.8
    carolinas_xlimits = [-79.5,-74.5]
    carolinas_ylimits = [32.8,36.3]
    carolinas_shrink = 1.0

    # Color limits
    surface_range = 3.0
    speed_range = 1.0
    # speed_range = 1.e-2

    xlimits = full_xlimits
    ylimits = full_ylimits
    eta = physics.sea_level
    if not isinstance(eta,list):
        eta = [eta]
    surface_limits = [eta[0]-surface_range,eta[0]+surface_range]
    speed_limits = [0.0,speed_range]
    
    wind_limits = [0,55]
    pressure_limits = [966,1013]
    friction_bounds = [0.01,0.04]
    vorticity_limits = [-1.e-2,1.e-2]

    def pcolor_afteraxes(current_data):
        surge_afteraxes(current_data)
        surge.gauge_locations(current_data)
    
    def contour_afteraxes(current_data):
        surge_afteraxes(current_data)

    
    # ==========================================================================
    # ==========================================================================
    #   Plot specifications
    # ==========================================================================
    # ==========================================================================

    # ========================================================================
    #  Surface Elevations - Entire Atlantic
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface - Atlantic',  
                                         figno=100)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes
    
    surge.add_surface_elevation(plotaxes,bounds=surface_limits,shrink=full_shrink)
    surge.add_land(plotaxes)


    # ========================================================================
    #  Water Speed - Entire Atlantic
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Currents - Atlantic',  
                                         figno=200)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = pcolor_afteraxes

    # Speed
    surge.add_speed(plotaxes,bounds=speed_limits,shrink=full_shrink)

    # Land
    surge.add_land(plotaxes)

    # ========================================================================
    #  Surface Elevations - North and South Carolina Area
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface - Carolinas',  
                                         figno=300)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = carolinas_xlimits
    plotaxes.ylimits = carolinas_ylimits
    def after_with_gauges(cd):
        surge_afteraxes(cd)
        surge.gauge_locations(cd)
    plotaxes.afteraxes = after_with_gauges
    
    surge.add_surface_elevation(plotaxes,bounds=surface_limits,shrink=carolinas_shrink)
    surge.add_land(plotaxes)

    # ========================================================================
    #  Currents Elevations - North and South Carolina Area
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Currents - Carolinas',  
                                         figno=400)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents'
    plotaxes.scaled = True
    plotaxes.xlimits = carolinas_xlimits
    plotaxes.ylimits = carolinas_ylimits
    def after_with_gauges(cd):
        surge_afteraxes(cd)
        surge.gauge_locations(cd)
    plotaxes.afteraxes = after_with_gauges
    
    surge.add_speed(plotaxes,bounds=speed_limits,shrink=carolinas_shrink)
    surge.add_land(plotaxes)


    # ========================================================================
    # Hurricane forcing - Entire Atlantic
    # ========================================================================
    # Friction field
    plotfigure = plotdata.new_plotfigure(name='Friction',
                                         figno=500)
    plotfigure.show = friction_data.variable_friction and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Manning's N Coefficients"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True

    surge.add_friction(plotaxes,bounds=friction_bounds)

    # Pressure field
    plotfigure = plotdata.new_plotfigure(name='Pressure',  
                                         figno=600)
    plotfigure.show = surge_data.pressure_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Pressure Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.add_pressure(plotaxes,bounds=pressure_limits)
    # add_pressure(plotaxes)
    surge.add_land(plotaxes)
    
    # Wind field
    plotfigure = plotdata.new_plotfigure(name='Wind Speed', 
                                         figno=700)
    plotfigure.show = surge_data.wind_forcing and True
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Wind Field"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    surge.add_wind(plotaxes,bounds=wind_limits,plot_type='imshow')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='contour')
    # add_wind(plotaxes,bounds=wind_limits,plot_type='quiver')
    surge.add_land(plotaxes)
    
    # Surge field
    plotfigure = plotdata.new_plotfigure(name='Surge Field', 
                                         figno=800)
    plotfigure.show = ((surge_data.wind_forcing or surge_data.pressure_forcing) 
                        and False)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Storm Surge Source Term S"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.pressure_field + 1
    plotitem.pcolor_cmap = plt.get_cmap('PuBu')
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1e-3
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.colorbar_label = "Source Strength"
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,0,0]
    
    surge.add_land(plotaxes)

    plotfigure = plotdata.new_plotfigure(name='Friction/Coriolis Source', 
                                         figno=900)
    plotfigure.show = False
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = full_xlimits
    plotaxes.ylimits = full_ylimits
    plotaxes.title = "Friction/Coriolis Source"
    plotaxes.afteraxes = surge_afteraxes
    plotaxes.scaled = True
    
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = surge.pressure_field + 2
    plotitem.pcolor_cmap = plt.get_cmap('PuBu')
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1e-3
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.colorbar_label = "Source Strength"
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,0,0]
    
    surge.add_land(plotaxes)

    # ==========================================================================
    #  Depth
    # ==========================================================================
    plotfigure = plotdata.new_plotfigure(name='Depth - Entire Domain', 
                                         figno=1000)
    plotfigure.show = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Topography'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.afteraxes = surge_afteraxes

    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = 0
    plotitem.imshow_cmin = 0
    plotitem.imshow_cmax = 200
    plotitem.imshow_cmap = plt.get_cmap("terrain")
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1,1,1,1,1,1,1]

    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface',   
                                         figno=250,type='each_gauge')
    plotfigure.show = True
    plotfigure.clf_each_gauge = True
 
    stations = [('8661070', 'Springmaid Pier, SC', 'NOAA', None),
                ('8658120', 'Wilmington, NC', 'NOAA', None),
                ('8658163', 'Wrightsville Beach, NC', 'NOAA', None),
                ('8656483', 'Beaufort, NC', 'NOAA', None),
                ('8654467', 'Hatteras, NC', 'NOAA', None),
                ('8652587', 'Oregon Inlet Marina, NC', 'NOAA', None),
                ('02084472', 'Pamlico River, NC', 'USGS', '00065'),
                ('02092576', 'Trent River, NC', 'USGS', '62620')]
  
    landfall_time = np.datetime64('2018-09-14T07:15')
    begin_date = datetime.datetime(2018, 9, 12 )
    end_date = datetime.datetime(2018, 9, 16) 
    
    # modified fetch_noaa_tide_data function for current NOAA formatting
    def fetch_noaa_tide_data(station, begin_date, end_date, time_zone='GMT',
                         datum='STND', units='metric', cache_dir=None,
                         verbose=True):
        """Fetch water levels and tide predictions at given NOAA tide station.
        
        The data is returned in 6 minute intervals between the specified begin and
        end dates/times.  A complete specification of the NOAA CO-OPS API for Data
        Retrieval used to fetch the data can be found at:
           
            https://tidesandcurrents.noaa.gov/api/
        
        By default, retrieved data is cached in the geoclaw scratch directory
        located at:
            
            $CLAW/geoclaw/scratch
        
        :Required Arguments:
        - station (string): 7 character station ID
        - begin_date (datetime): start of date/time range of retrieval
        - end_date (datetime): end of date/time range of retrieval
        
        :Optional Arguments:
        - time_zone (string): see NOAA API documentation for possible values
        - datum (string): see NOAA API documentation for possible values
        - units (string): see NOAA API documentation for possible values
        - cache_dir (string): alternative directory to use for caching data
        - verbose (bool): whether to output informational messages
        
        :Returns:
        - date_time (numpy.ndarray): times corresponding to retrieved data
        - water_level (numpy.ndarray): preliminary or verified water levels
        - prediction (numpy.ndarray): tide predictions
        """
        
        NOAA_API_URL = 'https://tidesandcurrents.noaa.gov/api/datagetter'
    
        # use geoclaw scratch directory for caching by default
        if cache_dir is None:
            if 'CLAW' not in os.environ:
                raise ValueError('CLAW environment variable not set')
            claw_dir = os.environ['CLAW']
            cache_dir = os.path.join(claw_dir, 'geoclaw', 'scratch')

        def fetch(product, expected_header, col_idx, col_types):
            noaa_params = get_noaa_params(product)
            cache_path = get_cache_path(product)

            # use cached data if available
            if os.path.exists(cache_path):
                if verbose:
                    print('Using cached {} data for station {}'.format(
                        product, station))
                return parse(cache_path, col_idx, col_types, header=True)

            # otherwise, retrieve data from NOAA and cache it
            if verbose:
                print('Fetching {} data from NOAA for station {}'.format(
                    product, station))
            full_url = '{}?{}'.format(NOAA_API_URL, urllib.request.urlencode(noaa_params))
            with urllib.request.urlopen(full_url) as response:
                text = response.read().decode('utf-8')
                with io.StringIO(text) as data:
                    # ensure that received header is correct
                    header = data.readline().strip()
                if header != expected_header or 'Error' in text:
                    # if not, response contains error message
                    raise ValueError(text)

                    # if there were no errors, then cache response
                    save_to_cache(cache_path, text)

                    return parse(data, col_idx, col_types, header=False)

        def get_noaa_params(product):
            noaa_date_fmt = '%Y%m%d %H:%M'
            noaa_params = {
                'product': product,
                'application': 'NOS.COOPS.TAC.WL',
                'format': 'csv',
                'station': station,
                'begin_date': begin_date.strftime(noaa_date_fmt),
                'end_date': end_date.strftime(noaa_date_fmt),
                'time_zone': time_zone,
                'datum': datum,
                'units': units
            }
            return noaa_params

        def get_cache_path(product):
            cache_date_fmt = '%Y%m%d%H%M'
            dates = '{}_{}'.format(begin_date.strftime(cache_date_fmt),
                                   end_date.strftime(cache_date_fmt))
            filename = '{}_{}_{}'.format(time_zone, datum, units)
            abs_cache_dir = os.path.abspath(cache_dir)
            return os.path.join(abs_cache_dir, product, station, dates, filename)

        def save_to_cache(cache_path, data):
            # make parent directories if they do not exist
            parent_dir = os.path.dirname(cache_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)

            # write data to cache file
            with open(cache_path, 'w') as cache_file:
                cache_file.write(data)

        def parse(data, col_idx, col_types, header):
            # read data into structured array, skipping header row if present
            a = np.genfromtxt(data, usecols=col_idx, dtype=col_types,
                                 skip_header=int(header), delimiter=',',
                                 missing_values='')

            # return tuple of columns
            return tuple(a[col] for col in a.dtype.names)

        # only need first two columns of data; first column contains date/time,
        # and second column contains corresponding value
        col_idx = (0, 1)
        col_types = 'datetime64[m], float'

        # fetch water levels and tide predictions
        date_time, water_level = fetch(
            'water_level', 'Date Time, Water Level, Sigma, O or I (for verified), F, R, L, Quality',
            col_idx, col_types)
        date_time2, prediction = fetch('predictions', 'Date Time, Prediction',
                                       col_idx, col_types)

        # ensure that date/time ranges are the same
        if not np.array_equal(date_time, date_time2):
            raise ValueError('Received data for different times')

        return date_time, water_level, prediction
  
    def fetch_usgs_gauge_data(station, begin_date, end_date, parameter, cache_dir=None, verbose=True):
    
        '''Fetch gauge water levels at given USGS site.

        More details about the USGS web service and parameter filters 
        can be found here: 
            
            https://waterservices.usgs.gov/rest/IV-Service.html

        A complete list of parameter codes and descriptions can be found
        here:
            
            https://help.waterdata.usgs.gov/parameter_cd?group_cd=PHY

        Retrieved data is cached in the Geoclaw scratch directory by default,
        located at:
            
            $CLAW/geoclaw/scratch

        :Required Arguments:
            - station (string): site ID (length may vary)
            - begin_date (datetime): start of date/time range of retrieval
            - end_date (datetime): end of date/time range of retrieval
            - parameter (string): 5-character parameter code
        
        :Optional Arguments:
            - cache_dir (string): alternative directory to use for caching data
            - verbose (bool): whether to ouput informational messages

        :Returns:
            - date_time (tuple): times corresponding to retrieved data
            - water_level (tuple): water level at each time
        '''

        feet2meters = lambda feet: feet * 0.3048

        #use geoclaw scratch directory for caching by default
        if cache_dir is None:
            if 'CLAW' not in os.environ:
                raise ValueError('CLAW environment variable not set')
            claw_dir = os.environ['CLAW']
            cache_dir = os.path.join(claw_dir, 'geoclaw', 'scratch')   

        def fetch(parameter):
            usgs_params = {
            'sites': station,
            'format': 'waterml,2.0',
            'startDT': begin_date.isoformat(),
            'endDT': end_date.isoformat(),
            'parameterCd': parameter # parameter code
            }
            
            cache_path = get_cache_path(parameter)
            
            # use cached data if available
            if os.path.exists(cache_path):
                if verbose:
                    print('Using cached {} data for station {}'.format(
                            parameter, station))
                return parse(cache_path)
            
            # otherwise, retrieve data from USGS and cache it
            if verbose:
                print('Fetching {} data from USGS for station {}'.format(
                        parameter, station))
            params = urllib.parse.urlencode(usgs_params)
            full_url = 'http://waterservices.usgs.gov/nwis/iv/?%s' % params
            
            # create response object from url 
            resp = requests.get(full_url)
            
            # check HTTP status code and raise exception if unsuccessful
            resp.raise_for_status()   
            
            xml_content = resp.content
            
            # cache response content
            save_to_cache(cache_path, xml_content)
            
            return parse(cache_path)
        
        def get_cache_path(parameter):
            cache_date_fmt = '%Y%m%d%H%M'
            filename = '{}_{}.xml'.format(begin_date.strftime(cache_date_fmt),
                                    end_date.strftime(cache_date_fmt))
            abs_cache_dir = os.path.abspath(cache_dir)

            return os.path.join(abs_cache_dir, 'USGS', parameter, station, filename)

        def save_to_cache(cache_path, data):
            # make parent directories if they do not exist
            parent_dir = os.path.dirname(cache_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)

            # write data to cache file
            with open(cache_path, 'wb') as cache_file:
                cache_file.write(data)
        
        def parse(data): 
            # create ElementTree object
            tree = ET.parse(data)

            namespaces = {'wm12': 'http://www.opengis.net/waterml/2.0'}

            # return root as Element object
            root = tree.getroot()

            times = []
            values = []
            
            # find data from subelements and store into lists
            for MeasurementTVP in root.findall('.//wm12:MeasurementTVP', namespaces):
                time = MeasurementTVP.find('wm12:time', namespaces).text
                date_time = np.datetime64(time[0:19])
                #seconds_rel_landfall = (date_time - landfall_time) / np.timedelta64(1, 's')
                times.append(date_time)
        
                value = MeasurementTVP.find('wm12:value', namespaces).text
                value_in_m = feet2meters(float(value))
                values.append(value_in_m)       
            
            return tuple(times), tuple(values)
        
        # fetch with parameter code for surface height
        date_time, water_level = fetch(parameter) 
        
        return date_time, water_level        
    
# need to uncomment this function if you want to compare with real data from NOAA/USGS
    def get_actual_water_levels(station_id, gauge_source, parameter_code):
        # Fetch water levels and tide predictions for given station
        if gauge_source == 'NOAA':
            date_time, water_level, tide = fetch_noaa_tide_data(station_id,
                    begin_date, end_date, datum='NAVD')
            # Subtract tide predictions from measured water levels
            water_level -= tide
        
        elif gauge_source == 'USGS':
            date_time, water_level = fetch_usgs_gauge_data(station_id, 
                    begin_date, end_date, parameter_code)
        
        # Calculate times relative to landfall
        seconds_rel_landfall = (date_time - landfall_time) / np.timedelta64(1, 's')

        return seconds_rel_landfall, water_level
 
    def gauge_afteraxes(cd):
        station_id, station_name, gauge_source, parameter_code = stations[cd.gaugeno-1]
# uncomment the next line to plot against real NOAA/USGS data
        seconds_rel_landfall, actual_level = get_actual_water_levels(station_id, gauge_source, parameter_code)

        axes = plt.gca()
        #surgeplot.plot_landfall_gauge(cd.gaugesoln, axes, landfall=landfall)
# uncomment the next line to plot against real NOAA/USGS data 
        axes.plot(seconds_rel_landfall, actual_level, 'g', label='Observed')
        
        # Fix up plot - in particular fix time labels
        axes.set_title(station_name)
        axes.set_xlabel('Seconds relative to landfall')
        axes.set_ylabel('Surface (m)')
        axes.set_ylim([0, 4])
        #axes.set_xticks([ days2seconds(-2), days2seconds(-1), 0, days2seconds(1)])
        #axes.set_xticklabels([r"$-3$", r"$-2$", r"$-1$", r"$0$", r"$1$"])
        axes.grid(True)
        plt.legend(loc="upper left")

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    try:
        plotaxes.xlimits = [clawdata.t0, clawdata.tfinal]
    except:
        pass
    plotaxes.ylimits = surface_limits
    plotaxes.title = 'Surface'
    plotaxes.afteraxes = gauge_afteraxes

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'
    
    #  ===================
    #  Gauge Location Plot
    #  ===================
    # Gauges 1-3
    def gauge_location_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[1,2,3],
                                        format_string='ko', add_labels=True)

    plotfigure = plotdata.new_plotfigure(name="Gauge Locations (1-3)")
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Gauge Locations (1-3)'
    plotaxes.scaled = True
    plotaxes.xlimits = [-78.9, -77.6]
    plotaxes.ylimits = [33.6, 34.4]
    plotaxes.afteraxes = gauge_location_afteraxes
    surge.add_surface_elevation(plotaxes, bounds=surface_limits)
    surge.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # Gauges 4-6
    def gauge_location_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[4,5,6],
                                        format_string='ko', add_labels=True)

    plotfigure = plotdata.new_plotfigure(name="Gauge Locations (4-6)")
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Gauge Locations (4-6)'
    plotaxes.scaled = True
    plotaxes.xlimits = [-76.85, -75.5]
    plotaxes.ylimits = [34.55, 35.9]
    plotaxes.afteraxes = gauge_location_afteraxes
    surge.add_surface_elevation(plotaxes, bounds=surface_limits)
    surge.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10

    # Gauges 7-8
    def gauge_location_afteraxes(cd):
        plt.subplots_adjust(left=0.12, bottom=0.06, right=0.97, top=0.97)
        surge_afteraxes(cd)
        gaugetools.plot_gauge_locations(cd.plotdata, gaugenos=[7,8],
                                        format_string='ko', add_labels=True)

    plotfigure = plotdata.new_plotfigure(name="Gauge Locations (7-8)")
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Gauge Locations (7-8)'
    plotaxes.scaled = True
    plotaxes.xlimits = [-77.3, -76.5]
    plotaxes.ylimits = [34.7, 35.65]
    plotaxes.afteraxes = gauge_location_afteraxes
    surge.add_surface_elevation(plotaxes, bounds=surface_limits)
    surge.add_land(plotaxes)
    plotaxes.plotitem_dict['surface'].amr_patchedges_show = [0] * 10
    plotaxes.plotitem_dict['land'].amr_patchedges_show = [0] * 10


    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

