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
DEFAULT_CONTAINERS_PER_ROW = 3
DEFAULT_RADIUS = 2
DEFAULT_LAT = 37.779310
DEFAULT_LON = -122.466370
DEFAULT_RELOAD_PERIOD = 60   # time in seconds for autoreloading sensors


# Every-Time Initialization

SENSORS = {}
WORLD_SENSORS = SensorList()
#all_useful_sensors_df = WORLD_SENSORS.to_dataframe("useful")
all_useful_sensors_df = WORLD_SENSORS.to_dataframe(sensor_filter='useful', channel='parent')
relevant_sensors = None

# SIDEBAR

with st.sidebar:
    st.title("AQI Microclimates")

    # reload_seconds = st.number_input(label="reload time (seconds)", value=DEFAULT_RELOAD_PERIOD, min_value=0, max_value=3600)

    st.subheader("Enter a location below")

    #TODO: get lat-long from address or map click (Leaflet?)
    #address = st.text_input(label="address")

    lat = st.number_input(label="latitude", value=DEFAULT_LAT)
    lon = st.number_input(label="longitude", value=DEFAULT_LON)

    st.write("Distance from epicenter in KM")
    radius = st.number_input(label="radius", value=DEFAULT_RADIUS)

    st.write("Set sensor circles per row")
    circles_per_row = st.number_input(label="circles per row", value=DEFAULT_CONTAINERS_PER_ROW, min_value=2, max_value=10)


# Fill the Sensor grid if we know where we live.
if lat and lon:
    relevant_sensors = get_relevant_sensors(all_useful_sensors_df, lat, lon, radius)
    SENSORS = relevant_sensors.to_dict("records")


# MAIN

st.title("SENSOR GRID")
#st.write("<hr />", unsafe_allow_html=True)

with st.beta_expander(label="Map of Nearby Sensors"):
    st.map(relevant_sensors)


# set up the layout grid
COLUMNS = st.beta_columns(circles_per_row)

# SENSOR GRID

container_x = 0
for idx in range(len(SENSORS)):
    sensor = SENSORS[idx]

    with COLUMNS[container_x]:
        st.write(sensor_div(sensor['usaqi']), unsafe_allow_html=True)
        st.write(sensor["name"])
        st.write("{:.2f} km".format(sensor["dist"]))

    if (idx % circles_per_row) == 0:
        container_x = 0
    else:
        container_x += 1


# RAW DATA

with st.collapsible_container(label="Raw Data"):
    st.write(relevant_sensors)

