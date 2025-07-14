import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
import datetime
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


async def get_calendar_service():
    # account_id = body["account_id"]
    account_id = "412d2267-a604-499c-909f-d54d67d2abe9"
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    # Fetch credentials data from Supabase (sync call, no await)
    response = (
        supabase.table("google_connections")
        .select("*")
        .eq("account_id", account_id)
        .single()
        .execute()
    )
    if not response.data:
        print("No credentials found for this account")
        return None
    creds_data = response.data
    creds = Credentials(
        token=creds_data["access_token"],
        refresh_token=creds_data["refresh_token"],
        token_uri=creds_data["token_uri"],
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        scopes=creds_data["scopes"],
    )
    # Refresh the token if expired or close to expire
    if not creds.valid or (
        creds.expiry
        and creds.expiry < datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    ):
        try:
            request_adapter = GoogleRequest()
            creds.refresh(request_adapter)

            # Update the refreshed tokens in Supabase
            update_response = (
                supabase.table("google_connections")
                .update(
                    {
                        "access_token": creds.token,
                        "refresh_token": creds.refresh_token,  # usually unchanged, but good to update anyway
                        "expiry": creds.expiry.isoformat() if creds.expiry else None,
                    }
                )
                .eq("account_id", account_id)
                .execute()
            )
            if update_response.status_code != 200:
                print("Failed to update refreshed tokens in Supabase")

        except RefreshError as e:
            print(f"Failed to refresh token: {e}")
            return None

    try:
        service = build("calendar", "v3", credentials=creds)
        print("Calendar service built successfully")
        return service
    except Exception as e:
        print(f"Failed to build calendar service: {e}")
        return None


async def main():
    service = await get_calendar_service()
    print(service)


if __name__ == "__main__":
    asyncio.run(main())
