from fastapi import APIRouter, HTTPException, Request
from app.services.google_calendar.oauth import get_credentials_from_code


router = APIRouter()


@router.post("/token")
async def exchange_code(request: Request):
    db = request.state.supabase
    data = await request.json()
    code = data["code"]
    account_id = data["account_id"]
    chatbot_id = data["chatbot_id"]
    results = get_credentials_from_code(code)
    creds = results["credentials"]
    user_info = results["user_info"]

    scopes = creds.scopes if isinstance(creds.scopes, list) else [creds.scopes]
    expiry = creds.expiry.isoformat() if creds.expiry else None
    result = (
        db.table("google_connections")
        .insert(
            {
                "account_id": account_id,
                "email": user_info["email"],
                "access_token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": scopes,  # Assuming list or set
                "expiry": expiry,
                "chatbot_id": chatbot_id,
            }
        )
        .execute()
    )
    return {
        "message": "Google credentials saved",
        "account_id": account_id,
        "result": result,
    }


@router.delete("/token/{chatbot_id}")
async def delete_token(request: Request):
    chatbot_id = request.path_params["chatbot_id"]
    db = request.state.supabase
    result = (
        db.table("google_connections").delete().eq("chatbot_id", chatbot_id).execute()
    )
    return {"message": "Google credentials deleted", "result": result}
