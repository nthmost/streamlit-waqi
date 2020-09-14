# AQI Near Me

`streamlit run aqi_near_me.py`

## Air Quality Microclimates

I wanted a tablet-ready dashboard to see all of the relevant sensors to MY neighborhood, as well as sensors in places I might like to go to get fresher air (e.g. Ocean Beach).  A lot of AQI reports apply to the city as a whole as an average, and as we all know, San Francisco is anything but uniform in its weather patterns.  We have air quality microclimates too!
  
While I didn't get far enough in this hackathon to make a really NICE interface, I did get to play around with the Horizontal Layout demo so I could generate a "Sensor Grid" of circles.  The circles are filled from top-left to bottom-right in order of how close they are to the epicenter (lat/long).

## Qualifications for a RELEVANT Sensor

* Actually in my neighborhood (not an average for San Francisco!).

* A reasonable radius from my location (default 2km, configurable on the dashboard).

* Has reported something within the last 10 seconds (SF has over 6000 outdoor sensors, we can afford to be picky).

* Has ALL air quality measurements reporting (some sensors are missing some? so let's just drop them).


## Next Improvements

I would like to integrate <a href="https://discuss.streamlit.io/t/using-leaflet-instead-of-folium-in-streamlit-to-return-coordinates-on-map-click/4946/6">a Leaflet component started by andfanilo</a> to grab lat/long from user click.

After that, I'd like to generate a nice map with colored circles for each sensor location corresponding to the AQI colors.  Or maybe a heat map overlay using pydeck.
