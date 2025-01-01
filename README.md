# Getting Started with project

The project consit of functionality to extract user data from csv file and insert in to User table. We can expect a summarised result as response total records saved. total records rejected and error messages of rejected records.
Apart from that also implemented a custom middleware for rate limiting the request based on client ip address. This is to protect the backend server from attacks like spamming multiple request to the server. Through this i have demonstrated how a custom middleware is created and its set up.

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

For handling large csv input data we can optimize the process by using `Celery` and run the task in background. Am aware of the performance, Since this is a demonstration we can keep it simple. On production level definetly we will work along with performance based structure.
