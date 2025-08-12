from fastapi import Request
from supabase import Client


def get_chatbot(request: Request):
    form = request.state.form
    supabase = request.state.supabase  # type: Client
    phone_number_id_str = form.get("To")
    request.state.phone_number_id = phone_number_id_str
    if phone_number_id_str is None:
        return
    try:
        phone_number_id = 14155238886
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
