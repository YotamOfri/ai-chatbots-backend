from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def get_bots(request: Request):
    supabase = request.state.supabase

    response = supabase.table("chatbots").select("*, google_connections(*)").execute()

    return response.data


@router.post("/")
async def create_bot(request: Request):
    supabase = request.state.supabase
    body = await request.json()
    chatbot = {
        "name": body["name"],
        "location": body["location"],
        "phone_number": body["phone"],
        "account_id": body["account_id"],
    }
    response = supabase.table("chatbots").insert(chatbot).execute()

    return response.data
