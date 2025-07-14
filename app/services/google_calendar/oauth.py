import requests
from google_auth_oauthlib.flow import Flow
from app.core.config import settings


def get_credentials_from_code(code: str):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=settings.GOOGLE_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )
    flow.fetch_token(code=code)
    creds = flow.credentials

    # Fetch email from userinfo endpoint
    headers = {"Authorization": f"Bearer {creds.token}"}
    resp = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo", headers=headers
    )
    if resp.status_code != 200:
        raise Exception("Failed to fetch user info")

    user_info = resp.json()
    return {
        "credentials": creds,
        "user_info": {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
        },
    }
