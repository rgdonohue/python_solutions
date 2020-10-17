# import required libraries
import geopandas as gpd
import os

# import data
df_stormwater = gpd.read_file('./data/stormwater')

# open .prj file to extract known CRS info
with open('./data/stormwater/stormwater.prj') as f:
    wkt_def = f.read()

# define current CRS
df_stormwater.crs = wkt_def

# transform CRS to WGS84
df_stormwater_wgs84 = df_stormwater.to_crs("EPSG:4326")

# write output to GeoJSON file
df_stormwater_wgs84.to_file('./data/stormwater.json', driver='GeoJSON')

# write output to shapefile
os.mkdir('./data/stormwater_wgs84')
df_stormwater_wgs84.to_file('./data/stormwater_wgs84/stormwater_wgs84.shp')
