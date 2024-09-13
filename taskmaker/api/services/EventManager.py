import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class EventManager:
    def authenticate():
        creds = None
        TOKEN_PATH = "./api/creds/google-calendar/token.json"
        CREDS_PATH = "./api/creds/google-calendar/credentials.json"

        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

        return creds

    def deleteEvent(event_id):
        creds = EventManager.authenticate()

        try:
            service = EventManager.buildService(creds)

            service.events().delete(calendarId="primary", eventId=event_id).execute()

            return "Event with: " + event_id + " has been deleted successfully."
        except HttpError as err:
            return err

    def buildTime(date, time=None):
        if time is None:
            return {"tag": "date", "content": date}

        return {"tag": "dateTime", "content": date + "T" + time}

    def createEvent(event):
        creds = EventManager.authenticate()

        try:
            service = EventManager.buildService(creds)

            time = EventManager.buildTime(event.date, event.time)

            response = (
                service.events()
                .insert(
                    calendarId="primary",
                    body={
                        "summary": event.summary,
                        "start": {time["tag"]: time["content"]},
                        "end": {time["tag"]: time["content"]},
                        "description": event.description,
                    },
                )
                .execute()
            )

            return response

        except HttpError as err:
            print(err)
            return err

    def buildService(creds):
        return build("calendar", "v3", credentials=creds)


class EventBuilder:
    def __init__(self, summary, date, description=None, time=None):
        self.summary = summary
        self.date = date
        self.description = description
        self.time = time
