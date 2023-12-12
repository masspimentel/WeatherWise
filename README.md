# WeatherWise by masspimentel

☀🌤☀

## Overview

WeatherWise is a Python application that provides detailed weather forecasts for the next 7 days. It features a fully-functional user interface built with the PyQT library, secure user authentication using bcrypt, and data storage in SQLite. Users can view weather graphs and input phone numbers for notifications, and access current weather data. 

## Main library explanation

- [OpenWeatherMap](https://openweathermap.org/api): This is an open-source web API allowing users to fetch weather data from your current location or a preset location. Outputs data in JSON format.
- [pandas](https://pandas.pydata.org/): A python library widely used in data analysis. This allows the user to create custom dataframes containing data from a plethora of data sources.
- [Matplotlib](https://matplotlib.org/): A python library used for data visualization. This allows the user to create powerful and custom visualization from different data sources. Mainly used with     Pandas dataframes in this application.
- [PyQT6](https://pypi.org/project/PyQt6/): A powerful python library used for GUI creation. This library allows to create custom labels, buttons, and layouts.
- [bcrypt](https://pypi.org/project/bcrypt/): A python library used to encode sensitive information.
- [SQLite3](https://docs.python.org/3/library/sqlite3.html): A python library to connect with SQLite Databases on your system. 

This is an ongoing project that I will be continually add new functions to. 

## Requirements

- Python 3.11
- Libraries: requests, json, datetime, pandas, numpy, matplotlib, seaborn, opencage, time
- OpenWeatherAPI key (sign up at [OpenWeather](https://openweathermap.org/))
- OpenCageAPI key (sign up at [OpenCage](https://opencagedata.com/))
- Twilio API key, Auth. token, and phone number (sign up at [Twilio](https://www.twilio.com/try-twilio))

## Usage

1. Clone the repository:

   ```
   git clone https://github.com/masspimentel/WeatherWise.git
   cd WeatherWise
   ```
   Enter the city name, country code, and the number of API calls as prompted.
2. Download the requirements.txt file
   ```
   pip install -r /path/to/requirements.txt
   ```
3. Start the application in your IDE or use a CLI by using one of the commands below:
   ```
   cd path/to/main.py
   python main.py
   ```
   ```
   cd path/to/main.py
   python3 main.py
   ```
   ```
   cd path/to/main.py
   py main.py
   ```

## Results
WeatherWise displays weather information based on user location or input. It presents daily weather cards and customizable graphs. All data is stored securely in a local SQLite database.

## To use notification function
1. Create a Twilio account [here](https://www.twilio.com/try-twilio)
2. Create an API key, authorization token and obtain your Twilio number
3. Create a config.py class and name the variables accordingly. 
4. Once those are created, you should have the notifications set up.
5. To automate the notifications, you have a plethora of options to choose. From cloud based (AWS, Google Cloud, Heroku) or local based (Windows Task manager, Linux Cron Jobs).
   
   ### AWS Linux Setup (this is what I used)
   1. Go to [AWS](https://portal.aws.amazon.com/billing/signup) and sign up
   2. Search EC2 and create a new instance
   3. Follow the setup process (most of the settings can be left to their defaults). Make sure to create an SSH key, this 
      will be vital in connecting to your EC2.
   4. Once created, click 'Launch Instance'
   5. AWS should give you instructions on how to connect to your EC2. If it doesnt you can use the steps below to connect.
      
      a. Download a SSH client (PuTTy or Git Bash)
      
      b. In your CLI put his command in.
         ```
         ssh -i "path/to/SSHKey.pem" EC2-username@ec2-EC2-IP-ADDRESS.YOURREGION.compute.amazonaws.com
         ```
   7. Now your in!
   8. To move files from your local env. to your EC2 instance. Open your SSH client (not connected to EC2)
   9. Use this command:
      ```
      scp -i /path/to/pem/ssh/token /path/to/local/file ec2user@ec2instance:/path/to/ec2/location
      ```
   10. Files will now be moved.
   11. You may have to install python depending on your choices in your EC2. You will have to install the different 
       libraries using the requirements.txt file.
       
       a. Follow this [guide](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html) to install           python on your EC2.
       
       b. To install your requirements.txt, use the below command while connected to your EC2:
          ```
          sudo pythonX -m pip install -r path/to/requirements.txt
          ```
          X = version of python installed on EC2
   ### To setup a Cron Job
   1. While connected to your EC2 instance, put this command in:
      ```
      crontab -e
      ```
   2. You can use a command such as below (pointing to the sched_task.py)
      ```
      45 12 * * * /usr/bin/python3 path/to/sched_task.py >> /home/YOURUSERNAME/cronlog.log 2>&1
      ```
      Each * designates a certain time interval in this format: minute, hour, day, week, month


## Sample Photo of application
![alt text](https://github.com/masspimentel/beg-project/blob/main/weatherProj/Main/images/SampleAppPhoto.PNG?raw=true)
![alt text](https://github.com/masspimentel/beg-project/blob/main/weatherProj/Main/images/SampleWeatherfromApp.PNG?raw=true)

## Sample Output of data frame
|       dt     |     sunrise   |     sunset    |     moonrise  |     moonset   |  pop  |  temp_max  |
|---------------|--------------|---------------|---------------|---------------|-------|------------|
|  2023-04-06  |  06:57:29 AM  |  06:36:09 PM  |  03:22:03 AM  |  02:26:58 PM  |  0.19  |  25.73  |
|  2023-04-07  |  06:55:57 AM  |  06:37:16 PM  |  04:19:03 AM  |  03:27:25 PM  |  0.62  |  26.37  |
|  2023-04-08  |  06:54:25 AM  |  06:38:24 PM  |  05:15:56 AM  |  04:28:10 PM  |  0.64  |  27.19  |
|  2023-04-09  |  06:52:54 AM  |  06:39:32 PM  |  06:12:44 AM  |  05:28:42 PM  |  0.17  |  28.01  |
|  2023-04-10  |  06:51:22 AM  |  06:40:40 PM  |  07:09:28 AM  |  06:28:49 PM  |  0.29  |  28.05  |

## Sample Graphs

![alt text](https://github.com/masspimentel/beg-project/blob/main/weatherProj/Main/images/wspeedvswdegcompassgraph.PNG?raw=true)
![alt text](https://github.com/masspimentel/beg-project/blob/main/weatherProj/Main/images/maxtempbargraph.PNG?raw=true)
![alt text](https://github.com/masspimentel/beg-project/blob/main/weatherProj/Main/images/humiditybargraph.PNG?raw=true)

## Roadmap
```
- [x] Basic Data Analysis
- [x] Usage of Pandas
- [x] Begin implementation of matplotlib
- [x] Create GUI with PyQT
- [ ] Create new, more advanced dataframes for visualization
- [ ] Add functionality to retrieve historical data
```
## Updates

UPDATE 24/10/2023: I have now added functionality to retrieve historical weather data (only to 1979 and up to 4 days in the future). Also, ability to convert between lat and lon to readable location with OpenCageAPI.

UPDATE 10/12/2023: Full UI for users and functionality for notifications. Historical Data is unused (for now). More functions will come later but for now its mostly complete. Also, added user authentication and its data as well as user preferences are stored in a SQLite DB. I understand its not needed as it is a local application but it was fun to learn how to implement authentication.

## Acknowledgments
Special thanks to OpenWeather for providing weather data through their API.

Feel free to customize this README to suit your project's specific needs.
