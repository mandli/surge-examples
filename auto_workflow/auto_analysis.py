# Author: Max Zhao
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import clawpack.geoclaw.util
from math import sin, cos, sqrt, atan2, radians
import re
import logging
import os

def generate_time(storm, user_in):
    """
    @param: storm data in pandas series, landfall time in strings, format: date/month/year/hour
    @return: tuple of (s_date, e_date, delta_days, before_landfall, after_landfall, user_in)
    """ 
    try:

        data_start_y = int(storm[0][2][1:5])
        data_start_m = int(storm[0][2][5:7])
        data_start_d = int(storm[0][2][7:9])
        data_start_t = int(storm[0][2][9:])

        data_end_y = int(storm[len(storm)-1][2][1:5])
        data_end_m = int(storm[len(storm)-1][2][5:7])
        data_end_d = int(storm[len(storm)-1][2][7:9])
        data_end_t = int(storm[len(storm)-1][2][9:])

        l_date = l_date = pd.to_datetime(user_in)
        s_date = datetime(data_start_y, data_start_m, data_start_d, data_start_t)
        e_date = datetime(data_end_y, data_end_m, data_end_d, data_end_t)

        before_landfall = float((l_date - s_date).total_seconds()/86400)
        after_landfall = float((e_date - l_date).total_seconds()/86400)
        delta_days = float((e_date - s_date).total_seconds()/86400)

        return (s_date, e_date, delta_days, round(before_landfall,2), round(after_landfall,2), user_in)
    except:
        print('Something was wrong with data...')

def convert_km(lat_1, lng_1, lat_2, lng_2):
    """
    @param: two locations' coordinates in degree
    @return: distance between two locations in kilometers
    """ 
    radius = 6371.0

    d_lat = radians(lat_2) - radians(lat_1)
    d_lng = radians(lng_2) - radians(lng_1)
    
    var_1 = sin(d_lat / 2)**2 + cos(radians(lat_1)) * cos(radians(lat_2)) * sin(d_lng / 2)**2
    var_2 = 2 * atan2(sqrt(var_1), sqrt(1 - var_1))
   
    distance = radius * var_2

    return distance


def generate_gauge(metadata, storm):
    """
    @param: stations metadata, storm specific data
    @return: a dictionary of recommended gauges and their specific information. Gauge names are key and [station id, latitude, longitude, distance to storm eye] are values
    """ 
    location = []
    for i in range(len(storm)):
        lat_raw = re.findall(r'\d+',storm[i][6])
        lon_raw = re.findall(r'\d+',storm[i][7])
        lat = float(int(lat_raw[0])/10)
        lon = float(int(lon_raw[0])/10)
        location.append((lat, lon))
    

    gauge = {}
    for i in location:
        for j in range(len(metadata)):
            if (i[0]-0.5)<metadata['stations'][j]['lat']<(i[0]+0.5):
                if (-i[1]-1)<metadata['stations'][j]['lng']<(-i[1]+1):
                    if metadata['stations'][j]['name'] not in gauge:
                        gauge[metadata['stations'][j]['name']] = [metadata['stations'][j]['id'],
                        round(metadata['stations'][j]['lat'],2),round(metadata['stations'][j]['lng'],2), 
                        round(convert_km(metadata['stations'][j]['lat'], metadata['stations'][j]['lng'], i[0], -i[1]), 3)]
                    else:
                        if round(convert_km(metadata['stations'][j]['lat'], metadata['stations'][j]['lng'], i[0], -i[1]), 3) < gauge[metadata['stations'][j]['name']][3]:
                            gauge[metadata['stations'][j]['name']][3] = round(convert_km(metadata['stations'][j]['lat'], metadata['stations'][j]['lng'], i[0], -i[1]), 3)

            
    return gauge


