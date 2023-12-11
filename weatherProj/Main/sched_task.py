#this script is used for to initialize the messages to send messages and ultimately send them to the user.

from weather_fetch import fetch_weather_data
from notifications import send_notifs
import sqlite3
import os

def send_daily_notifs():

    #connect to the db and get the user data
    conn = sqlite3.connect('weatherProj\WeatherApp.db')
    cur = conn.cursor()
    cur.execute('''SELECT u.username, uf.phone_num, uf.city, uf.country_code 
                   FROM userPref uf
                   JOIN users u ON u.user_id = uf.user_id''')
    userPref = cur.fetchall() 

    #for each user in the db, get their weather data and send them a message
    for user_data in userPref:
        username, phone_num, city, countryCode = user_data
        print(phone_num)
        choice = "1"
        callAmount = 1
        realTime = None

        try:
            weather_data = fetch_weather_data(choice, city, countryCode, callAmount, realTime)
        except IndexError as e:
            print(f'Error fetching weather data: {e}')
            return

        weather_type = weather_data[1]['weather_description'].iloc[0]
        high_temp = weather_data[1]['temp'][0]['max']
        low_temp = weather_data[1]['temp'][0]['min']
        humidity = weather_data[1]['humidity'].iloc[0]
        print(weather_type, high_temp, low_temp, humidity)

        message = f'Good morning {username}! Here\'s your daily weather update:\n'

        if 'snow' in weather_type or 'blizzard' in weather_type or 'sleet' in weather_type:
            message += f'Hoagie down, its going to be a snowy one \U0001F328,  with a high of {high_temp}°C and a low of {low_temp}°C. Bundle up!'
        elif 'rain' in weather_type or 'drizzle' in weather_type or 'shower' in weather_type or 'downpour' in weather_type or 'pour' in weather_type or 'mist' in weather_type or 'hail' in weather_type or 'precipitation' in weather_type:
            message += f'Good morning! Today\'s weather will be rain \U0001F327 with a high of {high_temp}°C and a low of {low_temp}°C. Don\'t forget your umbrella \uE48C!'
        elif 'thunderstorm' in weather_type or 'storm' in weather_type or 'lightning' in weather_type or 'thunder' in weather_type:
            message += f'Watch out! It may be stormy today u"\u26C8", with a high of {high_temp}°C and a low of {low_temp}°C. Don\'t forget your umbrella \uE48C and stay safe!'
        elif 'clouds' in weather_type or 'overcast' in weather_type or 'cloud' in weather_type:
            message += f'Todays cloudy \u2601!  Today\'s weather will be {weather_type} with a high of {high_temp}°C and a low of {low_temp}°C.'
        elif 'clear' in weather_type or 'sunny' in weather_type or 'hot' in weather_type or 'warm' in weather_type:
            message += f'Good morning! Today\'s weather will be {weather_type} with a high of {high_temp}°C and a low of {low_temp}°C. Don\'t forget your sunscreen!'
        if humidity > 50:
            message += f'\nWatch out Queen! It could be a frizzy one, with a humidity of {humidity}%'
    
        send_notifs(phone_num, message)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    send_daily_notifs()