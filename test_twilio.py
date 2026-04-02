import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv('C:/Users/Avrasya/.gemini/antigravity/scratch/avrasya_bot/.env', override=True)

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER')
to_number = 'whatsapp:+905373474903'
message_body = "Hello from direct Twilio API Python test!"

url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
payload = {
    'From': from_number,
    'To': to_number,
    'Body': message_body
}

print(f"Sending via Twilio: From {from_number} to {to_number}")
response = requests.post(url, data=payload, auth=(account_sid, auth_token))
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
