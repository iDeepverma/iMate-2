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
