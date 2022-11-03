# Kanban backend built with Django Rest Framework

Boards. Agile, scrum, travel itineraries, whatever you want.

The frontend, built with Vue, is in [this repo](https://github.com/FirstPrinciplesDevelopment/kanban-vue).

# Setup to run locally,

### clone this repository

`git clone https://github.com/mellkior/kanban.git`

### create and activate virtual environment (optional, recommended)

Create a virtual environment in the project root
`python -m venv env`

Activate the environment
Mac OS or Linux:
`source env/bin/activate`
Windows:
`env\Scripts\activate`

### install dependencies

`pip install -r requirements.txt`

### create sqlite database and schema

django does this for us with a single command
`manage.py migrate`

### create an admin user (superuser)

`manage.py createsuperuser`

### set environment variables

set DEBUG = "True" and SECRET_KEY = "a_long_random_string"

### run the development server

`manage.py runserver`

### Troubleshooting

If you get a "Bad Request (400)" when you visit http://127.0.0.1:8000/, you probably didn't set `DEBUG=True`.
In bash, use `export DEBUG=True` before running `manage.py runserver`. In Windows command prompt, use `set DEBUG=True`. Alternatively, you can edit settings.py.
