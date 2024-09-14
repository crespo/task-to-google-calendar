# Task to Google Calendar (Events too ✨)
## Description
This project was initially made for a internship challenge, but I plan to update it and implement new features whenever I feel the mood to do so.

It features a complete CRUD of tasks and events based on Google Calendar standards, also it synchronizes the tasks and events with your personal Google Calendar agenda, so when you create and delete a individual task or event, it'll be required to login with a Google account and then the API will create the task for you automatically.
## Tech Stack
To achieve all of this, it was used Python as the base programming language, Django and Django Rest Framework (a.k.a. DRF) as frameworks to help building the API and [Google Calendar API](https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/index.html) and [Google Tasks API](https://developers.google.com/resources/api-libraries/documentation/tasks/v1/python/latest/index.html) with all the JWT authentication necessary to integrate with Google's endpoints.
## Installation
### Requirements
| Resource | Link | Recommended Version |
| :------: | :--: | :-----: |
| Python | [Python's official download page](https://www.python.org/downloads/) | 3.12+ |
| Pip | [Pip's official documentation](https://pip.pypa.io/en/stable/installation/) | 24.2+ |
| Git | [Git's official download page](https://git-scm.com/downloads) | any |
### Install
Open a ``````Terminal`````` instance and then follow the steps below:
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
After succesfully running the server, do the [Set up your environment](https://developers.google.com/calendar/api/quickstart/python#set-up-environment) tutorial from Google's API activation tutorial and import the credentials.json to both ```./taskmaker/api/creds/google-calendar/``` and ```./taskmaker/api/creds/google-tasks/``` directories and you're good to go!
