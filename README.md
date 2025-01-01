# Getting Started with project

### `cd csv-processing`

if environment setup is needed, run:

### `python -m venv env`

for activating virtual environment, run:

### `env/Scripts/activate`

install requirements.txt for required dependencies

### `pip install -r requirements.txt`

if migration not applied run:

### `python manage.py migrate`

After run backend application:

### `python manage.py runserver`

The project will run in "http://127.0.0.1:8000"

For Unit testing:

### `python manage.py test`

Sample input file and sample output file are attached in the project root directory.

For handling large csv input data we can optimize the process by using ###`Celery` and run the task in background. Am aware of the performance, Since this is a demonstration we can keep it simple. On production level definetly we will work along with performance based structure.
