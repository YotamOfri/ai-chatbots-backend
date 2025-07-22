from googleapiclient.errors import HttpError
import datetime
from app.services.google_calendar.index import get_calendar_service
from dateutil.parser import isoparse
from fastapi import Request


async def create_calendar_event(
    summary,
    description,
    start_time,
    end_time,
    timezone="Asia/Jerusalem",
    request: Request = None,
):
    service = await get_calendar_service(request)
    print("Creating a new calendar event...")

    # Parse strings to datetime if needed
    if isinstance(start_time, str):
        start_time = isoparse(start_time)
    if isinstance(end_time, str):
        end_time = isoparse(end_time)

    description = description or "No description provided"

    print(
        f"Summary: {summary} Description: {description} Start Time: {start_time} End Time: {end_time} Timezone: {timezone}"
    )

    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": timezone,
        },
    }

    try:
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        return event
    except HttpError as error:
        print(f"An error occurred while creating the event: {error}")
        return None


async def get_upcoming_events(max_results=10, request: Request = None):
    print("Retrieving upcoming events from Google Calendar...")
    """
    Retrieves upcoming events from the user's Google Calendar.

    Args:
        service: The authenticated Google Calendar API service object.
        max_results (int): The maximum number of events to retrieve.

    Returns:
        list: A list of upcoming event resources, or None if an error occurred.
    """
    try:

        service = await get_calendar_service(request)
        if not service:
            print("Calendar service is not initialized.")
            return None
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print(f"Getting the upcoming {max_results} events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []
        return events
    except HttpError as error:
        print(f"An error occurred while retrieving events: {error}")
        return None


async def get_event_by_id(event_id, request: Request = None):
    try:
        service = await get_calendar_service(request)
        event = service.events().get(calendarId="primary", eventId=event_id).execute()
        return event
    except HttpError as error:
        print(f"An error occurred while retrieving the event: {error}")
        return None


async def get_events_by_date(date, max_results=10, request: Request = None):
    """
    Retrieves events from the user's Google Calendar for a specific date.

    Args:
        date (datetime.date): The date for which to retrieve events.
        max_results (int): The maximum number of events to retrieve.

    Returns:
        list: A list of event resources for the specified date, or None if an error occurred.
    """
    if isinstance(date, str):
        date = isoparse(date)

    print(
        f"Retrieving events for date: {date.isoformat()} with max results: {max_results}"
    )
    try:
        service = await get_calendar_service(request)
        start_of_day = (
            datetime.datetime.combine(date, datetime.time.min).isoformat() + "Z"
        )
        end_of_day = (
            datetime.datetime.combine(date, datetime.time.max).isoformat() + "Z"
        )
        print(f"Start of day: {start_of_day} End of day: {end_of_day}")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_of_day,
                timeMax=end_of_day,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        print(events_result)
        events = events_result.get("items", [])
        print(events, "events")
        return events
    except HttpError as error:
        print(f"An error occurred while retrieving events: {error}")
        return None


async def update_calendar_event(
    event_id,
    summary=None,
    description=None,
    start_time=None,
    end_time=None,
    timezone="Asia/Jerusalem",
    request: Request = None,
):
    """
    Updates an existing event on the user's Google Calendar.

    Args:
        event_id (str): The ID of the event to update.
        summary (str, optional): The new summary/title of the event.
        description (str, optional): The new description of the event.
        start_time (datetime.datetime, optional): The new start time of the event.
        end_time (datetime.datetime, optional): The new end time of the event.
        timezone (str): The timezone for the event (e.g., "Asia/Jerusalem").

    Returns:
        dict: The updated event resource, or None if an error occurred.
    """
    try:
        service = await get_calendar_service(request)
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        if summary:
            event["summary"] = summary
        if description:
            event["description"] = description
        if start_time:
            event["start"] = {
                "dateTime": start_time.isoformat(),
                "timeZone": timezone,
            }
        if end_time:
            event["end"] = {
                "dateTime": end_time.isoformat(),
                "timeZone": timezone,
            }

        updated_event = (
            service.events()
            .update(calendarId="primary", eventId=event_id, body=event)
            .execute()
        )
        print(f"Event updated: {updated_event.get('htmlLink')}")
        return updated_event
    except HttpError as error:
        print(f"An error occurred while updating the event: {error}")
        return None


async def delete_calendar_event(event_id, request: Request = None):
    """
    Deletes an event from the user's Google Calendar.

    Args:
        service: The authenticated Google Calendar API service object.
        event_id (str): The ID of the event to delete.

    Returns:
        bool: True if the event was deleted successfully, False otherwise.
    """
    try:
        service = await get_calendar_service(request)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"Event with ID '{event_id}' deleted successfully.")
        return True
    except HttpError as error:
        print(f"An error occurred while deleting the event: {error}")
        return False
