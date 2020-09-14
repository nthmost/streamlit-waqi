import streamlit as st

from purpleair.network import SensorList
import requests

from math import sin, cos, sqrt, atan2, radians
import os


MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN")
SENSOR_DIV_TEMPLATE = '<div style="%s"><h1>%i</h1></div>'

# huge thanks to https://developer.mozilla.org/en-US/docs/Learn/CSS/Howto/create_fancy_boxes
CIRCLE_DIV = "text-align: center; padding: 1.5em; border: 0.5em solid black; width: 10em; height: 10em; border-radius: 100%;"

GREEN_CIRCLE = CIRCLE_DIV + "background-color: #16e031"
YELLOW_CIRCLE = CIRCLE_DIV + "background-color: #e0de3a"
ORANGE_CIRCLE = CIRCLE_DIV + "background-color: #d49528"
RED_CIRCLE = CIRCLE_DIV + "background-color: #e33c22"
PURPLE_CIRCLE = CIRCLE_DIV + "background-color: #6c2b8f"

# CONFIGURATION 
CONTAINERS_PER_ROW = 3
NUM_ROWS = 2
ALPHABET = "ABCD"


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



def get_latlong_from_address(address):
    address = address.replace(" ", "+")
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s' % address)
    return response.json()['results'][0]['geometry']['location']


# One-time initialization
ALL_WORLD_SENSOR_DATA_PATH = "all_world_sensors.json"
WORLD_SENSORS = None

if os.path.exists(ALL_WORLD_SENSOR_DATA_PATH):
    WORLD_SENSORS = SensorList(local_data_path=ALL_WORLD_SENSOR_DATA_PATH)
else:
    WORLD_SENSORS = SensorList()
    WORLD_SENSORS.write_to_disk(ALL_WORLD_SENSOR_DATA_PATH)


# Every-Time Initialization

SENSORS = []
df = WORLD_SENSORS.to_dataframe("useful")

#SIDEBAR

with st.sidebar:
    st.title("AQI Microclimates")
    st.subheader("Reloads all sensor data every 60 seconds")
    st.subheader("Enter a location below")

    #TODO: get lat-long from address
    address = st.text_input(label="address")

    lat = st.number_input(label="latitude")
    lng = st.number_input(label="longitude")

    st.write("Distance from epicenter in KM")
    radius = st.number_input(label="radius", value=10)


if address:
    print(get_latlong_from_address(address))



# Fill the Sensor grid if we know where we live.
if lat and lng:
    #Apply distance function to dataframe
    df['dist']=list(map(lambda k: get_distance(df.loc[k]['lat'],df.loc[k]['lon'], lat, lng), df.index))

    #This will give all locations within radius of X km
    closest = df[df['dist'] < radius]

    # Only recent readings, please!
    recent = closest[closest['age'] < 10]

    #We just want the "outside" ones.
    print(recent[recent['location_type']=="outside"])


# MAIN

st.title("SENSOR GRID")
st.write("<hr />", unsafe_allow_html=True)

# set up the layout grid
COLUMNS = st.columns(CONTAINERS_PER_ROW)

#for item in COLUMNS:
#   print(item._get_coordinates())


#TODO: Fill sensors, sort by distance from epicenter.


def sensor_div(reading):
    if reading < 50:
        # good
        return SENSOR_DIV_TEMPLATE % (GREEN_CIRCLE, reading)
    elif (reading >= 50) and (reading < 100):
        # moderate
        return SENSOR_DIV_TEMPLATE % (YELLOW_CIRCLE, reading)
    elif (reading >= 100) and (reading < 150):
        # bad
        return SENSOR_DIV_TEMPLATE % (ORANGE_CIRCLE, reading)
    elif (reading >= 150) and (reading < 200):
        # real bad
        return SENSOR_DIV_TEMPLATE % (RED_CIRCLE, reading)
    elif (reading >= 200) and (reading < 250):
        # real real bad
        return SENSOR_DIV_TEMPLATE % (PURPLE_CIRCLE, reading)
    elif (reading >= 250) and (reading < 300):
        # yikes
        return SENSOR_DIV_TEMPLATE % (PURPLE_CIRCLE, reading)
    else:
        # nightmarish hellscape
        return SENSOR_DIV_TEMPLATE % (PURPLE_CIRCLE, reading)


# SENSOR GRID

SENSORS = [(145, "nearest"), (98, "second"), (125, "third"), (98, "fourth")]

container_x = 0
for idx in range(len(SENSORS)):
    sensor = SENSORS[idx]

    with COLUMNS[container_x]:
        #st.header(sensor[0])
        #st.write(sensor[1])
        st.write(sensor_div(sensor[0]), unsafe_allow_html=True)
        st.write(sensor[1])


    if (idx % CONTAINERS_PER_ROW) == 0:
        container_x = 0
    else:
        container_x += 1
 
