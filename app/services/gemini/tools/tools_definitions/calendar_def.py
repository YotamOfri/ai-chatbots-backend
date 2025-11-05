from app.services.gemini.tools.tool_functions.calendar_functions import (
    create_calendar_event,
    get_upcoming_events,
    update_calendar_event,
    delete_calendar_event,
    get_events_by_date,
    find_available_slot,
)

calendar_functions = {
    "create_event": {
        "description": "Creates a new calendar event. Before using this tool, check for existing events at the requested time using the 'check_availability' tool.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Title of the event",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the event",
                },
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Start time in ISO 8601 format (e.g., 2025-07-10T15:00:00+03:00)",
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "End time in ISO 8601 format (e.g., 2025-07-10T16:00:00+03:00)",
                },
            },
            "required": ["summary", "description", "start_time", "end_time"],
        },
        "fetcher": create_calendar_event,
    },
    "get_events_by_date": {
        "description": "Retrieves a list of upcoming events from the user's calendar.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Date in ISO 8601 format (e.g., 2025-07-10)",
                },
            },
            "required": [
                "date",
            ],
        },
        "fetcher": get_events_by_date,
    },
    "update_event": {
        "description": "Updates an existing calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to update",
                },
                "summary": {
                    "type": "string",
                    "description": "New title for the event (optional)",
                },
                "description": {
                    "type": "string",
                    "description": "New description for the event (optional)",
                },
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "New start time in ISO 8601 format (optional)",
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "New end time in ISO 8601 format (optional)",
                },
                "timezone": {
                    "type": "string",
                    "description": "Timezone of the event (default is 'Asia/Jerusalem')",
                    "default": "Asia/Jerusalem",
                },
            },
            "required": ["event_id"],
        },
        "fetcher": update_calendar_event,
    },
    "delete_event": {
        "description": "Deletes a calendar event by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The ID of the event to delete",
                },
            },
            "required": ["event_id"],
        },
        "fetcher": delete_calendar_event,
    },
    "check_availability": {
        "description": "Checks if a specific date is available for a calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "desired_datetime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Date in ISO 8601 format (e.g., 2025-07-10)",
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Duration of the event in minutes according to type of service",
                },
            },
            "required": ["desired_datetime", "duration_minutes"],
        },
        "fetcher": find_available_slot,
    },
}
