import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks"]


class TaskManager:
    def authenticate():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            TaskManager.creds = Credentials.from_authorized_user_file(
                "token.json", SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    def deleteTask(taskId):
        creds = TaskManager.authenticate()

        try:
            service = build("tasks", "v1", credentials=creds)

            service.tasks().delete(
                tasklist=TaskManager.getFirstTasklistID(), task=taskId
            ).execute()

        except HttpError as err:
            print(err)

    def createTask(task):
        TaskManager.authenticate()

        try:
            service = build("tasks", "v1", credentials=TaskManager.creds)

            addTaskResponse = (
                service.tasks()
                .insert(
                    tasklist=TaskManager.getFirstTasklistID(),
                    body={
                        "title": task.titulo,
                        "notes": task.descricao,
                        "due": task.buildDate(),
                    },
                )
                .execute()
            )

            print(addTaskResponse)

        except HttpError as err:
            print(err)

    def getFirstTasklistID():
        try:
            service = build("tasks", "v1", credentials=TaskManager.creds)

            results = service.tasklists().list(maxResults=10).execute()
            tasklists = results.get("items", [])

            return tasklists[0]["id"]

            # taskGroups = []
            # for tasklist in tasklists:
            #     results = service.tasks().list(tasklist=tasklist["id"]).execute()
            #     taskGroup = results.get("items", [])
            #     taskGroups.append(taskGroup)

            # individualTasks = []

            # for taskGroup in taskGroups:
            #     for task in taskGroup:
            #         individualTasks.append({"id": task["id"], "task": task["title"]})

            # print(individualTasks)

        except HttpError as err:
            print(err)


class Task:
    def __init__(self, titulo, data, descricao=None, horario=None):
        self.titulo = titulo
        self.data = data
        self.descricao = descricao
        self.horario = horario
