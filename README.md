# Dashboard Empresarial

This repo is the result of a one week project from platzi master.

## Getting Started

Being a Django project it would be advisable to start by install everything in our requirements.txt. I recommend doing the installation in a virtual environment.
I would recommend to run this first on its own:

    pip install django 

Then

    pip install -r requirements.txt

Or alternatively with:

    pip3 install -r requirements.txt


### Prerequisites

We are using postgreSQL 13 which means that you will need to have it installed in whatever place or environment that you wish to run this project in.
- [Tutorial](https://www.postgresql.org/docs/13/tutorial-install.html)

We are also using postgis which allows us to save location based data in our database.
- [PostGIS](https://postgis.net/install/)

## DB creation and set up

First make sure that your postgres service is runing. 
- [Help](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html)

then access to psql. On ubuntu you can run these commands:

    sudo su - postgres
    psql

Now we should be able to straight up run this:

    CREATE DATABASE 'databasename';

Connect to the database with:

    \c 'databasename';

Let's allow our data base to use PostGIS

    CREATE EXTENSION postgis;

Create a user and grant it full access to the data base 

    create user 'your user' with password 'your password';

    grant all privileges on database 'databasename' to 'your user';


### More prerequisites
If you open the next file /CSVPROYECTO/CSVPROYECTO/settings.py and look at the DATABASES variable you'll notice that We're using .env variables, this file and the variables within it to need to be created by you. 

example of a variable in the .env file: DB_NAME='the name of your data base'

### Installing

Locate yourself in the folder that you have manage.py in and run 

    python manage.py makemigrations

alternatively:

    python3 manage.py makemigrations

Follow that with:

    python3 manage.py makemigrations

Lastly run:

    python3 manage.py runserver



## Authors

  - **Jorge Alberto Delgadilo Alonso** 
