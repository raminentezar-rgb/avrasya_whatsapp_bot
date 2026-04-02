import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_telegram_message(chat_id, message):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.warning(f"TELEGRAM_BOT_TOKEN not set. Mock sending message to {chat_id}: {message}")
        return True, None
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, None
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False, str(e)

def send_whatsapp_message(phone_number, message_body):
    """
    Sends WhatsApp message via Twilio or Meta API depending on configuration.
    For this initial phase, we use Twilio Sandbox format or mock.
    """
    whatsapp_provider = os.environ.get('WHATSAPP_PROVIDER', 'mock')
    
    if whatsapp_provider == 'mock':
        logger.warning(f"MOCK WhatsApp to {phone_number}: {message_body}")
        return True, None
        
    elif whatsapp_provider == 'twilio':
        # Twilio sends via HTTP Basic Auth
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER') # e.g. whatsapp:+14155238886
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        # Twilio requires form-encoded data, not json
        payload = {
            'From': from_number,
            'To': f"whatsapp:{phone_number}",
            'Body': message_body
        }
        try:
            response = requests.post(url, data=payload, auth=(account_sid, auth_token))
            response.raise_for_status()
            return True, None
        except Exception as e:
            logger.error(f"Twilio API Error: {response.text if 'response' in locals() else e}")
            return False, str(e)
            
    elif whatsapp_provider == 'meta':
        # Meta Cloud API
        access_token = os.environ.get('META_ACCESS_TOKEN')
        phone_number_id = os.environ.get('META_PHONE_NUMBER_ID')
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": message_body
            }
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return True, None
        except Exception as e:
            logger.error(f"Meta API Error: {response.text if 'response' in locals() else e}")
            return False, str(e)
    
    return False, "Invalid WHATSAPP_PROVIDER configured"
