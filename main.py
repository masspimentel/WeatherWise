import requests
import json
import datetime
from datetime import datetime
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import time
from opencage.geocoder import OpenCageGeocode


class currentWeather:
    # This function gets the location data using the city name and country code. The data is then converted to json and returned.
    def get_location_data(city, countryCode, callAmount):
        endpoint = 'http://api.openweathermap.org/geo/1.0/direct'
        url = f"{endpoint}?q={city},{countryCode}&limit={callAmount}&appid={config.openweather_api_key}"
        res = requests.get(url)
        data = res.json()
        return data

    # This function gets the current weather data using the lat and lon values from the location data. The data is then converted to json and returned.
    def get_current_weather_data(lat, lon):
        currWeatherURL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly,alerts&appid={config.openweather_api_key}"
        currWeatherRes = requests.get(currWeatherURL)
        currWeatherData = currWeatherRes.json() 
        return currWeatherData

    # This function processes the json data and returns a dataframe with the processed data. not all data is processed, was mostly used to test the data. all the variables are self-explanatory, just converting the data to more readable formats.
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
        print(currWeatherDF.columns.to_list())
        return currWeatherDF

    #This function sorts the data of the json data by temperature and returns a dataframe with the sorted data (by temperature).
    def sortbyTemp(data):
        if not data.empty:
            topTempsExtr = data['temp'].apply(lambda x: x['max']) #extract the max temp value from the temp column (as this column hold a dict of min, max, mean, etc.). lambda x is a function that allows us to extract the max value from the dict
            topTempsDF = pd.DataFrame(topTempsExtr) #SEE BELOW FOR EXPLANATION ON HOW THE DATAFRAME IS CREATED
            mergeDFs = pd.merge(data, topTempsDF, left_index=True, right_index=True)
            mergeDFs.rename(columns={'temp_y': 'temp_max'}, inplace=True)
            sortedDFbyTemp = mergeDFs.sort_values(by='temp_max', ascending=False)
            #print(sortedDFbyTemp)
            return sortedDFbyTemp
        else:
            print("Data is empty or doesn't meet the condition.")

    # This function sorts the data of the json data by humidity and returns a dataframe with the sorted data.
    def sortbyHumidity(data):
        if not data.empty:
            humSort = data.sort_values(by='humidity', ascending=False) # not really needed, used to assign var
            humSortDF = pd.DataFrame(humSort) # create new dataframe with the sorted data (by humidity)
            mergeDFs = pd.merge(data, humSortDF[['dt', 'humidity']], on='dt', how='left') # merge the dataframes together using the dt column as the key
            sortbyTopHumidity = mergeDFs.sort_values(by='humidity_y', ascending=False) # real sorting happens here
            return sortbyTopHumidity # return the sorted dataframe
        else: print('Data is empty or doesn\'t meet the condition.')

    # This function plots the data in a polar plot passing the windspeed and wind degree.
    def plotWindspeedvsWindDeg(data):
        if not data.empty:
            sns.set_theme(style="whitegrid")
            fig = plt.figure()
            ax = fig.add_subplot(projection='polar') # sets the projection to polar (compass/radial plot)
            sc = ax.scatter(data['wind_deg'], data['wind_speed'], c=data['wind_speed'], cmap='winter') # c is what the plots are colored by, cmap is the color palette
            cbar = plt.colorbar(sc, label='Wind Speed (m/s)') #create a colorbar on the y axis that shows the wind speed based on the color of the plot
            cbar.set_label('Wind Speed (m/s)')
            plt.title('Wind Speed vs Wind Degree')
            plt.show()
        else: print('Data is empty or doesn\'t meet the condition.')

    # This function plots the data in a bargrapgh where the x-axis is the date and the y-axis is the max temperature. READ COMMENTS BELOW FOR EXPLANATION ON HOW THE PLOT IS CREATED
    def plotDataByMaxTemp(data):
        if not data.empty:
            sns.set_theme(style="whitegrid")
            col_pallette = sns.color_palette("rocket", len(data))
            rank = data["temp_max"].argsort().argsort()
            ax = sns.barplot(x="dt", y="temp_max", data=data, palette=np.array(col_pallette[::-1])[rank])
            plt.xticks(fontsize=8)
            plt.title('Max Temperature by Date')
            plt.show()
        else: print('Data is empty or doesn\'t meet the condition.')

    # This function plots the data in a bargrapgh where the x-axis is the date and the y-axis is the humidity
    def plotDataByHumidity(sortbyTopHumidity):
        if not sortbyTopHumidity.empty:
            sns.set_theme(style="whitegrid") #setting theme
            col_pallette = sns.color_palette("rocket", len(sortbyTopHumidity)) #setting color palette
            rank = sortbyTopHumidity["humidity_y"].argsort().argsort() #creating a rank for the color palette
            sns.barplot(x="dt", y="humidity_y", data=sortbyTopHumidity, palette=np.array(col_pallette[::-1])[rank]) #plotting the data and passing the args for the pallette, np.array is used to convert the color palette to an array then flip using -1, then passing the rank var to rank the colors based on humidity
            plt.xticks(fontsize=8) #setting x axis font 
            plt.title('Humidity by Date') #adding a title
            plt.show()
        else: print('Data is empty or doesn\'t meet the condition.')

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
        print(historyData)
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
        print(histweatherDF)
        return histweatherDF
    @staticmethod
    def plot_historical_data(histweatherDF):
        if not histweatherDF.empty:
            sns.set_theme(style="whitegrid")
            col_pallette = sns.color_palette("rocket", len(histweatherDF))
            rank = histweatherDF["temp"].argsort().argsort()
            ax = sns.barplot(x="dt", y="temp", data=histweatherDF, palette=np.array(col_pallette[::-1])[rank])
            plt.xticks(fontsize=8)
            plt.title('Max Temperature by Date')
            plt.show()
        else:
            print('Data is empty or doesn\'t meet the condition')

