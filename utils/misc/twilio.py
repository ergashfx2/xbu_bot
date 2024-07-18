from twilio.rest import Client

auth_token = "79e8c14712473b041d55b75a6e06f21e"
account_sid = 'AC41dc9bc4d99c38e3ae0987bc545843f1'
client = Client(account_sid, auth_token)

def send_sms(message, phone):
   message = client.messages.create(
     body=message,
     from_='+12513206400',
     to='+998901288877'
)