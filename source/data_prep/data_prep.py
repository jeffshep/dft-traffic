import json
import os

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, MultiPolygon, Feature, Polygon
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point
from pandas import DataFrame

def point_in_ward():
    ward_data = read_ward_data()    

    # geometry = [Point(xy) for xy in zip(data.longitude, data.latitude)]
    # df = data.drop(['longitude', 'latitude'], axis=1)
    # gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
    # print(gdf.head())

    # path = [os.path.dirname(__file__), 'static', 'dft_traffic_counts_aadf_by_direction.geojson']
    # file_path = os.path.join(*path)
    # gdf.to_file(file_path, driver='GeoJSON')

    print('Getting ward data')
    ward_path = [os.path.dirname(__file__), 'static', 'Wards_May_2021_UK_BFE.geojson']
    ward_file_path = os.path.join(*ward_path)
    ward_gdf = read_file(ward_file_path)

    print('Getting road data')
    road_path = [os.path.dirname(__file__), 'static', 'dft_traffic_counts_aadf_by_direction.geojson']
    road_file_path = os.path.join(*road_path)
    road_gdf = read_file(road_file_path)

    road_sindex = road_gdf.sindex
    for feature in ward_data["features"]:
        ward_id = feature["properties"]["OBJECTID"]
        print (f'Processing {ward_id}')

        queried_ward = ward_gdf.loc[ward_gdf['OBJECTID'] == ward_id]
        bounds = list(queried_ward.bounds.values[0])

        point_candidate_idx = list(road_sindex.intersection(bounds))
        point_candidates = road_gdf.loc[point_candidate_idx]

        final_selection = point_candidates.loc[point_candidates.intersects(queried_ward['geometry'].values[0])]

        print('Writing file')
        path = [os.path.dirname(__file__), 'ward_data', f'{ward_id}.geojson']
        file_path = os.path.join(*path)
        try:            
            final_selection.to_file(file_path, driver='GeoJSON')    
        except ValueError:
            with open(file_path, 'w') as f:
                json.dump({}, f)

def read_ward_data():
    path = [os.path.dirname(__file__), 'static', 'Wards_May_2021_UK_BFE.geojson']
    file_path = os.path.join(*path)
    ward_file = open(file_path)
    return json.load(ward_file)

point_in_ward()                