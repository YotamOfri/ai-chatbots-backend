from fastapi import Request
from app.models.whatsapptypes import WhatsAppWebhookData
from supabase import Client


def get_chatbot(whatsappData: WhatsAppWebhookData, request: Request):
    supabase = request.state.supabase  # type: Client
    print(whatsappData["entry"][0]["changes"][0]["value"]["metadata"], "whatsappData")
    phone_number_id_str = whatsappData["entry"][0]["changes"][0]["value"]["metadata"][
        "phone_number_id"
    ]
    request.state.phone_number_id = phone_number_id_str
    try:
        phone_number_id = int(phone_number_id_str)
    except ValueError:
        print(f"Invalid phone_number_id: {phone_number_id_str}")
        return None

    chatbot_data = (
        supabase.table("chatbots")
        .select("*")
        .eq("phone_number_id", phone_number_id)
        .execute()
    )
    request.state.account_id = chatbot_data.data[0]["account_id"]
    request.state.chatbot = chatbot_data.data[0]