def generate_significance(gauge, t0, tf):
    """
    @param: gauge information in dictionary format, storm data start time, storm data end time
    @return: a Pandas dataframe of each gauge's maximum surge level and distance to storm eye for comparison
    """ 
    max_surge = {}
    max_surge_list = []
    dis_list = []
    index_list = []
    for item in gauge:
        date_time, water_level, prediction = clawpack.geoclaw.util.fetch_noaa_tide_data(gauge[item][0], report_time[0], report_time[1])
        date_time, mean_water_level, mean_prediction = clawpack.geoclaw.util.fetch_noaa_tide_data(gauge[item][0], report_time[0], report_time[1], datum='MSL')
        max_surge_list.append(round(np.max(water_level - prediction) - np.mean(mean_water_level - mean_prediction), 3))
        max_surge[gauge[item][0]] = round(np.max(water_level - prediction) - np.mean(mean_water_level - mean_prediction), 3)
        dis_list.append(gauge[item][3])
        index_list.append(item)
    if len(max_surge_list) == 0:
        logging.info('===============Report Storm Significance===============')
        logging.info('No gauge was detected...')
        logging.info('=======================================================')
        return pd.DataFrame({'A' : []})
    else:
        raw_data = {'max surge': max_surge_list, 'distance': dis_list}
        data = pd.DataFrame.from_dict(raw_data, orient='index', columns = index_list)

    return data
 

def generate_storm_data(number):
    """
    @param: storm number
    @return: storm specific data, data in Pandas series format
    """ 
    storm = pd.DataFrame(pd.read_csv(str('http://ftp.nhc.noaa.gov/atcf/archive/2021/b'+number+'.dat.gz'),
            sep=':', header=None,))

    storm = storm[0].str.split(',')

    return storm

def generate_station_data():
    """
    @param: none
    @return: Metadata for NOAA water level gauges, data in Pandas dataframe format
    """ 
    station_meta = pd.read_json('https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json')

    return station_meta


if __name__ == "__main__":
    # User input storm number: al******
    number = input("Please input the storm number (format: al______): ")

# Create and configure logger in current working directory with name 'auto_analysis_stormnumber.log'
    logging.basicConfig(filename=str(os.path.dirname(__file__)+'/auto_analysis_'+str(number)+'.log'), 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 

    # Create an object 
    logger=logging.getLogger() 

    # Set the threshold of logger to DEBUG 
    logger.setLevel(logging.DEBUG) 


    storm = generate_storm_data(number)
    

    # Log storm time info
    user_in = str(input("Please input the landfall time, format: date/month/year/hour: "))
    report_time = generate_time(storm, user_in)
    logging.info('===============Report of Time===============')
    logging.info('\n')
    logging.info(f'Data for the storm is available starting at {report_time[0]}')
    logging.info('\n')
    logging.info(f'Data for the storm is NOT available after {report_time[1]}')
    logging.info('\n')
    logging.info(f'Landfall time you selected was {pd.to_datetime(report_time[5])}')
    logging.info('\n')
    logging.info(f'{report_time[2]} days are ready to be simulated')
    logging.info(f'{report_time[3]} days before landfall')
    logging.info(f'{report_time[4]} days after landfall')
    logging.info('\n')
    logging.info('============================================')

    logging.info('\n')

    station_meta = generate_station_data()
    
    gauge = generate_gauge(station_meta, storm)
    
    logging.info('==============Search for Gauge==============')
    for item in gauge:
        logging.info('\n')
        logging.info(f'{item}: Station ID: {gauge[item][0]}, Latitude: {gauge[item][1]}, Longitude: {gauge[item][2]}, Distance: {gauge[item][3]} kilometers')
        logging.info('\n')
    logging.info('==========================================')

    logging.info('\n')

    data = generate_significance(gauge, report_time[0], report_time[1])
    if data.empty:
        pass
    else:
        pd.set_option("display.max.columns", None)
        logging.info('\n \n ===========================Report Storm Significance===========================')
        logging.info(f'\n \n \n {data.head()}')
        logging.info('\n \n ===============================================================================')
    
