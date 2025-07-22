from app.services.gemini.utils.gemini_utils import send_message_with_retry
from app.services.gemini.tools.function_executor import process_function_calls
from fastapi import Request
from app.utils.twillo import extract_message

# from global_types.whatsapptypes import WhatsAppWebhookData


async def response_handler(chat, form, request: Request):

    parsed_message = extract_message(form)
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
