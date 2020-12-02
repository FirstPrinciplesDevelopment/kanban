# kanban
Boards. Agile, scrum, travel itineraries, whatever you want.

# Setup to run locally, 
### clone this repository
`git clone https://github.com/mellkior/kanban.git`

### create and activate virtual environment (optional, recommended)

Install virtualenv if not installed
`pip install virtualenv`

Create a virtual environment in the project root
`python -m virtualenv env`

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
set DEBUG = "True" and SECRET_KEY = "<a long random string>"

### run the development server
`manage.py runserver`