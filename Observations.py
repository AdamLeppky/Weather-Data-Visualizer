
from noaa_sdk import noaa  # https://github.com/paulokuong/noaa
from datetime import datetime
from preconditions import preconditions


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
        self.observations = [x for x in noaa.NOAA().get_observations(postal_code, country_code, start=start, end=end)]
        self.temperatures = None
        self.max_temperature_last_24_hours = None
        self.values = {}

    @preconditions(lambda value_key: value_key in ['windSpeed', 'temperature', 'precipitationLast6Hours', 'relativeHumidity', 'windDirection', 'seaLevelPressure', 'precipitationLastHour', 'dewpoint', 'windGust', 'maxTemperatureLast24Hours', 'windChill', 'barometricPressure', 'elevation', 'precipitationLast3Hours', 'visibility', 'heatIndex'])
    def get_values_by_key(self, value_key):
        if value_key not in self.values:
            timestamps = [to_datetime(x['timestamp']) for x in self.observations if x[value_key]['value'] is not None]
            values = [x[value_key]['value'] for x in self.observations if x[value_key]['value'] is not None]
            self.values[value_key] = {'timestamps': timestamps, 'values': values, 'unit_code': self.observations[0][value_key]['unitCode'].strip('unit:')}
        return self.values[value_key]
