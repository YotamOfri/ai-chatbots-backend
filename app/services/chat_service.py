from typing import Optional
from google.genai import types
import base64
from datetime import datetime, timezone


def serialize_history(history) -> list:
    """Convert Gemini Content objects to JSON-serializable dicts."""

    def make_json_safe(obj):
        """Recursively convert bytes and complex objects to JSON-safe types."""
        if isinstance(obj, bytes):
            # Convert bytes → base64 string
            return {"__bytes__": base64.b64encode(obj).decode("utf-8")}
        elif isinstance(obj, dict):
            return {k: make_json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_json_safe(v) for v in obj]
        else:
            return obj

    serialized = []
    for item in history:
        if hasattr(item, "model_dump"):
            data = item.model_dump()
        elif hasattr(item, "to_dict"):
            data = item.to_dict()
        elif isinstance(item, dict):
            data = item
        else:
            data = dict(item)

        serialized.append(make_json_safe(data))

    return serialized


def deserialize_history(history_data) -> list:
    """Convert stored JSON back to Gemini Content objects."""
    if not history_data:
        return []

    def restore_bytes(obj):
        if isinstance(obj, dict):
            # Detect base64-encoded bytes
            if "__bytes__" in obj:
                return base64.b64decode(obj["__bytes__"])
            return {k: restore_bytes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [restore_bytes(v) for v in obj]
        return obj

    deserialized = []
    for item in history_data:
        try:
            item = restore_bytes(item)
            content = types.Content(
                parts=[types.Part(**part) for part in item.get("parts", [])],
                role=item.get("role"),
            )
            deserialized.append(content)
        except Exception as e:
            logger.warning(f"Failed to deserialize history item: {e}")
            continue

    return deserialized


def get_chat_history(user_id: Optional[str], request) -> list:

    id = user_id
    supabase = request.state.supabase
    try:
        response = (
            supabase.table("ChatHistory").select("body").eq("id", id).single().execute()
        )

        if response.data and response.data.get("body"):
            history_data = response.data["body"]
            # Deserialize back to Content objects
            history = deserialize_history(history_data)
            return history
        else:
            return []

    except Exception as e:
        return []


def save_chat_history(id, history, request):
    if not id:
        return
    supabase = request.state.supabase
    try:
        serialized_history = serialize_history(history)

        data = {
            "id": id,
            "body": serialized_history,
        }
        response = (
            supabase.table("ChatHistory").upsert(data, on_conflict="id").execute()
        )

        return response.data

    except Exception as e:
        raise
