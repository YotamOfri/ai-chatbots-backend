from fastapi import Request
from app.services.whatsapp.whatsapp import send_whatsapp_location


def send_location(request: Request):
    send_whatsapp_location(request.state.form, 37.7749, -122.4194, "Our Shop")
    return "sent the user the location"
