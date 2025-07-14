import requests
import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")


def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v23.0/{PHONE_ID}/messages"
    print(to, "", message)
    print(url)
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message},
    }
    requests.post(url, headers=headers, json=data)
