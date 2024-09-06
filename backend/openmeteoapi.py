import numpy as np
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from scipy import signal
from scipy.ndimage import shift
from datetime import date, timedelta, datetime
import json

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below

url = "https://api.open-meteo.com/v1/forecast"
historicalUrl = "https://archive-api.open-meteo.com/v1/archive"


def getAll(lat, long, start, end):
    return analyze(getAllData(lat, long, start, end))


def getAllData(lat, long, start: str, end: str):
    prev = date.today() - timedelta(days=5)
    enddate = datetime.fromisoformat(end.replace("Z", "")).date()
    startdate = datetime.fromisoformat(start.replace("Z", "")).date()
    if enddate <= prev:
        return request(lat, long, startdate, enddate, historicalUrl)
    else:
        if prev < startdate:
            return request(lat, long, startdate, enddate, url)
        else:
            pre = request(lat, long, startdate, prev, historicalUrl)
            new = request(lat, long, prev, enddate, url)
            return pre.merge(new, "outer")


def request(lat, long, start: date, end: date, url) -> pd.DataFrame:
    if end > date.today() + timedelta(days=15):
        end = date.today() + timedelta(days=15)
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
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
    return pd.DataFrame(data=hourly_data)


def analyze(hourly_dataframe):
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
        res = {
            "loss": loss,
            "minima": json.loads(minim.to_json()),
            "maxima": json.loads(maxim.to_json())
        }
        results.append(res)

    return results
