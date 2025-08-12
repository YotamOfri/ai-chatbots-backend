from googleapiclient.errors import HttpError
import datetime
import pytz
from app.services.google_calendar.index import get_calendar_service
from dateutil.parser import isoparse
from fastapi import Request
from dateutil import parser
from app.services.whatsapp.whatsapp import send_whatsapp_message


async def create_calendar_event(
    summary,
    description,
    start_time,
    end_time,
    timezone="Asia/Jerusalem",
    request: Request = None,
):
    form = request.state.form
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
        start_dt = parser.isoparse(event.get("start").get("dateTime"))
        formatted_time = start_dt.strftime("%H:%M")
        formatted_day = start_dt.strftime("%A")

        hebrew_days = {
            "Sunday": "ראשון",
            "Monday": "שני",
            "Tuesday": "שלישי",
            "Wednesday": "רביעי",
            "Thursday": "חמישי",
            "Friday": "שישי",
            "Saturday": "שבת",
        }
        hebrew_day = hebrew_days.get(formatted_day, formatted_day)

        print(f"Event created: {event.get('htmlLink')}")

        if event:
            event_created_message = (
                f"*נוצר תור*\n{event.get('summary')}:{formatted_time} ({hebrew_day})"
            )
            send_whatsapp_message(
                "whatsapp:+972585120704",
                form.get("To"),
                event_created_message,
            )

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
        event_id (str): The ID of the event to delete.

    Returns:
        bool: True if the event was deleted successfully, False otherwise.
    """
    try:
        service = await get_calendar_service(request)

        # First, get the event details before deleting
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        summary = event.get("summary", "ללא נושא")
        start_dt_str = event.get("start", {}).get("dateTime")

        if start_dt_str:
            start_dt = parser.isoparse(start_dt_str)
            formatted_time = start_dt.strftime("%H:%M")
            message = f"*נמחק תור*\n{summary}:{formatted_time}"
        else:
            message = f"*נמחק תור*\n{summary}"

        # Delete the event
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"Event with ID '{event_id}' deleted successfully.")

        # Optional: Send WhatsApp message
        form = getattr(request.state, "form", None)
        if form:
            send_whatsapp_message(
                "whatsapp:+972585120704",
                form.get("To"),
                message,
            )

        return True

    except HttpError as error:
        print(f"An error occurred while deleting the event: {error}")
        return False


async def find_available_slot(
    desired_datetime,
    duration_minutes,
    search_window=120,
    request: Request = None,
):
    """
    Checks if a slot is available. If not, suggests the nearest available slot that fits the duration.

    Args:
        desired_datetime (str or datetime.datetime): Desired start datetime.
        duration_minutes (int): Length of appointment.
        request (Request): FastAPI request.
        search_window (int): Minutes to look around the desired time.

    Returns:
        dict: {
            "available": bool,
            "suggested": Optional[{"start": str, "end": str}],
            "conflicts": list
        }
    """
    if isinstance(desired_datetime, str):
        desired_datetime = isoparse(desired_datetime)

    timezone = pytz.UTC if desired_datetime.tzinfo is None else desired_datetime.tzinfo
    desired_datetime = desired_datetime.astimezone(timezone)
    desired_end = desired_datetime + datetime.timedelta(minutes=duration_minutes)

    try:
        service = await get_calendar_service(request)

        time_min = (
            desired_datetime - datetime.timedelta(minutes=search_window)
        ).isoformat()
        time_max = (desired_end + datetime.timedelta(minutes=search_window)).isoformat()

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # Convert events to sorted list of (start, end)
        busy = sorted(
            [
                (
                    isoparse(
                        e["start"].get("dateTime", e["start"].get("date"))
                    ).astimezone(timezone),
                    isoparse(e["end"].get("dateTime", e["end"].get("date"))).astimezone(
                        timezone
                    ),
                )
                for e in events
            ],
            key=lambda x: x[0],
        )

        # 1️⃣ Check if desired slot fits
        def slot_fits(start, end, busy_blocks):
            return not any(
                max(start, b_start) < min(end, b_end) for b_start, b_end in busy_blocks
            )

        if slot_fits(desired_datetime, desired_end, busy):
            return {
                "available": True,
                "suggested": {
                    "start": desired_datetime.isoformat(),
                    "end": desired_end.isoformat(),
                },
                "conflicts": [],
            }

        # 2️⃣ Find nearest available slot
        # We'll scan from timeMin to timeMax, looking for gaps between events

        # Add boundaries at beginning and end
        search_start = desired_datetime - datetime.timedelta(minutes=search_window)
        search_end = desired_end + datetime.timedelta(minutes=search_window)
        blocks = [(search_start, search_start)] + busy + [(search_end, search_end)]

        for i in range(len(blocks) - 1):
            gap_start = blocks[i][1]
            gap_end = blocks[i + 1][0]

            available_duration = (gap_end - gap_start).total_seconds() / 60
            if available_duration >= duration_minutes:
                # Found a suitable gap
                if gap_start >= desired_datetime:
                    data = {
                        "available": False,
                        "suggested": {
                            "start": gap_start.isoformat(),
                            "end": (
                                gap_start + datetime.timedelta(minutes=duration_minutes)
                            ).isoformat(),
                        },
                        "conflicts": [
                            {"start": s.isoformat(), "end": e.isoformat()}
                            for s, e in busy
                        ],
                    }
                    print(data, "Appointments found")
                    return data

        return {
            "available": False,
            "suggested": None,
            "conflicts": [
                {"start": s.isoformat(), "end": e.isoformat()} for s, e in busy
            ],
        }

    except HttpError as error:
        print(f"Error while checking availability: {error}")
        return {"available": False, "error": str(error), "suggested": None}
