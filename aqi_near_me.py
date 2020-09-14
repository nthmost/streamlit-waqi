import os

import requests
import streamlit as st
import pandas as pd
import numpy as np

from purpleair.network import SensorList
from purpleair.sensor import Sensor

from sensor_styling import sensor_div
from df_math import get_relevant_sensors


# CONFIGURATION 
CONTAINERS_PER_ROW = 3
NUM_ROWS = 2
DEFAULT_RADIUS = 2
DEFAULT_LAT = 37.779310
DEFAULT_LON = -122.466370
SENSOR_AVG_KEY = "30min_avg"


# One-time initialization from Purple Air (This file is ~12MB)
ALL_WORLD_SENSOR_DATA_PATH = "all_world_sensors.json"
WORLD_SENSORS = None

if os.path.exists(ALL_WORLD_SENSOR_DATA_PATH):
    WORLD_SENSORS = SensorList(local_data_path=ALL_WORLD_SENSOR_DATA_PATH)
else:
    WORLD_SENSORS = SensorList()
    WORLD_SENSORS.write_to_disk(ALL_WORLD_SENSOR_DATA_PATH)


# Every-Time Initialization

SENSORS = {}
all_useful_sensors_df = WORLD_SENSORS.to_dataframe("useful")
relevant_sensors = None

# SIDEBAR

with st.sidebar:
    st.title("AQI Microclimates")
    st.subheader("Enter a location below")

    #TODO: get lat-long from address or map click (Leaflet?)
    #address = st.text_input(label="address")

    lat = st.number_input(label="latitude", value=DEFAULT_LAT)
    lon = st.number_input(label="longitude", value=DEFAULT_LON)

    st.write("Distance from epicenter in KM")
    radius = st.number_input(label="radius", value=DEFAULT_RADIUS)


# Fill the Sensor grid if we know where we live.
if lat and lon:
    relevant_sensors = get_relevant_sensors(all_useful_sensors_df, lat, lon, radius)
    SENSORS = relevant_sensors.to_dict("records")


st.title("SENSOR GRID")
#st.write("<hr />", unsafe_allow_html=True)


with st.collapsible_container(label="map"):
    st.map(relevant_sensors)


    #st.write(pdk.Deck(
    #    map_style="mapbox://styles/mapbox/light-v9",
    #    initial_view_state={
    #        "latitude": lat,
    #        "longitude": lon,
    #        "zoom": 11,
    #        "pitch": 50,
    #        },
    #    ))


# MAIN

# set up the layout grid
COLUMNS = st.columns(CONTAINERS_PER_ROW)

# SENSOR GRID

container_x = 0
for idx in range(len(SENSORS)):
    sensor = SENSORS[idx]

    with COLUMNS[container_x]:
        st.write(sensor_div(sensor[SENSOR_AVG_KEY]), unsafe_allow_html=True)
        st.write(sensor["name"])

    if (idx % CONTAINERS_PER_ROW) == 0:
        container_x = 0
    else:
        container_x += 1


