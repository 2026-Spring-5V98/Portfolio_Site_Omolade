import datetime
import json
import logging
import os

logger = logging.getLogger(__name__)

_SCOPES = ['https://www.googleapis.com/auth/calendar']


def _get_service():
    from django.conf import settings
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        return None, None

    try:
        creds_json = os.environ.get('GCAL_CREDENTIALS_JSON', '')
        if creds_json:
            # Render deployment: credentials stored as JSON env var
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(creds_json), scopes=_SCOPES,
            )
        else:
            # Local development: credentials stored as a file
            creds_path = getattr(settings, 'GCAL_CREDENTIALS_PATH', '')
            if not creds_path:
                return None, None
            credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=_SCOPES,
            )
        service = build('calendar', 'v3', credentials=credentials)
        calendar_id = getattr(settings, 'GCAL_CALENDAR_ID', 'primary')
        return service, calendar_id
    except Exception:
        logger.exception("Google Calendar: failed to build service")
        return None, None


def create_event(appointment):
    """Create a calendar event for an approved appointment. Returns event ID or None."""
    from django.conf import settings
    service, calendar_id = _get_service()
    if not service:
        return None

    tz = getattr(settings, 'GCAL_TIMEZONE', 'UTC')
    start_dt = datetime.datetime.combine(appointment.date, appointment.time)
    end_dt = start_dt + datetime.timedelta(hours=1)

    event = {
        'summary': f"Appointment: {appointment.purpose}",
        'description': (
            f"Booked by: {appointment.name}\n"
            f"Email: {appointment.email}\n"
            f"Phone: {appointment.phone or '—'}\n\n"
            f"Notes:\n{appointment.message or '—'}"
        ),
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': tz},
        'end':   {'dateTime': end_dt.isoformat(),   'timeZone': tz},
        'attendees': [{'email': appointment.email, 'displayName': appointment.name}],
        'reminders': {'useDefault': True},
    }

    try:
        result = service.events().insert(
            calendarId=calendar_id,
            body=event,
            sendUpdates='all',
        ).execute()
        return result.get('id')
    except Exception:
        logger.exception("Google Calendar: failed to create event")
        return None


def delete_event(event_id):
    """Delete a calendar event by its ID (used when an approval is reversed)."""
    if not event_id:
        return
    service, calendar_id = _get_service()
    if not service:
        return
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    except Exception:
        logger.exception("Google Calendar: failed to delete event %s", event_id)
