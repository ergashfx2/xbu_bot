import os
from twilio.rest import Client

def send_sms(phone_number,message):
    account_sid = 'AC41dc9bc4d99c38e3ae0987bc545843f1'
    auth_token = '6bd6045937b33adf15d8e74fcbebd56a'
    client = Client(account_sid, auth_token)
    print(phone_number)
    message = client.messages.create(
        body=message,
        from_="+12513206400",
        to=f"+{phone_number}",
    )