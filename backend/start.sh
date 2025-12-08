#!/bin/bash
cd /app/backend
python3 manage.py migrate
exec python3 -m gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2
