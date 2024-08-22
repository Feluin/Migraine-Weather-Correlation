import numpy as np
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from scipy import signal
from scipy.ndimage import shift

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below

url = "https://api.open-meteo.com/v1/forecast"


def getData(lat, long, start, end):
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": start,
        "end_date": end,
        "hourly": "surface_pressure"
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_surface_pressure = hourly.Variables(0).ValuesAsNumpy()
    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "surface_pressure": hourly_surface_pressure.astype(float)}
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe['MA'] = hourly_dataframe["surface_pressure"].rolling(window=15).mean()
    maxima = signal.argrelextrema(hourly_dataframe['MA'].values, np.greater)[0]
    minima = signal.argrelextrema(hourly_dataframe["MA"].values, np.less)[0]
    results = []
    if minima[0] < maxima[0]:
        maxima = shift(maxima, 1)
    for i, idx in enumerate(minima):
        if len(maxima) <= i:
            continue
        maxim = hourly_dataframe.iloc[maxima[i]]
        minim = hourly_dataframe.iloc[minima[i]]
        loss = (minim["surface_pressure"] - maxim["surface_pressure"])
        res={
            "loss": loss,
            "minima": minim.to_dict(),
            "maxima": maxim.to_dict()
        }
        results.append(res)

    return results
