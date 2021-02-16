#!/usr/bin/env bash

set -e

if [ -n "$ALLOWED_HOSTS" ] && [ -n "$SECRET_KEY" ]; then
  export ALLOWED_HOSTS="$ALLOWED_HOSTS"
  export SECRET_KEY="$SECRET_KEY"
else
  echo "Not all environment variables set!"
  exit
fi

export DJANGO_SETTINGS_MODULE="dene.production_settings"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

chown www-data:www-data /opt/app/dene/db.sqlite3

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi

(gunicorn dene.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"