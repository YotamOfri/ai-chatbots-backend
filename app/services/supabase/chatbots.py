from fastapi import Request
from app.models.whatsapptypes import WhatsAppWebhookData
from supabase import Client


def get_chatbot(form: any, request: Request):
    supabase = request.state.supabase  # type: Client
    print("test")
    phone_number_id_str = form.get("WaId")
    request.state.phone_number_id = phone_number_id_str
    print(f"phone_number_id: {phone_number_id_str}")
    if phone_number_id_str is None:
        return
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
