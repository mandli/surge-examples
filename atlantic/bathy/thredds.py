#!/usr/bin/env python
# Script to download all .nc files from a THREDDS catalog directory
# Written by Sage 4/5/2016, revised 5/31/2018
  
from xml.dom import minidom
from urllib.request import urlopen
from urllib.request import urlretrieve
  
# Divide the url you get from the data portal into two parts
# Everything before "catalog/"
server_url = 'https://www.ngdc.noaa.gov/thredds/'
# Everything after "catalog/"
request_url = 'catalog/tiles/tiled_19as/'

   
def get_elements(url, tag_name, attribute_name):
  """Get elements from an XML file"""
  # usock = urllib2.urlopen(url)
  usock = urlopen(url)
  xmldoc = minidom.parse(usock)
  usock.close()
  tags = xmldoc.getElementsByTagName(tag_name)
  attributes=[]
  for tag in tags:
    attribute = tag.getAttribute(attribute_name)
    attributes.append(attribute)
  return attributes
 
def main():
  url = server_url + request_url + 'catalog.xml'
  print(url)
  catalog = get_elements(url,'dataset','urlPath')
  files=[]
  for citem in catalog:
    
    if (citem[:27]=='tiles/tiled_19as/ncei19_n40') or (citem[:27]=='tiles/tiled_19as/ncei19_n41') and (citem[-3:]=='.nc'):
      files.append(citem)
  count = 0
  for f in files:
    #if f== 'tiles/tiled_19as/ncei19_n40x75_w074x00_2015v1.nc' or f =='tiles/tiled_19as/ncei19_n40x75_w074x25_2015v1.nc' or f=='tiles/tiled_19as/ncei19_n40x75_w073x75_2015v1.nc':
     #   continue
    count +=1
    file_url = server_url + 'fileServer/' + f
    file_prefix = file_url.split('/')[-1][:-3]
    file_name = file_prefix + '.nc'
    print('Downloading file %d of %d' % (count,len(files)))
    print(file_name)
    a = urlretrieve(file_url,file_name)
    print(a)
 
# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
