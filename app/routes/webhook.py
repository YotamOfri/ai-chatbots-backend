from fastapi import APIRouter, Request, Query, Response, HTTPException
import asyncio
from app.services.gemini.client import start_chat
from app.core.config import settings
from app.services.supabase.customers import update_customer_if_exists
from app.services.supabase.chatbots import get_chatbot

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
        data = await request.json()
        get_chatbot(data, request)
        update_customer_if_exists(data, request)
        asyncio.create_task(start_chat(data, request))
        return {"status": "ok"}
    except Exception as e:
        print("❌ Error handling webhook:", str(e))
        return {"status": "error", "detail": str(e)}
