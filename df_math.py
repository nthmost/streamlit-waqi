import pandas as pd

from math import sin, cos, sqrt, atan2, radians


# Time threshold in seconds for sensor reading freshness.
# (Discard any sensor reading less fresh than 10s. i.e. technically WACK!)
SENSOR_FRESHNESS_THRESHOLD = 10

#Distance function between two lat/lon
#https://stackoverflow.com/questions/58548566/selecting-rows-in-geopandas-or-pandas-based-on-latitude-longitude-and-radius
def get_distance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_relevant_sensors(df):
    # Apply distance function to dataframe
    df['dist']=list(map(lambda k: get_distance(df.loc[k]['lat'],df.loc[k]['lon'], lat, lon), df.index))

    # This will give all locations within radius of X km
    closest = df[df['dist'] < radius]

    # Only recent readings, please!
    recent = closest[closest['age'] < SENSOR_FRESHNESS_THRESHOLD]

    # We just want the "outside" ones.
    return recent[recent['location_type']=="outside"]



