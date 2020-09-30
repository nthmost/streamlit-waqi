import pandas as pd

from math import sin, cos, sqrt, atan2, radians


# Time threshold in seconds for sensor reading freshness.
# (Discard any sensor reading less fresh than 10s. i.e. technically WACK!)
SENSOR_FRESHNESS_THRESHOLD = 10

# Which average to use to create US AQI.  Options: 10min_avg, 30min_avg... 
SENSOR_AVG_KEY = "10min_avg"

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




def calculate_usaqi(concentration, values):
    "Calculates USAQI given a pollutant concentration and a dict of AQI category values."
    ratio = ((values["i_high"] - values["i_low"]) / (values["c_high"] - values["c_low"]))
    cofactor = concentration - values["c_low"]
    return (ratio * cofactor) - values["i_low"]



def get_usaqi(ppm25avg):
    # https://cfpub.epa.gov/airnow/index.cfm?action=airnow.calculator
    # https://forum.airnowtech.org/t/the-aqi-equation/169    
    # https://en.wikipedia.org/wiki/Air_quality_index

    breakpoints = {1: {"i_high": 50, "i_low": 0, "c_high": 12, "c_low": 0}, 
        2: {"i_high": 100, "i_low": 51, "c_high": 35.4, "c_low": 12.1}, 
        3: {"i_high": 150, "i_low": 101, "c_high": 55.4, "c_low": 35.5}, 
        4: {"i_high": 200, "i_low": 151, "c_high": 150.4, "c_low": 55.5}, 
        5: {"i_high": 300, "i_low": 201, "c_high": 250.4, "c_low": 150.5}, 
        6: {"i_high": 400, "i_low": 301, "c_high": 350.4, "c_low": 250.5}, 
        7: {"i_high": 500, "i_low": 401, "c_high": 500.4, "c_low": 350.5}, 
    }


    # USAQI equation
    # I={\frac {I_{high}-I_{low}}{C_{high}-C_{low}}}(C-C_{low})+I_{low}

    for aqi_c, values in breakpoints.items():
        if ppm25avg <= values["c_high"]:
            if ppm25avg > values["c_low"]:
                return calculate_usaqi(ppm25avg, values)



def get_relevant_sensors(df, lat, lon, radius):
    # Apply distance function to dataframe
    df['dist']=list(map(lambda k: get_distance(df.loc[k]['lat'],df.loc[k]['lon'], lat, lon), df.index))

    df['usaqi']=list(map(lambda k: get_usaqi(df.loc[k][SENSOR_AVG_KEY]), df.index))

    # This will give all locations within radius of X km
    closest = df[df['dist'] < radius]

    # Only recent readings, please!
    recent = closest[closest['age'] < SENSOR_FRESHNESS_THRESHOLD]

    # We just want the "outside" ones.
    return recent[recent['location_type']=="outside"]


