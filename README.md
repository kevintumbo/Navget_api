# Navyget E-commerce Api

---

## Navyget - Find what you are looking for

---

This is an python/flask project for an ecommerce app

This ecommerce app is meant to help link Small Business Owners (SME's) and Customers

This project will act as a platform that will enable business users establish a social presence at a minimum cost

---

### How to Install

----

clone the repo

cd into the repo abd checkout to the master branch

create an isolated virtual environment

install the dependancies via pip install -r requirements.txt

create a .env file and add the following.

```
source name-of-virtual-env/bin/activate
export FLASK_APP="run.py" 
export SECRET="some-random-stuff-the-more-complicated-the-better"
export APP_SETTINGS="development"

```

#### Setting up the Database and Migrations

---

to run the migrations:

```
* python manage.py db init
* python manage.py db migrate
* python manage.py db upgrade
* flask run

```

### To run tests

----

```
* nosetests--with-coverage
```

This will return the number of tests run and the test coverage

## Author

---

```
* Kevin Mbugua Tumbo

```