# This is where we get user input and call the functions to get the data and plot it.
def main():
    print("1. Get current weather data")
    print("2. Get historical weather data")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        city = input("Enter city name: ")
        countryCode = input("Country Code: ")
        callAmount = input("Enter amount of API calls: ")
        
        location_data = currentWeather.get_location_data(city, countryCode, callAmount)
        if location_data[0] != '404':
            latlon = location_data[0]
            lat = latlon['lat']
            lon = latlon['lon']
            currWeatherData = currentWeather.get_current_weather_data(lat, lon) # get current weather data from function and assign to var
            currWeatherDF = currentWeather.process_weather_data(currWeatherData) # use process function assign to var

            sortedDFbyTemp = currentWeather.sortbyTemp(currWeatherDF) # call sortbyTemp function and assign to var
            sortedDFbyHumidity = currentWeather.sortbyHumidity(currWeatherDF) # call sortbyHumidity function and assign to var

            print('Sorted by temperature: ')
            print(sortedDFbyTemp) #print sorted (temp) dataframe to console
            sortedDFbyTemp.to_csv('sortedbyTemp.csv', sep=',', encoding='utf-8') #export sorted (temp) dataframe to csv

            print('Sorted by humidity: ')
            print(sortedDFbyHumidity) #print sorted (humidity) dataframe to console
            sortedDFbyHumidity.to_csv('sortedbyHumidity.csv', sep=',', encoding='utf-8') #export sorted (humidity) dataframe to csv

            currentWeather.plotDataByMaxTemp(sortedDFbyTemp) #call plot function and pass the sorted (temp) dataframe
            currentWeather.plotDataByHumidity(sortedDFbyHumidity) #call plot function and pass the sorted (humidity) dataframe
            currentWeather.plotWindspeedvsWindDeg(currWeatherDF) #call plot function and pass the processed dataframe
    
    elif choice == "2":
        city = input("Enter city name: ")
        countryCode = input("Country Code: ")
        realTime = input("Enter Date DD/MM/YYYY:")
        print("Note: OpenWeatherMapAPI only has historical data from 1/1/1970 to 4 days ahead of the current date. Please do not enter a date before or after this range.")
        callAmount = input("Enter amount of API calls: ")

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
            historicalWeather.plot_historical_data(histWeatherDF)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()




