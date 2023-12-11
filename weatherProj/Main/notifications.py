import config
from twilio.rest import Client

account_sid = config.twilio_account_sid
auth_token = config.twilio_api_key

# this is the function that will send the text message
def send_notifs(phone_num, message_body):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body,
        from_=config.twilio_phone_num,
        to='+1'+ phone_num
    )
    


