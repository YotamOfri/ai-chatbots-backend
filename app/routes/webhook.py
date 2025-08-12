from fastapi import APIRouter, Request, Query, Response, HTTPException
import asyncio
from app.services.gemini.client import start_chat
from app.core.config import settings
from app.services.supabase.customers import update_customer_if_exists
from app.services.supabase.chatbots import get_chatbot
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("")
async def verify_webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.FACEBOOK_VERIFY_TOKEN"),
    challenge: str = Query(..., alias="hub.challenge"),
):
    if mode == "subscribe" and token == settings.FACEBOOK_VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("")
async def receive_message(request: Request):
    try:
        # Twilio sends data as application/x-www-form-urlencoded
        form = await request.form()
        print("📫 WhatsApp Message Received", form)
        request.state.form = form
        # Extract useful fields
        from_number = form.get("From")
        body = form.get("Body")

        print("✅ WhatsApp Message Received")
        print(f"From: {from_number}")
        print(f"Message: {body}")

        # Pass the form data (or dict) to your handlers
        get_chatbot(request)
        print("🚀 Starting chatbot...")
        update_customer_if_exists(request)
        print("✅ Customer updated in Supabase")
        response = await asyncio.create_task(start_chat(request))  # runs in background

        return JSONResponse(content={"status": "success", "detail": response})

    except Exception as e:
        print("❌ Error handling webhook:", str(e))
        return JSONResponse(
            status_code=500, content={"status": "error", "detail": str(e)}
        )
