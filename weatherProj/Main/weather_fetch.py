import requests
import datetime
from datetime import datetime
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from opencage.geocoder import OpenCageGeocode

#used to fetch weather data from openweather api
class currentWeather:
    def __init__(self):
        pass
    
    # this function is used to gte the location data based on city, country code and call amount
    @staticmethod
    def get_location_data(city, countryCode, callAmount):
        endpoint = 'http://api.openweathermap.org/geo/1.0/direct'
        url = f"{endpoint}?q={city},{countryCode}&limit={callAmount}&appid={config.openweather_api_key}"
        res = requests.get(url)
        data = res.json()
        return data
    
    # this function is used to get the current weather data based on lat and lon values
    @staticmethod
    def get_current_weather_data(lat, lon):
        currWeatherURL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly,alerts&appid={config.openweather_api_key}"
        currWeatherRes = requests.get(currWeatherURL)
        currWeatherData = currWeatherRes.json()
        return currWeatherData
    
    # this function is used to process the current weather data and return a dataframe
    @staticmethod
    def process_weather_data(currWeatherData):
        currWeatherDF = pd.DataFrame(currWeatherData['daily'])
        currWeatherDF['dt'] = pd.to_datetime(currWeatherDF['dt'], unit='s').dt.date
        currWeatherDF['sunrise'] = pd.to_datetime(currWeatherDF['sunrise'], unit='s').dt.strftime('%I:%M %p')
        currWeatherDF['sunset'] = pd.to_datetime(currWeatherDF['sunset'], unit='s').dt.strftime('%I:%M %p')
        currWeatherDF['moonrise'] = pd.to_datetime(currWeatherDF['moonrise'], unit='s').dt.strftime('%I:%M %p')
        currWeatherDF['moonset'] = pd.to_datetime(currWeatherDF['moonset'], unit='s').dt.strftime('%I:%M %p')
        currWeatherDF['moon_phase'] = currWeatherDF['moon_phase'].astype(float)
        currWeatherDF['pop'] = currWeatherDF['pop'].astype(float) * 100
        currWeatherDF['windspeed'] = currWeatherDF['wind_speed'].astype(float)
        currWeatherDF['weather_description'] = currWeatherDF['weather'].apply(lambda x: x[0]['description']).astype(str)        
        #print(currWeatherDF.columns.to_list())
        return currWeatherDF

#unused class, maybe will have use in the future. but does the same as above but for historical data
class historicalWeather:
    @staticmethod
    def get_location(city, countryCode, callamount):
        endpoint = 'http://api.openweathermap.org/geo/1.0/direct'
        url = f"{endpoint}?q={city},{countryCode}&limit={callamount}&appid={config.openweather_api_key}"
        res = requests.get(url)
        data = res.json()
        return data
    @staticmethod
    def get_historical_data(geoLat, geoLon, realTime):
        date_str = datetime.strptime(realTime, "%d/%m/%Y")
        unixTime = int(time.mktime(date_str.timetuple()))
        endpoint = f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={geoLat}&lon={geoLon}&dt={unixTime}&appid={config.openweather_api_key}'
        timeRes = requests.get(endpoint)
        historyData = timeRes.json()
        #print(historyData)
        
        # csv_columns = historyData.values()        |
        # csv_name = 'historyData.csv'              |
        # try:                                      |
        #     with open(csv_name, 'w') as csvfile:  | - Used to export historyData values to csv
        #         write = csv.writer(csvfile)       |
        #         write.writerow(csv_columns)       |
        # except IOError:                           |
        #     print("I/O error")                    |

        return historyData
    @staticmethod
    def process_historical_data(historyData):
        histweatherDF = pd.DataFrame.from_dict(historyData['data'])
        histweatherDF['dt'] = pd.to_datetime(histweatherDF['dt'], unit='s').dt.date
        histweatherDF['sunrise'] = pd.to_datetime(histweatherDF['sunrise'], unit='s').dt.strftime('%I:%M %p')
        histweatherDF['sunset'] = pd.to_datetime(histweatherDF['sunset'], unit='s').dt.strftime('%I:%M %p')
        histweatherDF['feels_like'] = histweatherDF['feels_like'].astype(float)
        histweatherDF['wind_speed'] = histweatherDF['wind_speed'].astype(float)
        histweatherDF['weather_description'] = histweatherDF['weather'].apply(lambda x: x[0]['description']).astype(str)
        #print(histweatherDF.columns.to_list())
        return histweatherDF

# this function is used to fetch the weather data based on the city and country code.
def fetch_weather_data(choice, city, countryCode, callAmount, realTime = None):
    if choice == "1": 
        location_data = currentWeather.get_location_data(city, countryCode, callAmount) # get location data from function and assign to var
        if location_data[0] != '404':
            latlon = location_data[0]
            lat = latlon['lat']
            lon = latlon['lon']
            currWeatherData = currentWeather.get_current_weather_data(lat, lon) # get current weather data from function and assign to var
            currWeatherDF = currentWeather.process_weather_data(currWeatherData) # use process function assign to var
            return (
                'currWeatherDF', currWeatherDF
            )
        
    #same as above but for historical data
    elif choice == "2":
        if realTime is None:
            raise ValueError("realTime cannot be None")
        historicalWeather_data = historicalWeather.get_location(city, countryCode, callAmount)
        if  historicalWeather_data[0] != '404':
            geocoder = OpenCageGeocode(config.opencage_api_key)
            results = geocoder.geocode(f'{city}', limit=callAmount)

            if results and len(results):
                geoLat = results[0]['geometry']['lat']
                geoLon = results[0]['geometry']['lng']
            else: 
                print("Error: No results found")

        histWeatherData = historicalWeather.get_historical_data(geoLat, geoLon, realTime)
        histWeatherDF = historicalWeather.process_historical_data(histWeatherData)
        return ('histWeatherDF', histWeatherDF)

    else:
        raise ValueError("choice must be 1 or 2")
    

if __name__ == "__main__":
    fetch_weather_data('1', 'Bolton', 'CA', 1, realTime = None)
