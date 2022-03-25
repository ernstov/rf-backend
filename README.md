# rainforest-backend

## Getting started

To clone repository on your local machine, please follow these steps:

```
git clone https://gitlab.com/lambospeed/rainforest-backend
cd rainforest-backend
```

## Setting up the project
Create a virtualenvironment, activate it, and install project requirements dependencies.
```
$ pip install virtualenv
$ virtualenv <name of your environment>
$ source <name of your environment>/bin/activate
$ pip install -r requirements.txt
```
Create a `.env` file while copying the contents from the `.env.example` file.
```
cp .env.example .env
```
And finally we need to migrate the database. So, for this run command:
```
$ python manage.py migrate
```

## Usage

```
$ python manage.py runserver
```

## APIs Docs:
For Swagger API documentation visit: `http://localhost:8000/api-docs`