from twilio.rest import Client

auth_token = "62e2fda1e607ee97a751ddc03930e2c3"
account_sid = 'AC41dc9bc4d99c38e3ae0987bc545843f1'
client = Client(account_sid, auth_token)

def send_sms(message, phone):
   message = client.messages.create(
     body=message,
     from_='+12513206400',
     to='+998901288877'
)