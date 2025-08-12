from app.services.gemini.constants.prompt import SYSTEM_PROMPT
from app.services.gemini.constants.gemini_config import client
from app.services.gemini.response_handler import response_handler
from app.services.gemini.tools.tools_definitions.index import tools
from app.services.whatsapp.whatsapp import send_whatsapp_message
import json
from pathlib import Path
from google.genai import types
from fastapi import Request

CHAT_HISTORY_PATH = Path("chat_history.json")


# Helper function to convert Gemini Part to dict
def part_to_dict(part):
    if hasattr(part, "text") and part.text:
        return {"text": part.text}
    elif isinstance(part, dict) and "text" in part:
        return {"text": part["text"]}
    # Ignore invalid or empty parts
    return None


# Load function
def load_chat_history():
    if CHAT_HISTORY_PATH.exists():
        try:
            with open(CHAT_HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Chat history JSON is corrupted.")
    return []


# Save function
def save_chat_history(chat_history):
    history_data = []
    for content in chat_history:
        parts = [part_to_dict(part) for part in content.parts]
        # Filter out None parts
        parts = [p for p in parts if p]
        if parts:  # only save if parts are valid
            history_data.append(
                {
                    "role": content.role,
                    "parts": parts,
                }
            )

    with open(CHAT_HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)


async def start_chat(request: Request):
    print("🔔 Incoming Whatsapp Data to StartChat")
    form = request.state.form
    history = load_chat_history()

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=tools,
    )

    chat = client.chats.create(model="gemini-2.5-flash", config=config, history=history)

    final_response = await response_handler(chat, request)
    print("🚀 Final Response:", final_response)
    try:
        save_chat_history(chat.get_history())
    except Exception as e:
        print(f"⚠️ Failed to save chat history: {e}")
    if final_response:
        send_whatsapp_message(
            form.get("From"),
            form.get("To"),
            final_response,
        )

    return final_response


if __name__ == "__main__":
    pass
