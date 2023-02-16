
from pymongo import MongoClient
import pandas as pd
import time
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import geopandas as gpd
from dotenv import load_dotenv
import os
import requests





def get_offices_location (data):
    nested_data = []
    for item in data:
        name = item['name']
        for office in item['offices']:
            nested_data.append({
                'name': name,
                'office description': office['description'],
                'office latitude': office['latitude'],
                'office longitude': office['longitude']
            })
    df = pd.DataFrame(nested_data)
    return df

def load_cities(city_names):
    cities = {}
    for city_name in city_names:
        city_geo = gpd.read_file(f"Geojsons/{city_name}.geojson")
        cities[city_name.title()] = city_geo.geometry[0]
    return cities

def add_city_name(df, cities):
    city_names = []
    for _, row in df.iterrows():
        lat, lon = row['office latitude'], row['office longitude']
        point = gpd.points_from_xy([lon], [lat])
        for city_name, city_geometry in cities.items():
            if point.within(city_geometry)[0]:
                city_names.append(city_name)
                break
        else:
            city_names.append(None)
    df['city'] = city_names
    return df

def centroid_coordinates(df):
    centroid_lat = df["office latitude"].sum() / len(df)
    centroid_lon = df["office longitude"].sum() / len(df)
    return [round(centroid_lat, 4), round(centroid_lon, 4)]

def add_marker (name, color, icon_, coordinates, map):
    icon1 = Icon(
    color = color,
    opacity = 0.1,
    prefix = "fa", #font-awesome
    icon = icon_,
    icon_color = "white"
    )   
    marker_ = Marker(
    location = coordinates,
    tooltip = name,
    icon = icon1
    )
    marker_.add_to(map)
    return map

def mean_coordinates_raw (list_):
    x = 0
    y = 0
    for i in list_:
        x +=i[0]
        y +=i[1]
    x = x/len(list_)
    y = y/len(list_)

    return [round(x,4), round(y,4)]

def process_4sq_data(data):
    rows = []
    for result in data['results']:
        row = {
            'name': result['name'],
            'distance': result['distance'],
            'latitude': result['geocodes']['main']['latitude'],
            'longitude': result['geocodes']['main']['longitude'],
            'category_id': result['categories'][0]['id'],
            'category_name': result['categories'][0]['name']
        }
        rows.append(row)
    df = pd.DataFrame(rows).sort_values(by='distance', ascending=True)
    return df