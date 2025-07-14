from app.services.gemini.utils.gemini_utils import send_message_with_retry
from app.services.gemini.tools.function_executor import process_function_calls
from fastapi import Request

# from global_types.whatsapptypes import WhatsAppWebhookData


async def response_handler(chat, message, request: Request):
    if (
        not message
        or "entry" not in message
        or "changes" not in message["entry"][0]
        or "value" not in message["entry"][0]["changes"][0]
        or "messages" not in message["entry"][0]["changes"][0]["value"]
        or "text" not in message["entry"][0]["changes"][0]["value"]["messages"][0]
        or "body"
        not in message["entry"][0]["changes"][0]["value"]["messages"][0]["text"]
    ):
        print("❌ Invalid message format received:")
        return None
    parsed_message = message["entry"][0]["changes"][0]["value"]["messages"][0]["text"][
        "body"
    ]
    print("🔔 Incoming WhatsApp Message:", parsed_message)
    response_text = None
    latest_response = await send_message_with_retry(
        chat,
        parsed_message,
    )
    while True:
        if latest_response.function_calls:
            try:
                function_responses = await process_function_calls(
                    latest_response.function_calls, request
                )
                latest_response = await send_message_with_retry(
                    chat, function_responses
                )
            except Exception as e:
                response_text = f"Error during function execution: {e}"
                break
        elif latest_response.text:
            response_text = latest_response.text
            break
        else:
            response_text = "No interpretable response from Gemini."
            break
    return response_text
