import config
import sqlite3
from twilio.rest import Client
from weatherDB import weatherDB

account_sid = config.twilio_account_sid
auth_token = config.twilio_api_key

# this is the function that will send the text message
def send_notifs(phone_num, message_body):
    client = Client(account_sid, auth_token)

    conn = sqlite3.connect('weatherProj\WeatherApp.db')
    cur = conn.cursor()
    cur.execute('''
                SELECT phone_num FROM userPref
                WHERE phone_num = ?
    ''', (phone_num,))
    phone_num = cur.fetchall()

    if phone_num:    
        message = client.messages.create(
            body=message_body,
            from_=config.twilio_phone_num,
            to='+1'+ phone_num
        )
    else:
        print('No phone number found')
    


