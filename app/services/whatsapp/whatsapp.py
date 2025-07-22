import os
from dotenv import load_dotenv
from twilio.rest import Client
from app.core.config import settings

load_dotenv()

WHATSAPP_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")


from twilio.rest import Client


def send_whatsapp_location(form, latitude, longitude, label="Our Shop"):
    to = form.get("From")
    from_ = form.get("To")
    client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

    # Send native WhatsApp location pin
    print("Sending location pin...")
    client.messages.create(
        to=to,
        from_=from_,
        body=label,  # This will appear as the message text
        persistent_action=[f"geo:{latitude},{longitude}|{label}"],
        status_callback="https://example.com/callback",
    )
    print("Location pin sent successfully!")


def send_whatsapp_message(form, message):
    message_to = form.get("From")
    message_from = form.get("To")
    client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
    message = client.messages.create(
        to=message_to,
        from_=message_from,
        body=message,
        status_callback="https://example.com/callback",
    )


# Metas Api
# def send_whatsapp_message(to, message):
#     client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
#     url = f"https://graph.facebook.com/v23.0/{PHONE_ID}/messages"
#     print(to, "", message)
#     print(url)
#     headers = {
#         "Authorization": f"Bearer {WHATSAPP_TOKEN}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "messaging_product": "whatsapp",
#         "to": to,
#         "type": "text",
#         "text": {"body": message},
#     }
#     requests.post(url, headers=headers, json=data)
