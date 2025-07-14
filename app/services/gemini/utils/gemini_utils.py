import google
import time


async def send_message_with_retry(chat, user_input, max_retries=3, initial_delay=1):

    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return chat.send_message(user_input)
        except google.genai.errors.ServerError as e:
            if e.status_code == 503:
                print(
                    f"Attempt {attempt + 1}/{max_retries}: Model overloaded. Retrying in {delay} seconds..."
                )
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise
    raise Exception("Max retries reached. The model is still overloaded.")
