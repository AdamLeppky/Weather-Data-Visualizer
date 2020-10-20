
import requests
import pandas as pd
import json
import numpy as np
from datetime import datetime

# Tutorial Link: "https://towardsdatascience.com/getting-weather-data-in-3-easy-steps-8dc10cc5c859"

TOKEN = 'WMctgGJzgLAyBxhnMwCifSuBrKmqwYCD'
STATION_ID = 'GHCND:USW00014971'


def main():
    dates_temp = []
    dates_prcp = []
    temps = []
    prcp = []

    # for each year from 2014-2020 ...
    for year in range(2015, 2021):
        year = str(year)
        print('working on year ' + year)

        # make the api call
        r = requests.get(
            'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&limit=1000&stationid=GHCND:USW00023129&startdate=' + year + '-01-01&enddate=' + year + '-12-31',
            headers={'token': TOKEN})
        # load the api response as a json
        d = json.loads(r.text)
        # get all items in the response which are average temperature readings
        avg_temps = [item for item in d['results'] if item['datatype'] == 'TAVG']
        # get the date field from all average temperature readings
        dates_temp += [item['date'] for item in avg_temps]
        # get the actual average temperature from all average temperature readings
        temps += [item['value'] for item in avg_temps]

        # initialize dataframe
        df_temp = pd.DataFrame()

        # populate date and average temperature fields (cast string date to datetime and convert temperature from tenths of Celsius to Fahrenheit)
        df_temp['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_temp]
        df_temp['avgTemp'] = [float(v) / 10.0 * 1.8 + 32 for v in temps]


if __name__ == '__main__':
    main()
