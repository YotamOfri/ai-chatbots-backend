from twilio.rest import Client
from app.core.config import settings
from twilio.rest import Client


def send_whatsapp_options(form, body_text, buttons):
    """
    Sends a WhatsApp interactive message with reply buttons.

    :param form: incoming form with From/To
    :param body_text: main message body
    :param buttons: list of tuples (id, title)
                    e.g. [("store_main", "🏬 Main Store"), ("store_outlet", "🛒 Outlet")]
    """

    to = form.get("From")
    from_ = form.get("To")
    client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

    interactive_buttons = [
        {"type": "reply", "reply": {"id": btn_id, "title": btn_title}}
        for btn_id, btn_title in buttons
    ]

    try:
        message = client.messages.create(
            to=to,
            from_=from_,
            status_callback="https://example.com/callback",
        )
        print("Interactive message sent successfully!")
    except Exception as e:
        print(f"Error sending interactive message: {e}")


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


def send_whatsapp_message(to_, from_, message):
    # message_to = form.get("From")
    # message_from = form.get("To")
    client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
    message = client.messages.create(
        to=to_,
        from_=from_,
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
