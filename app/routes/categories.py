from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


@router.get("/")
async def get_categories(request: Request):
    supabase = request.state.supabase
    response = supabase.table("categories").select("*").execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data


@router.post("/")
async def create_category(request: Request):
    supabase = request.state.supabase
    body = await request.json()
    category = body["category"]
    response = supabase.table("categories").insert(category).execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]


@router.put("//{category_id}")
async def update_category(request: Request, category_id: int):
    supabase = request.state.supabase
    body = await request.json()
    updates = body["category"]
    response = (
        supabase.table("categories").update(updates).eq("id", category_id).execute()
    )

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data[0]


@router.delete("//{category_id}")
async def delete_category(request: Request, category_id: int):
    supabase = request.state.supabase
    response = supabase.table("categories").delete().eq("id", category_id).execute()

    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"status": "deleted", "id": category_id}
