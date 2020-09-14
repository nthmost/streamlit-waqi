import os

from purpleair.network import SensorList
from purpleair.sensor import Sensor

from df_math import get_relevant_sensors
from sensor_styling import sensor_div


DEFAULT_LAT = 37.78
DEFAULT_LON = -122.47
DEFAULT_RADIUS = 2

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

all_useful_sensors_df = WORLD_SENSORS.to_dataframe("useful")

SENSORS = get_relevant_sensors(all_useful_sensors_df, 
                    DEFAULT_LAT, DEFAULT_LON, 
                    DEFAULT_RADIUS).to_dict("records")


# MAIN

print("SENSOR GRID")

# SENSOR GRID

for idx in range(len(SENSORS)):
    sensor = SENSORS[idx]
    print(sensor["name"])
    print(sensor[SENSOR_AVG_KEY])

    print(sensor_div(sensor[SENSOR_AVG_KEY]))

