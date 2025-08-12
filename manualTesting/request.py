import requests
import sys

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# URL to send the POST request to
url = "http://localhost:8000/webhook"

# Static form data fields (everything except 'Body')
base_form_data = [
    ("SmsMessageSid", "SM8569033f3f4183bd637d5ae8196d5394"),
    ("NumMedia", "0"),
    ("ProfileName", "Eyal Avraham"),
    ("MessageType", "text"),
    ("SmsSid", "SM8569033f3f4183bd637d5ae8196d5394"),
    ("WaId", "972532862261"),
    ("SmsStatus", "received"),
    ("To", "whatsapp:+14155238886"),
    ("NumSegments", "1"),
    ("ReferralNumMedia", "0"),
    ("MessageSid", "SM8569033f3f4183bd637d5ae8196d5394"),
    ("AccountSid", "AC1824fec7e33cc9a5cf6b97e5aec49912"),
    (
        "ChannelMetadata",
        '{"type":"whatsapp","data":{"context":{"ProfileName":"Eyal Avraham","WaId":"972532862261"}}}',
    ),
    ("From", "whatsapp:+972532862261"),
    ("ApiVersion", "2010-04-01"),
]

print("📨 WhatsApp Chat Simulator")
print("Type your message and press Enter. Type 'exit' to quit.\n")

while True:
    message = input("🧑 You: ")
    if message.lower() in ("exit", "quit"):
        print("👋 Exiting chat.")
        break

    # Add the dynamic Body field
    form_data = base_form_data + [("Body", message)]

    # Send POST request
    response = requests.post(url, data=form_data)

    # Print response from server
    print("🤖 Server response:", response.status_code, response.text, "\n")
