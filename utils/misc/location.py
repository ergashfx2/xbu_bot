import pandas as pd
from math import radians, sin, cos, sqrt, atan2

from utils.db_api import db


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371 
    return r * c

def get_closest_location(current_lat, current_lon):
    locations = db.select_location()
    df = pd.DataFrame(locations, columns=['bxm', 'viloyat', 'tuman', 'ish_kunlari','nomi','coordinates'])
    df[['Latitude', 'Longitude',"Nothing","nothing"]] = df['coordinates'].str.split(',', expand=True)
    df['Latitude'] = df['Latitude'].str.strip()
    df['Longitude'] = df['Longitude'].str.strip()
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    df['Distance'] = df.apply(lambda row: haversine(current_lat, current_lon, row['Latitude'], row['Longitude']), axis=1)
    closest_location = df.loc[df['Distance'].idxmin()]
    return closest_location[['bxm', 'viloyat', 'tuman', 'ish_kunlari', 'nomi', 'coordinates', 'Distance']].tolist()




