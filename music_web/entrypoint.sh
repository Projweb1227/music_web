#!/bin/bash

python manage.py collectstatic --no-input # --settings=music_web.settings.production

echo "Waiting for database..."
python manage.py waitfordb # --settings=music_web.settings.production

# python manage.py makemigrations --settings=music_web.settings.production
echo "Doing migrations..."
python manage.py migrate 

# python manage.py runserver --settings=music_eng.settings.production
gunicorn --env DJANGO_SETTINGS_MODULE=music_web.settings.production --bind 0.0.0.0:8000 music_web.wsgi:application

