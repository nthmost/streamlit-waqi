from pwaqi import get_location_observation, findStationCodesByCity, get_station_observation

from datetime import datetime

"""
{'idx': 3900,
'city': {'geo': [37.76595, -122.39902],
'name': 'San Francisco-Arkansas Street, San Francisco, California',
'url': 'https://aqicn.org/city/california/san-francisco/san-francisco-arkansas-street'},
'aqi': 99,
'dominentpol': 'pm25',
'time': '2020-09-05 14:00:00',
'iaqi': [{'p': 'co', 'v': 5.5},
{'p': 'h', 'v': 40},
{'p': 'no2', 'v': 7.5},
{'p': 'o3', 'v': 50.7},
{'p': 'p', 'v': 1011.1},
{'p': 'pm25', 'v': 99},
{'p': 't', 'v': 30},
{'p': 'w', 'v': 4},
{'p': 'wg', 'v': 11}]}
"""

class Observation:

    def __init__(self, obs):
        self.idx = obs.get("idx", 0)
        self.city = obs.get("city", "")
        self.aqi = obs.get("aqi", 0)
        self.dominantpol = obs.get("dominantpol", "")
        self.time = obs.get("time", None)
        self.iaqi = obs.get("iaqi", [])
        _process_datetime()

    def _process_datetime()
        if self.time:
            self.time = datetime.strptime("%Y-%m-%d %H:%M:%D")
        else:
            self.time = datetime.now()




