import pandas as pd
from math import radians, sin, cos, sqrt, atan2

from utils.db_api import db


def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371  # Radius of earth in kilometers
    return r * c

def get_closest_location(current_lat, current_lon):
    locations = db.select_location()

    # Create a DataFrame
    df = pd.DataFrame(locations, columns=['Manzil', 'Ish kunlari', 'Telefon', 'LatLon'])

    # Split 'LatLon' into 'Latitude' and 'Longitude'
    df[['Latitude', 'Longitude']] = df['LatLon'].str.split(',', expand=True)

    # Convert 'Latitude' and 'Longitude' to numeric values
    df['Latitude'] = pd.to_numeric(df['Latitude'])
    df['Longitude'] = pd.to_numeric(df['Longitude'])

    # Calculate the distance using the Haversine formula
    df['Distance'] = df.apply(lambda row: haversine(current_lat, current_lon, row['Latitude'], row['Longitude']), axis=1)

    # Find the row with the minimum distance
    closest_location = df.loc[df['Distance'].idxmin()]

    # Return the relevant values as a list
    return closest_location[['Manzil', 'Ish kunlari', 'Telefon', 'LatLon', 'Distance', 'Latitude', 'Longitude']].tolist()

