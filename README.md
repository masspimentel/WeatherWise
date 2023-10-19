# Weather Analysis with OpenWeatherAPI

![Weather Image]

A Python script to retrieve and analyze weather data using OpenWeatherAPI.

## Overview

This Python script allows you to retrieve weather information for a given city using the OpenWeatherAPI. It provides daily weather forecasts, including temperature, sunrise/sunset times, moonrise/moonset times, moon phase, precipitation probability, and wind speed. Additionally, it identifies the top temperatures for the forecasted days.

This is an ongoing project that I will be continually add new functions to. 

## Requirements

- Python 3.x
- Libraries: requests, json, datetime, pandas, numpy, matplotlib, seaborn
- OpenWeatherAPI key (sign up at [OpenWeather](https://openweathermap.org/))

## Usage

1. Clone the repository:

   ```
   git clone https://github.com/masspimentel/beg-project.git
   cd your-repo

   Run the script: python main.py
   Enter the city name, country code, and the number of API calls as prompted.

## Results
The script will display the weather data, and the top temperatures will be sorted and shown in descending order.

## Sample Output
|       dt     |     sunrise   |     sunset    |     moonrise  |     moonset   |  pop  |  temp_max  |
|---------------|--------------|---------------|---------------|---------------|-------|------------|
|  2023-04-06  |  06:57:29 AM  |  06:36:09 PM  |  03:22:03 AM  |  02:26:58 PM  |  0.19  |  25.73  |
|  2023-04-07  |  06:55:57 AM  |  06:37:16 PM  |  04:19:03 AM  |  03:27:25 PM  |  0.62  |  26.37  |
|  2023-04-08  |  06:54:25 AM  |  06:38:24 PM  |  05:15:56 AM  |  04:28:10 PM  |  0.64  |  27.19  |
|  2023-04-09  |  06:52:54 AM  |  06:39:32 PM  |  06:12:44 AM  |  05:28:42 PM  |  0.17  |  28.01  |
|  2023-04-10  |  06:51:22 AM  |  06:40:40 PM  |  07:09:28 AM  |  06:28:49 PM  |  0.29  |  28.05  |


## Roadmap
<code>
```
- [x] Basic Data Analysis
- [x] Usage of Pandas
- [ ] Begin implementation of matplotlib & Seaborn for visualization
- [ ] Create new, more advanced dataframes for visualization
- [ ] Create GUI & more user input to create a more customizable application
```
</code>

## Acknowledgments
Special thanks to OpenWeather for providing weather data through their API.

Feel free to customize this README to suit your project's specific needs.