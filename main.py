import requests
import json
import datetime
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

endpoint = 'http://api.openweathermap.org/geo/1.0/direct'

city = input('Enter city name: ')
countryCode = input('Country Code: ')
callAmount = input('Enter amount of api calls: ')

url = endpoint + '?q=' + city + ',' + countryCode + '&limit=' + callAmount + '&appid=' + config.api_key

res = requests.get(url)

data = res.json()

if data[0] != '404':
    print(data)

    latlon = data[0]

    lat = latlon['lat']
    lon = latlon['lon']

currWeatherURL = 'https://api.openweathermap.org/data/3.0/onecall?lat=' + str(lat) + '&lon=' + str(lon) + '&units=metric' + '&exclude=minutely,hourly,alerts' + '&appid=' + config.api_key

currWeatherRes = requests.get(currWeatherURL)

currWeatherData = currWeatherRes.json()

currWeatherDF = pd.DataFrame(currWeatherData['daily'])

currWeatherDF['dt'] = pd.to_datetime(currWeatherDF['dt'], unit='s').dt.date
currWeatherDF['sunrise'] = pd.to_datetime(currWeatherDF['sunrise'], unit='s').dt.strftime('%I:%M %p')
currWeatherDF['sunset'] = pd.to_datetime(currWeatherDF['sunset'], unit='s').dt.strftime('%I:%M %p')
currWeatherDF['moonrise'] = pd.to_datetime(currWeatherDF['moonrise'], unit='s').dt.strftime('%I:%M %p')
currWeatherDF['moonset'] = pd.to_datetime(currWeatherDF['moonset'], unit='s').dt.strftime('%I:%M %p')
currWeatherDF['moon_phase'] = currWeatherDF['moon_phase'].astype(float)
currWeatherDF['pop'] = currWeatherDF['pop'].astype(float) * 100
currWeatherDF['windspeed'] = currWeatherDF['wind_speed'].astype(float) * 3.6

topTempsExtr = currWeatherDF['temp'].apply(lambda x: x['max'])

topTempsDF = pd.DataFrame(topTempsExtr)
topTemps = topTempsExtr.sort_values(ascending=False)

mergeDFs = pd.merge(currWeatherDF, topTempsDF, left_index=True, right_index=True)

colList = currWeatherDF.columns.tolist()
mergedColList = mergeDFs.columns.tolist()

mergeDFs.rename(columns={'temp_y': 'temp_max'}, inplace=True)

sortedDFbyTemp = mergeDFs.sort_values(by='temp_max', ascending=False)

print(sortedDFbyTemp)