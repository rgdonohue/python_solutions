# import required libraries
import geopandas as gpd
import sys
import os
import shutil

class bcolors:
    STATUS = '\u001b[34;1m'
    OKGREEN = '\u001b[32;1m'
    ERROR = '\u001b[33;1m'
    FAIL = '\u001b[31;1m'
    ENDC = '\033[0m'

print(f'{bcolors.STATUS}Importing Shapefile data{bcolors.ENDC}')
try:
    # import data
    df_stormwater = gpd.read_file('./data/stormwater')
    print(f'{bcolors.OKGREEN}Data successfully read!{bcolors.ENDC}')
except:
    e = sys.exc_info()[0]
    print(f'{bcolors.ERROR}Error: %s' % e)
    sys.exit(f'{bcolors.FAIL}Shapefile not read. Exiting Script{bcolors.ENDC}')


print(f'{bcolors.STATUS}Reading CRS/proejction info ...{bcolors.ENDC}') 

try:
    # open .prj file to extract known CRS info
    with open('./data/stormwater/stormwater.prj') as f:
        wkt_def = f.read()
        print(f'{bcolors.OKGREEN}CRS info read:{bcolors.ENDC} %s' % wkt_def)
except:
    e = sys.exc_info()[0]
    print('Error: %s' % e)
    sys.exit('Projection info not retrieved')

    
print('transforming current dataset to WGS84')
# define current CRS
df_stormwater.crs = wkt_def

# transform CRS to WGS84
df_stormwater_wgs84 = df_stormwater.to_crs("EPSG:4326")

# write output to GeoJSON file (will overwrite GeoJSON)
print('writing new dataset to GeoJSON')
df_stormwater_wgs84.to_file('./data/stormwater.json', driver='GeoJSON')

print(f'{bcolors.STATUS}Writing new dataset to Shapefile.{bcolors.ENDC}')

# write output to shapefile
try:
    os.mkdir('./data/stormwater_wgs84')
except FileExistsError:
    print(f'{bcolors.ERROR}Shapefile directory exists. Now deleting directory and contents.{bcolors.ENDC}')
    shutil.rmtree('./data/stormwater_wgs84')
finally:
    os.mkdir('./data/stormwater_wgs84')
    df_stormwater_wgs84.to_file('./data/stormwater_wgs84/stormwater_wgs84.shp')
    print(f'{bcolors.OKGREEN}Shapefile successfully written to disk.{bcolors.ENDC}')
