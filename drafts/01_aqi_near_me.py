import streamlit as st

import os


# CONFIGURATION 
CONTAINERS_PER_ROW = 3
NUM_ROWS = 2
ALPHABET = "ABCD"


# One-time initialization
ALL_WORLD_SENSOR_DATA_PATH = "all_world_sensors.json"
WORLD_SENSORS = None

if os.path.exists(ALL_WORLD_SENSOR_DATA_FILENAME):
    WORLD_SENSORS = SensorList(local_data_path=ALL_WORLD_SENSOR_DATA_PATH)
else:
    WORLD_SENSORS = SensorList()
    WORLD_SENSORS.write_to_disk(ALL_WORLD_SENSOR_DATA_PATH)


# INITIALIZATION

SENSORS = []

# Pre-initialize empty containers
CONTAINERS = [[]]
for y in range(0, NUM_ROWS):
    for x in range(0, CONTAINERS_PER_ROW)
        CONTAINERS[x][y] = 



#SIDEBAR

st.sidebar.title("AQI Microclimates")

st.sidebar.subheader("Reloads all sensor data every 60 seconds")

st.sidebar.subheader("Enter a location below")

address = st.sidebar.text_input(label="address")

#TODO: get lat-long from address

lat = st.sidebar.number_input(label="latitude")
lng = st.sidebar.number_input(label="longitude")

#TODO: parse latlong for format / correctness 

# st.sidebar.write("Distance from epicenter in miles")
# radius = st.sidebar.number_input(label="radius")

# MAIN

st.title("SENSOR GRID")
st.write("<hr />", unsafe_allow_html=True)


#TODO: Fill sensors, sort by distance from epicenter.


# SENSOR GRID

SENSORS = [(145, "nearest"), (98, "second"), (125, "third"), (98, "fourth")]


for sensor in SENSORS:
    c = st.container()
    
