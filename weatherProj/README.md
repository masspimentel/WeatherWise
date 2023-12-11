# Weather Analysis with OpenWeatherAPI

☀🌤☀

A Python script to retrieve and analyze weather data using OpenWeatherAPI.

## Overview

This Python script allows you to retrieve weather information for a given city using the OpenWeatherAPI. It provides daily weather forecasts, including temperature, sunrise/sunset times, moonrise/moonset times, moon phase, precipitation probability, and wind speed. Additionally, it identifies the top temperatures for the forecasted days. 

UPDATE 24/10/2023: I have now added functionaility to retrieve historical weather data (only to 1979 and up to 4 days in the future). Also, ability to convert between lat and lon to readable location with OpenCageAPI.

UPDATE 10/12/2023: Full UI for users and functionality for notifications. Historical Data is unused (for now). More functions will come later but for now its mostly complete. Also, added user authentication. I understand its not needed as it is a local application but it was fun to learn how to implement this.

This is an ongoing project that I will be continually add new functions to. 

## Requirements

- Python 3.x
- Libraries: requests, json, datetime, pandas, numpy, matplotlib, seaborn, opencage, time
- OpenWeatherAPI key (sign up at [OpenWeather](https://openweathermap.org/))
- OpenCageAPI key (sign up at [OpenCage](https://opencagedata.com/))
- Twilio API key, Auth. token, and phone number (sign up at [Twilio](https://www.twilio.com/try-twilio))

## Usage

1. Clone the repository:

   ```
   git clone https://github.com/masspimentel/beg-project.git
   cd your-repo
   ```
   Run the script: python main.py
   Enter the city name, country code, and the number of API calls as prompted.
2. Download the requirements.txt file
   ```
   pip install -r /path/to/requirements.txt
   ```

## Results
This application is a displays weather info depending on user location (or user input). For now it will show weather cards for each day. I will also display the graphs shown below. The data is stored in a local SQLite DB. 

##To use notification function
1. Create a Twilio account [here](https://www.twilio.com/try-twilio)
2. Create an API key, authorization token and obtain your Twilio number
3. Create a config.py class and name the variables accordingly. 
4. Once those are created, you should have the notifications set up.
5. To automate the notifications, you have a plethora of options to choose. From cloud based (AWS, Google Cloud options, Heroku) or local based (Windows Task manager, Linux Cron Jobs). 
   a. I chose to use AWS the setup is relatively simple but I wont go over that here as it is all based on preference.

## Sample Photo of application
![alt text](https://github.com/masspimentel/beg-project/blob/main/images/SampleAppPhoto.PNG?raw=true)
![alt text](https://github.com/masspimentel/beg-project/blob/main/images/SampleWeatherfromApp.PNG?raw=true)

## Sample Output of data frame
|       dt     |     sunrise   |     sunset    |     moonrise  |     moonset   |  pop  |  temp_max  |
|---------------|--------------|---------------|---------------|---------------|-------|------------|
|  2023-04-06  |  06:57:29 AM  |  06:36:09 PM  |  03:22:03 AM  |  02:26:58 PM  |  0.19  |  25.73  |
|  2023-04-07  |  06:55:57 AM  |  06:37:16 PM  |  04:19:03 AM  |  03:27:25 PM  |  0.62  |  26.37  |
|  2023-04-08  |  06:54:25 AM  |  06:38:24 PM  |  05:15:56 AM  |  04:28:10 PM  |  0.64  |  27.19  |
|  2023-04-09  |  06:52:54 AM  |  06:39:32 PM  |  06:12:44 AM  |  05:28:42 PM  |  0.17  |  28.01  |
|  2023-04-10  |  06:51:22 AM  |  06:40:40 PM  |  07:09:28 AM  |  06:28:49 PM  |  0.29  |  28.05  |

## Sample Graphs

![alt text](https://github.com/masspimentel/beg-project/blob/main/images/wspeedvswdegcompassgraph.PNG?raw=true)
![alt text](https://github.com/masspimentel/beg-project/blob/main/images/maxtempbargraph.PNG?raw=true)
![alt text](https://github.com/masspimentel/beg-project/blob/main/images/humiditybargraph.PNG?raw=true)

## Roadmap
```
- [x] Basic Data Analysis
- [x] Usage of Pandas
- [x] Begin implementation of matplotlib & Seaborn for visualization
- [x] Create GUI & more user input to create a more customizable application
- [ ] Create new, more advanced dataframes for visualization
- [ ] Added functionality to retrieve historical data
```

## Acknowledgments
Special thanks to OpenWeather for providing weather data through their API.

Feel free to customize this README to suit your project's specific needs.
