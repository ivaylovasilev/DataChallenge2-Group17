import geopandas as gpd
import pandas as pd
from pyproj import Transformer

# Load the GeoPackage file containing London Boroughs
file_path = r"C:\Users\20224781\Downloads\London_Boroughs.gpkg"
gdf = gpd.read_file(file_path)

# Compute the bounding box coordinates
gdf['min_x'] = gdf.bounds.minx
gdf['max_x'] = gdf.bounds.maxx
gdf['min_y'] = gdf.bounds.miny
gdf['max_y'] = gdf.bounds.maxy

# Define the projection transformation from UK National Grid to WGS84
transformer = Transformer.from_crs('epsg:27700', 'epsg:4326', always_xy=True)

def convert_coords(row):
    min_lon, min_lat = transformer.transform(row['min_x'], row['min_y'])
    max_lon, max_lat = transformer.transform(row['max_x'], row['max_y'])
    return pd.Series([min_lat, max_lat, min_lon, max_lon])

# Apply the coordinate conversion to each row
gdf[['min_lat', 'max_lat', 'min_lon', 'max_lon']] = gdf.apply(convert_coords, axis=1)


final_df = gdf[['name', 'min_lat', 'max_lat', 'min_lon', 'max_lon']]

# Save the DataFrame with latitude and longitude information
final_df.to_csv('lat-long_new.csv', index=False)

print("Conversion completed and data saved.")
