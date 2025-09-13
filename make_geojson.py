import os
import geopandas
import pandas as pd
from shapely.geometry import MultiPolygon

cwd = os.path.join(os.getcwd(), 'area_info')
folder_list = [file for file in os.listdir(cwd)]
shp_files = [os.path.join(cwd, folder, "TL_SCCO_SIG.shp") for folder in folder_list]

geodf = geopandas.GeoDataFrame()

for file in shp_files:
    temp = geopandas.read_file(file, encoding='cp949')
    geodf = pd.concat([geodf, temp], sort=False).reset_index(drop=True)

#지도 내에 작은 구역(섬이나, 아주 작은 구역들)들은 제외한 나머지들을 반환하는 함수
def filter_small_polygons(multi_polygon, threshold_area):
    filtered_list = []
    if type(multi_polygon) == MultiPolygon:
        for polygon in multi_polygon.geoms:
            if polygon.area >= threshold_area:
                filtered_list.append(polygon)
        return MultiPolygon(filtered_list)
    else:
        return multi_polygon


geodf['geometry'] = geodf['geometry'].apply(lambda x: filter_small_polygons(x,threshold_area=7000000))
geodf['geometry'] = geodf['geometry'].simplify(100)

geodf = geodf.set_crs(epsg=5179)
geodf = geodf.to_crs(epsg=4326)

geodf.to_file('법정구역_시군구.geojson', driver='GeoJSON')