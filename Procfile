web: cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
release: cd backend && python manage.py migrate && python manage.py loaddata fixtures/01_categories.json && python manage.py loaddata fixtures/02_features.json
