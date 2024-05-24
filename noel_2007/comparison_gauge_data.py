#!/usr/bin/env python
# coding: utf-8

# In[31]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import urllib.request

## convert time relative to landfall day
def landfallTimeConvert(str):
        
    hours = (int(str[11:13]) + (int(str[14:])/60))/24
    
    if(str[5:7] == "10"):
        rel = int(str[8:10]) - 29
        rel += hours
        return rel
    if(str[5:7] == "11"):
        rel = int(str[8:10]) + 2
        rel += hours
        return rel 
    
## download NOAA water level data
url_verified = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?'               'begin_date=20071026&end_date=20071103&station=8723214&prod'               'uct=water_level&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

url_predicted = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'                '?begin_date=20071026&end_date=20071103&station=8723214&pr'                'oduct=predictions&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

urllib.request.urlretrieve(url_verified,'virginiakey_florida_verified_water_level_noaa.csv')
urllib.request.urlretrieve(url_predicted,'virginiakey_florida_predicted_water_level_noaa.csv')
        
## read data of Virginia Key water level
vkwl_ver = pd.read_csv('virginiakey_florida_verified_water_level_noaa.csv')
vkwl_pre = pd.read_csv('virginiakey_florida_predicted_water_level_noaa.csv')

vkwl_ver["Difference (m)"] = (vkwl_ver[' Water Level'] - vkwl_pre[' Prediction'])*0.3048

## changing date relative to landfall time
vkwl_ver["Datetime"] = vkwl_ver['Date Time']
vkwl_ver["Datetime"] = vkwl_ver["Datetime"].apply(landfallTimeConvert)

gauge_data_1 = vkwl_ver[["Difference (m)", "Datetime"]].copy()


# In[32]:


## download NOAA water level data
url_verified = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?'               'begin_date=20071026&end_date=20071103&station=8724580&prod'               'uct=water_level&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

url_predicted = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'                '?begin_date=20071026&end_date=20071103&station=8724580&pr'                'oduct=predictions&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

urllib.request.urlretrieve(url_verified,'key_west_verified_water_level_noaa.csv')
urllib.request.urlretrieve(url_predicted,'key_west_predicted_water_level_noaa.csv')

## read data of Key West water level
kwwl_ver = pd.read_csv('key_west_verified_water_level_noaa.csv')
kwwl_pred = pd.read_csv('key_west_predicted_water_level_noaa.csv')

kwwl_ver["Difference (m)"] = (kwwl_ver[' Water Level'] - kwwl_pred[' Prediction'])*0.3048

## changing date relative to landfall time
kwwl_ver["Datetime"] = kwwl_ver['Date Time']
kwwl_ver["Datetime"] = kwwl_ver["Datetime"].apply(landfallTimeConvert)


gauge_data_2 = kwwl_ver[["Difference (m)", "Datetime"]].copy()


# In[33]:


## download NOAA water level data
url_verified = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?'               'begin_date=20071026&end_date=20071103&station=9759938&prod'               'uct=water_level&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

url_predicted = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'                '?begin_date=20071026&end_date=20071103&station=9759938&pr'                'oduct=predictions&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

urllib.request.urlretrieve(url_verified,'mona_island_puerto_rico_verified_water_level_noaa.csv')
urllib.request.urlretrieve(url_predicted,'mona_island_puerto_rico_predicted_water_level_noaa.csv')

## read data of mona island water level
prwl_ver = pd.read_csv('mona_island_puerto_rico_verified_water_level_noaa.csv')
prwl_pre = pd.read_csv('mona_island_puerto_rico_predicted_water_level_noaa.csv')

prwl_ver["Difference (m)"] = (prwl_ver[' Water Level'] - prwl_pre[' Prediction'])*0.3048

## changing date relative to landfall time
prwl_ver["Datetime"] = prwl_ver['Date Time']
prwl_ver["Datetime"] = prwl_ver["Datetime"].apply(landfallTimeConvert)

gauge_data_3 = prwl_ver[["Difference (m)", "Datetime"]].copy()


# In[34]:


## download NOAA water level data
url_verified = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?'               'begin_date=20071026&end_date=20071103&station=9759110&prod'               'uct=water_level&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

url_predicted = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'                '?begin_date=20071026&end_date=20071103&station=9759110&pr'                'oduct=predictions&datum=mllw&units=english&time_zone=gmt&application=web_services&format=csv'

urllib.request.urlretrieve(url_verified,'magueyes_island_puerto_rico_verified_water_level_noaa.csv')
urllib.request.urlretrieve(url_predicted,'magueyes_island_puerto_rico_predicted_water_level_noaa.csv')

## read data of magueyes island water level
miwl_ver = pd.read_csv('magueyes_island_puerto_rico_verified_water_level_noaa.csv')
miwl_pre = pd.read_csv('magueyes_island_puerto_rico_predicted_water_level_noaa.csv')

miwl_ver["Difference (m)"] = (miwl_ver[' Water Level'] - miwl_pre[' Prediction'])*0.3048

## changing date relative to landfall time
miwl_ver["Datetime"] = miwl_ver['Date Time']
miwl_ver["Datetime"] = miwl_ver["Datetime"].apply(landfallTimeConvert)

gauge_data_4 = miwl_ver[["Difference (m)", "Datetime"]].copy()


# In[35]:


# save data as a text file for GeoClaw

np.savetxt('gauge_data_1.txt', gauge_data_1.values)
np.savetxt('gauge_data_2.txt', gauge_data_2.values)
np.savetxt('gauge_data_3.txt', gauge_data_3.values)
np.savetxt('gauge_data_4.txt', gauge_data_4.values)


# In[ ]:




