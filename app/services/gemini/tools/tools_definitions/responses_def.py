from app.services.gemini.tools.tool_functions.response_function import send_location


response_function = {
    "location_response": {
        "description": "Sends the user the location",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "fetcher": send_location,
        "type": "custom_response",
    }
}
