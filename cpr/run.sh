#!/bin/bash

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000
# gunicorn cpr.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --reload  # for prod, reload is flakey with docker.