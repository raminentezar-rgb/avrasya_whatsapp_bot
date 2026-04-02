import os
import requests
from dotenv import load_dotenv

load_dotenv('C:/Users/Avrasya/.gemini/antigravity/scratch/avrasya_bot/.env', override=True)

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json?PageSize=10"

response = requests.get(url, auth=(account_sid, auth_token))
messages = response.json().get('messages', [])

for msg in messages:
    print(f"Time: {msg.get('date_created')} | From: {msg.get('from')} | To: {msg.get('to')} | Status: {msg.get('status')} | Error: {msg.get('error_message')} | Body: {msg.get('body')}")
