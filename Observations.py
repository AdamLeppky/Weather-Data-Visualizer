
from noaa_sdk import noaa  # https://github.com/paulokuong/noaa
from datetime import datetime


def to_datetime(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S+00:00')


def to_fahrenheit(temperature):
    return (temperature * 9/5) + 32


class Observations:
    def __init__(self, postal_code, country_code, start, end):
        self.postal_code = postal_code
        self.country_code = country_code
        self.start = start
        self.end = end
        self.observations = [x for x in noaa.NOAA().get_observations(postal_code, country_code, start=start)]
        self.temperatures = None

    def get_temperatures(self):
        if self.temperatures is None:
            self.temperatures = {'timestamps': [to_datetime(x['timestamp']) for x in self.observations if x['temperature']['value'] is not None],
                                 'temperatures': [to_fahrenheit(x['temperature']['value']) for x in self.observations if x['temperature']['value'] is not None]}
        return self.temperatures
