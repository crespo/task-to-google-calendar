# Task to Google Calendar (Events too ✨)
## Description
This project was initially made for a internship challenge, but I plan to update it and implement new features whenever I feel in the mood to do so.

It features a complete CRUD of tasks and events based on Google Calendar standards, also it synchronizes the tasks and events with your personal Google Calendar agenda, so when you create and delete a individual task or event, it'll be required to login with a Google account and then the API will create the task for you automatically.
## Tech Stack
To achieve all of this, it was used Python as the base programming language, Django and Django Rest Framework (a.k.a. DRF) as frameworks to help building the API, [Google Calendar API](https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/index.html) and [Google Tasks API](https://developers.google.com/resources/api-libraries/documentation/tasks/v1/python/latest/index.html) with all the JWT authentication necessary to integrate with Google's endpoints and Swagger UI to make a quick beautiful API documentation page.
## Installation
### Requirements
| Resource | Link | Recommended Version |
| :------: | :--: | :-----: |
| Python | [Python's official download page](https://www.python.org/downloads/) | 3.12+ |
| Pip | [Pip's official documentation](https://pip.pypa.io/en/stable/installation/) | 24.2+ |
| Git | [Git's official download page](https://git-scm.com/downloads) | any |
### Install
Open a ```Terminal``` instance and then follow the steps below:
```bash
git clone https://github.com/crespo/task-to-google-calendar.git
cd task-to-google-calendar/
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
cd taskmaker/
python3 manage.py makemigrations api
python3 manage.py migrate api
python3 manage.py runserver
```
After succesfully running the server, do the [Set up your environment](https://developers.google.com/calendar/api/quickstart/python#set-up-environment) tutorial from Google's API activation tutorial and import the ```credentials.json``` to both ```./taskmaker/api/creds/google-calendar/``` and ```./taskmaker/api/creds/google-tasks/``` directories and you're good to go!
## Usage
You can check [localhost:8000/swagger/](http://localhost:8000/swagger/) to see available endpoints.

```POST``` example to ```/api/v1/events/``` endpoint:
```json
{
  "summary": "This will be the title of the event",
  "date": "2024-09-14",
  "description": "This will represent the event's description",
  "time_start": "08:00:00.00-0300",
  "time_end": "08:30:00.00-0300"
}
```
- The ```description```, ```time_start``` and ```time_end``` fields are optionals.
- ```date``` field should accept ```yyyy-mm-dd``` format.
- ```time_start``` and ```time_end``` should accept [RFC3339](https://www.rfc-editor.org/rfc/rfc3339) format where ```-0300``` in the example above represents the GMT -3 timezone.

```POST``` example to ```/api/v1/tasks/``` endpoint:
```json
{
  "title": "This will be the title of the task",
  "date": "2024-09-14",
  "notes": "This will represent the task's description",
  "time": "08:00:00.00-0300"
}
```
- The ```notes``` and ```time``` fields are optionals.
- ```date``` field should accept ```yyyy-mm-dd``` format.
- Note that even though ```time``` field is implemented in this API, it doesn't work. It's there just for a possible future update of Google Tasks' API. [See the reason here](https://issuetracker.google.com/issues/166896024).

| ```GET``` examples to filter by text: |
| :------------------------------------ |
| ```{...}/api/v1/events?search=example``` |
| ```{...}/api/v1/tasks?search=example``` |


| ```GET``` examples to filter by date: |
| :------------------------------------ |
| ```{...}/api/v1/events/{start_date}/{end_date}/``` |
| ```{...}/api/v1/tasks/{start_date}/{end_date}/``` |
| PS.: Dates takes the form of ```yyyy-mm-dd```. |
