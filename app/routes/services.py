from fastapi import APIRouter, HTTPException, Request
from supabase import Client

router = APIRouter()


@router.get("/{chatbot_id}")
async def get_services(request: Request):
    supabase = request.state.supabase
    chatbot_id = request.path_params["chatbot_id"]
    response = (
        supabase.table("services").select("*").eq("chatbot_id", chatbot_id).execute()
    )
    return response.data


@router.post("/")
async def create_service(request: Request):
    supabase = request.state.supabase
    body = await request.json()
    service = body["service"]
    response = supabase.table("services").insert(service.dict()).execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]


@router.put("/{service_id}")
async def update_service(req: Request):
    supabase = req.state.supabase
    service_id = req.path_params["service_id"]
    body = await req.json()
    updates = body["service"]
    response = (
        supabase.table("services")
        .update(updates.dict(exclude_unset=True))
        .eq("id", service_id)
        .execute()
    )

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]


@router.delete("/{service_id}")
async def delete_service(request: Request):
    supabase = request.state.supabase
    service_id = request.path_params["service_id"]
    response = supabase.table("services").delete().eq("id", service_id).execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"status": "deleted", "id": service_id}
