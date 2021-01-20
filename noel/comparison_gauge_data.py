#!/usr/bin/env python
# coding: utf-8

# In[10]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

## convert time relative to landfall day
def landfallTimeConvert(str):
        
    hours = (int(str[10:12]) + (int(str[13:])/60))/24
    
    if(str[5:7] == "10"):
        rel = int(str[8:10]) - 29
        rel += hours
        return rel
    if(str[5:7] == "11"):
        rel = int(str[8:10]) + 2
        rel += hours
        return rel
        

## read data of Virginia Key water level
fwl = pd.read_csv("virginiakey_biscaynebay_florida_water_level_noaa.csv")
fwl["Difference (m)"] = (fwl["Verified (ft)"] - fwl["Predicted (ft)"])*0.3048
fwl["Verified (m)"] = fwl["Verified (ft)"]*0.3048

## changing date relative to landfall time
fwl["Datetime"] = fwl["Date"]+fwl["Time (LST/LDT)"]
fwl["Datetime"] = fwl["Datetime"].apply(landfallTimeConvert)

gauge_data_1 = fwl[["Difference (m)", "Datetime"]].copy()


# In[11]:


## read data of Key West water level
kwwl = pd.read_csv("key_west_water_level_noaa.csv")
kwwl["Difference (m)"] = (kwwl["Verified (ft)"] - kwwl["Predicted (ft)"])*0.3048
kwwl["Verified (m)"] = kwwl["Verified (ft)"]*0.3048


## changing date to relative to landfall time
kwwl["Datetime"] = kwwl["Date"]+kwwl["Time (GMT)"]
kwwl["Datetime"] = kwwl["Datetime"].apply(landfallTimeConvert)

gauge_data_2 = kwwl[["Difference (m)", "Datetime"]].copy()


# In[12]:


## read data of mona island water level
prwl = pd.read_csv("mona_island_puerto_rico_water_level_noaa.csv")
prwl["Difference (m)"] = (prwl["Verified (ft)"] - prwl["Predicted (ft)"])*0.3048
prwl["Verified (m)"] = prwl["Verified (ft)"]*0.3048


## changing date to relative to landfall time
prwl["Datetime"] = prwl["Date"]+prwl["Time (LST/LDT)"]
prwl["Datetime"] = prwl["Datetime"].apply(landfallTimeConvert)

gauge_data_3 = prwl[["Difference (m)", "Datetime"]].copy()


# In[13]:


## read data of magueyes island water level
miwl = pd.read_csv("magueyes_island_puerto_rico_water_level_noaa.csv")
miwl["Difference (m)"] = (miwl["Verified (ft)"] - miwl["Predicted (ft)"])*0.3048
miwl["Verified (m)"] = miwl["Verified (ft)"]*0.3048


## changing date to relative to landfall time
miwl["Datetime"] = miwl["Date"]+miwl["Time (GMT)"]
miwl["Datetime"] = miwl["Datetime"].apply(landfallTimeConvert)

gauge_data_4 = miwl[["Difference (m)", "Datetime"]].copy()


# In[8]:


# save data as a text file for GeoClaw

np.savetxt('gauge_data_1.txt', gauge_data_1.values)
np.savetxt('gauge_data_2.txt', gauge_data_2.values)
np.savetxt('gauge_data_3.txt', gauge_data_3.values)
np.savetxt('gauge_data_4.txt', gauge_data_4.values)

