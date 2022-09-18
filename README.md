# HackerNewsApi
after cloning

Create a virtual enviroment by inputing - python -m venv env activate env by typing env\scripts\activate

Install ERLANG OTP first then Install Rabbitmq Server launch rabbitmq server

python manage.py makemigrations python manage.py migrate python manage.py runserver

To auto update database: Open terminal and type: celery -A news worker -l INFO --pool=solo 

open another terminal: 
celery -A news beat -l INFO
