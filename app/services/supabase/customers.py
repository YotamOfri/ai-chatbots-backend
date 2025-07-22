from fastapi import Request
from app.models.whatsapptypes import WhatsAppWebhookData
from supabase import Client


def update_customer_if_exists(request: Request):
    form = request.state.form
    supabase = request.state.supabase  # type: Client
    customer_phone_number = form.get("From")
    name = form.get("ProfileName")
    wa_id = form.get("WaId")
    customer = (
        supabase.table("customers")
        .select("*")
        .eq("phone_number", customer_phone_number)
        .execute()
        .data
    )
    if not customer:
        (
            supabase.table("customers")
            .insert(
                {
                    "phone_number": customer_phone_number,
                    "phone_number_id": wa_id,
                    "chatbot_id": request.state.chatbot["id"],
                    "name": name,
                }
            )
            .execute()
        )

    request.state.customer = customer
