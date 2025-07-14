from fastapi import APIRouter, HTTPException
from fastapi import Request

router = APIRouter()


@router.get("/{chatbot_id}")
async def get_calendar(request: Request):
    supabase = request.state.supabase
    chatbot_id = request.path_params["chatbot_id"]
    response = (
        supabase.table("calendar")
        .select("*")
        .eq("chatbot_id", chatbot_id)
        .order("day_of_week")
        .execute()
    )

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data


@router.post("/")
async def create_calendar_entry(request: Request):
    supabase = request.state.supabase
    body = await request.json()
    entry = body["entry"]
    response = supabase.table("calendar").insert(entry.dict()).execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]


@router.put("/{calendar_id}")
async def update_calendar_entry(request: Request):
    supabase = request.state.supabase
    calendar_id = request.path_params["calendar_id"]
    body = await request.json()
    updates = body["entry"]
    response = (
        supabase.table("calendar")
        .update(updates.dict(exclude_unset=True))
        .eq("id", calendar_id)
        .execute()
    )

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]


@router.delete("/{calendar_id}")
async def delete_calendar_entry(request: Request):
    calendar_id = request.path_params["calendar_id"]
    supabase = request.state.supabase
    response = supabase.table("calendar").delete().eq("id", calendar_id).execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"status": "deleted", "id": calendar_id}
