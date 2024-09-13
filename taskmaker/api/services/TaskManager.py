import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/tasks"]


class TaskManager:
    def authenticate():
        creds = None
        token_path = "./api/creds/google-tasks/token.json"
        creds_path = "./api/creds/google-tasks/credentials.json"
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        return creds

    def deleteTask(task_id):
        creds = TaskManager.authenticate()

        try:
            service = TaskManager.buildService(creds)

            service.tasks().delete(
                tasklist=TaskManager.getFirstTasklistID(creds), task=task_id
            ).execute()

            return "Task with: " + task_id + " has been deleted succesfully."
        except HttpError as err:
            return err

    def createTask(task):
        creds = TaskManager.authenticate()

        try:
            service = TaskManager.buildService(creds)

            response = (
                service.tasks()
                .insert(
                    tasklist=TaskManager.getFirstTasklistID(creds),
                    body={
                        "title": task.titulo,
                        "notes": task.descricao,
                        "due": task.data + "T00:00:00.00Z",
                    },
                )
                .execute()
            )

            return response

        except HttpError as err:
            return err

    def getFirstTasklistID(creds):
        try:
            service = TaskManager.buildService(creds)

            results = service.tasklists().list(maxResults=10).execute()
            tasklists = results.get("items", [])

            return tasklists[0]["id"]

        except HttpError as err:
            return err

    def buildService(creds):
        return build("tasks", "v1", credentials=creds)


class TaskBuilder:
    def __init__(self, title, date, notes=None, time=None):
        self.title = title
        self.date = date
        self.notes = notes
        self.time = time
