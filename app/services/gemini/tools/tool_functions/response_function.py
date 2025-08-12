from fastapi import Request
from app.services.whatsapp.whatsapp import send_whatsapp_location, send_whatsapp_options


def send_location(request: Request):
    send_whatsapp_location(request.state.form, 37.7749, -122.4194, "איתמר פורר מספרה")
    # send_whatsapp_options(
    #     request.state.form,
    #     "Where would you like to go?",
    #     [
    #         ("main_store", "🏬 Main Store"),
    #         ("outlet", "🛒 Outlet"),
    #         ("nearby_kiosk", "📍 Nearby Kiosk"),
    #     ],
    # )
    return "sent the user the location"
