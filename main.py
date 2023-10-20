import requests
import json
import datetime
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

# This function gets the location data using the city name and country code. The data is then converted to json and returned.
def get_location_data(city, countryCode, callAmount):
    endpoint = 'http://api.openweathermap.org/geo/1.0/direct'
    url = f"{endpoint}?q={city},{countryCode}&limit={callAmount}&appid={config.api_key}"
    res = requests.get(url)
    data = res.json()
    return data

# This function gets the current weather data using the lat and lon values from the location data. The data is then converted to json and returned.
def get_current_weather_data(lat, lon):
    currWeatherURL = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly,alerts&appid={config.api_key}"
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

# This is where we get user input and call the functions to get the data and plot it.
def main():
    city = input('Enter city name (You may leave this blank if you want to get a country\'s weather data): ') 
    countryCode = input('Country Code: ')
    callAmount = input('Enter amount of API calls: ')

    location_data = get_location_data(city, countryCode, callAmount) # get location data from function and assign to var

    if location_data[0] != '404':
        latlon = location_data[0] #get the first index of location_data (which is a list) and assign to var
        lat = latlon['lat'] # assign the lat value to the lat var
        lon = latlon['lon'] # assign the lon value to the lon var

        currWeatherData = get_current_weather_data(lat, lon) # get current weather data from function and assign to var
        currWeatherDF = process_weather_data(currWeatherData) # use process function assign to var

        sortedDFbyTemp = sortbyTemp(currWeatherDF) # call sortbyTemp function and assign to var
        sortedDFbyHumidity = sortbyHumidity(currWeatherDF) # call sortbyHumidity function and assign to var

        print('Sorted by temperature: ')
        print(sortedDFbyTemp) #print sorted (temp) dataframe to console
        sortedDFbyTemp.to_csv('sortedbyTemp.csv', sep=',', encoding='utf-8') #export sorted (temp) dataframe to csv

        print('Sorted by humidity: ')
        print(sortedDFbyHumidity) #print sorted (humidity) dataframe to console
        sortedDFbyHumidity.to_csv('sortedbyHumidity.csv', sep=',', encoding='utf-8') #export sorted (humidity) dataframe to csv

        plotDataByMaxTemp(sortedDFbyTemp) #call plot function and pass the sorted (temp) dataframe
        plotDataByHumidity(sortedDFbyHumidity) #call plot function and pass the sorted (humidity) dataframe
        plotWindspeedvsWindDeg(currWeatherDF) #call plot function and pass the processed dataframe


if __name__ == "__main__":
    main()





