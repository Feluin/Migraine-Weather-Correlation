import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from scipy import signal
from scipy.ndimage import shift
import numpy as np
import plotly.express as px

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "forecast_days": 16,
    "hourly": "surface_pressure"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()

hourly_surface_pressure = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
), "surface_pressure": hourly_surface_pressure}

hourly_dataframe = pd.DataFrame(data=hourly_data)
hourly_dataframe['MA'] = hourly_dataframe["surface_pressure"].rolling(window=15).mean()
maxima = signal.argrelextrema(hourly_dataframe['MA'].values, np.greater)[0]
minima = signal.argrelextrema(hourly_dataframe["MA"].values, np.less)[0]
if minima[0] < maxima[0]:
    maxima = shift(maxima, 1)

print(hourly_dataframe)

fig = px.line(hourly_dataframe, x="date", y="surface_pressure", title='surface_pressure')
fig.add_scatter(x=hourly_dataframe['date'], y=hourly_dataframe['MA'])
for i, idx in enumerate(minima):
    if len(maxima) <= i:
        continue
    maxim = hourly_dataframe.iloc[maxima[i]]
    minim = hourly_dataframe.iloc[minima[i]]
    loss = (minim["surface_pressure"] - maxim["surface_pressure"])
    if loss < -5:
        print(str(maxim["date"]) + " \t " + str(minim["date"]) + " \t " + str(
            (minim["surface_pressure"] - maxim["surface_pressure"])) + " \t " + str(
            maxim["surface_pressure"]) + " \t " + str(
            minim["surface_pressure"]))
        fig.add_vline(x=minim["date"])
fig.show()
