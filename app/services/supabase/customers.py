from fastapi import Request
from app.models.whatsapptypes import WhatsAppWebhookData
from supabase import Client


def update_customer_if_exists(whatsappData: WhatsAppWebhookData, request: Request):
    supabase = request.state.supabase  # type: Client
    customer_phone_number = whatsappData["entry"][0]["changes"][0]["value"]["messages"][
        0
    ]["from"]
    name = whatsappData["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"][
        "name"
    ]
    wa_id = whatsappData["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
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
