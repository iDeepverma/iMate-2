# I-Mate

## Introduction

Hello There !!!\
This is I-Mate a real-time web-chat app that lets you meet new and intresting people online. While being privacy centric and anonymous.

### Setting up the Project

- Make sure `python3.8` and `pipenv` are installed. Install `pipenv` by running `pip install pipenv`.
- Install python dependencies using the command `pipenv install` 
- To activate this project's virtual environment, run `pipenv shell`.
- Run `python manage.py migrate` on the first run to apply migrations.

### Starting Redis server
You need to have a redis server up and running to properly use this app. You can refer to [link](https://hub.docker.com/_/redis) for instructions to install the redis server.

	sudo docker run -p 6379:6379 -d redis:5
- Start the development server using `python manage.py runserver`

### Setting Up Google Auth
In order to use the Google OAuth authentication you will need to signup for google oauth and register the same with the social App in django admin. Please Refer [link](https://www.section.io/engineering-education/django-google-oauth/) for more info.

<br>
<hr>

- There are two branches one using SqlLite and another from Mysql both are similar in features except the fact that mysql one will not support Emojis on the go and needs to change some defaults of the mysql server to enable so.
