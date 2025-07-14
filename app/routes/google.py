from fastapi import APIRouter, HTTPException, Request
from app.services.google_calendar.oauth import get_credentials_from_code


router = APIRouter()


@router.post("/token")
async def exchange_code(request: Request):
    data = await request.json()
    code = data["code"]
    account_id = data["account_id"]  # Make sure this is sent from frontend

    results = get_credentials_from_code(code)

    creds = results["credentials"]
    user_info = results["user_info"]
    print(creds.to_json(), "creds")
    print(user_info, "user_info")
    db = request.state.supabase

    scopes = creds.scopes if isinstance(creds.scopes, list) else [creds.scopes]

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
                "scopes": scopes,
            }
        )
        .execute()
    )
    return {
        "message": "Google credentials saved",
        "account_id": account_id,
    }
