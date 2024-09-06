import zoneinfo
from datetime import datetime

import icalendar
from icalendar import Calendar, Event

from backend.openmeteoapi import getAll

data = getAll(lat=49.40768, long=8.69079, start="2024-01-01", end="2024-09-17")

cal = Calendar()
for x in data:

    if x["loss"] < -2:
        event = Event()
        event.add('summary', x["loss"])
        event.add('dtstart', datetime.fromtimestamp(x["maxima"]['date'] / 1e3))
        event.add('dtend', datetime.fromtimestamp(x["minima"]['date'] / 1e3))
        event.add('dtstamp', datetime.fromtimestamp(x["minima"]['date'] / 1e3))
        cal.add_component(event)

with open("test.ics", mode="w") as f:
    print(cal.to_ical().decode('utf-8'))
    f.writelines(cal.to_ical().decode('utf-8'))
