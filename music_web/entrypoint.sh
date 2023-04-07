#!/bin/bash

production=music_web.settings.production
development=music_web.settings.development

settings_in_use=$production

python manage.py collectstatic --no-input --settings=$settings_in_use

echo "Waiting for database..."
python manage.py waitfordb --settings=$settings_in_use


echo "Doing migrations..."
python manage.py migrate --settings=$settings_in_use

# python manage.py runserver --settings=settings_in_use
gunicorn --env DJANGO_SETTINGS_MODULE=$settings_in_use --bind 0.0.0.0:8000 music_web.wsgi:application

